import logging
import re
from pathlib import Path
from typing import List, NoReturn, Optional, Tuple
from unittest.mock import patch

import psycopg
import pytest
from pgtoolkit import conf as pgconf
from pgtoolkit.ctl import Status
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from pglift import databases, db, exceptions, instances, postgresql, systemd
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.postgresql import Standby
from pglift.settings import PostgreSQLVersion, Settings
from pglift.systemd import service_manager

from . import AuthType, check_connect, execute, reconfigure_instance
from .conftest import DatabaseFactory, Factory


def test_directories(instance: system.Instance) -> None:
    assert instance.datadir.exists()
    assert instance.waldir.exists()
    assert (instance.waldir / "archive_status").is_dir()


def test_config(
    instance: system.Instance, instance_manifest: interface.Instance
) -> None:
    postgresql_conf = instance.datadir / "postgresql.conf"
    assert postgresql_conf.exists()
    pgconfig = pgconf.parse(postgresql_conf)
    assert {k for k, v in pgconfig.entries.items() if not v.commented} & set(
        instance_manifest.settings
    )


def test_psqlrc(instance: system.Instance) -> None:
    assert instance.psqlrc.read_text().strip().splitlines() == [
        f"\\set PROMPT1 '[{instance}] %n@%~%R%x%# '",
        "\\set PROMPT2 ' %R%x%# '",
    ]


def test_systemd(ctx: Context, instance: system.Instance) -> None:
    if ctx.settings.service_manager == "systemd":
        assert systemd.is_enabled(
            ctx, service_manager.unit("postgresql", instance.qualname)
        )


def test_reinit(
    ctx: Context,
    instance: system.PostgreSQLInstance,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Instance already exists, no-op.
    with monkeypatch.context() as m:

        def fail() -> NoReturn:
            raise AssertionError("unexpected called")

        m.setattr(postgresql, "pg_ctl", fail)
        instances.init(
            ctx, interface.Instance(name=instance.name, version=instance.version)
        )


def test_log_directory(instance: system.Instance, log_directory: Path) -> None:
    config = instance.config()
    assert isinstance(config.log_directory, str)
    instance_log_dir = Path(config.log_directory)
    assert instance_log_dir == log_directory
    assert instance_log_dir.exists()


def passfile_entries(passfile: Path, *, role: str = "postgres") -> List[str]:
    return [line for line in passfile.read_text().splitlines() if f":{role}:" in line]


def test_pgpass(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    postgresql_auth: AuthType,
    surole_password: Optional[str],
    pgbackrest_password: Optional[str],
) -> None:
    passfile = ctx.settings.postgresql.auth.passfile
    if postgresql_auth != AuthType.pgpass:
        pytest.skip(f"not applicable for auth:{postgresql_auth}")

    port = instance.port
    backuprole = ctx.settings.postgresql.backuprole.name

    assert passfile_entries(passfile) == [f"*:{port}:*:postgres:{surole_password}"]
    assert passfile_entries(passfile, role=backuprole) == [
        f"*:{port}:*:{backuprole}:{pgbackrest_password}"
    ]

    with reconfigure_instance(ctx, instance_manifest, port=port + 1):
        assert passfile_entries(passfile) == [
            f"*:{port+1}:*:postgres:{surole_password}"
        ]
        assert passfile_entries(passfile, role=backuprole) == [
            f"*:{port+1}:*:{backuprole}:{pgbackrest_password}"
        ]

    assert passfile_entries(passfile) == [f"*:{port}:*:postgres:{surole_password}"]
    assert passfile_entries(passfile, role=backuprole) == [
        f"*:{port}:*:{backuprole}:{pgbackrest_password}"
    ]


def test_connect(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    postgresql_auth: AuthType,
) -> None:
    with postgresql.running(ctx, instance):
        check_connect(ctx, postgresql_auth, instance_manifest, instance)


def test_replrole(ctx: Context, instance: system.Instance) -> None:
    with postgresql.running(ctx, instance):
        (row,) = execute(
            ctx,
            instance,
            # Simplified version of \du in psql.
            "SELECT rolsuper, rolcanlogin, rolreplication,"
            " ARRAY(SELECT b.rolname"
            "       FROM pg_catalog.pg_auth_members m"
            "       JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)"
            "       WHERE m.member = r.oid) as memberof"
            " FROM pg_catalog.pg_roles r"
            " WHERE rolname = 'replication'",
        )
    assert row == {
        "rolsuper": False,
        "rolcanlogin": True,
        "rolreplication": True,
        "memberof": ["pg_read_all_stats"],
    }


def test_hba(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance: system.Instance,
    postgresql_auth: AuthType,
) -> None:
    hba_path = instance.datadir / "pg_hba.conf"
    hba = hba_path.read_text().splitlines()
    auth_settings = ctx.settings.postgresql.auth
    auth_instance = instance_manifest.auth
    assert auth_instance is not None
    if postgresql_auth == AuthType.peer:
        assert "peer" in hba[0]
    assert (
        f"local   all             all                                     {auth_settings.local}"
        in hba
    )
    assert (
        f"host    all             all             127.0.0.1/32            {auth_instance.host}"
        in hba
    )


def test_ident(
    ctx: Context, instance: system.Instance, postgresql_auth: AuthType
) -> None:
    ident_path = instance.datadir / "pg_ident.conf"
    ident = ident_path.read_text().splitlines()
    assert ident[0] == "# MAPNAME       SYSTEM-USERNAME         PG-USERNAME"
    if postgresql_auth == AuthType.peer:
        assert re.match(r"^test\s+\w+\s+postgres$", ident[1])
    else:
        assert len(ident) == 1


def test_start_stop_restart_running_is_ready_stopped(
    ctx: Context, instance: system.Instance, caplog: pytest.LogCaptureFixture
) -> None:
    i = instance
    use_systemd = ctx.settings.service_manager == "systemd"
    if use_systemd:
        assert not systemd.is_active(
            ctx, service_manager.unit("postgresql", i.qualname)
        )

    instances.start(ctx, i)
    try:
        assert postgresql.status(ctx, i) == Status.running
        assert postgresql.is_ready(ctx, i)
        if use_systemd:
            assert systemd.is_active(
                ctx, service_manager.unit("postgresql", i.qualname)
            )
    finally:
        instances.stop(ctx, i)

        # Stopping a non-running instance is a no-op.
        caplog.clear()
        with caplog.at_level(logging.WARNING, logger="pglift"):
            instances.stop(ctx, i)
        assert f"instance {instance} is already stopped" in caplog.records[0].message

    assert postgresql.status(ctx, i) == Status.not_running
    assert not postgresql.is_ready(ctx, i)
    if use_systemd:
        assert not systemd.is_active(
            ctx, service_manager.unit("postgresql", i.qualname)
        )

    instances.start(ctx, i)
    try:
        assert postgresql.status(ctx, i) == Status.running
        assert postgresql.is_ready(ctx, i)
        if not use_systemd:
            # FIXME: systemctl restart would fail with:
            #   Start request repeated too quickly.
            #   Failed with result 'start-limit-hit'.
            instances.restart(ctx, i)
            assert postgresql.status(ctx, i) == Status.running
            assert postgresql.is_ready(ctx, i)
        instances.reload(ctx, i)
        assert postgresql.status(ctx, i) == Status.running
        assert postgresql.is_ready(ctx, i)
    finally:
        instances.stop(ctx, i, mode="immediate")

    assert postgresql.status(ctx, i) == Status.not_running
    with instances.stopped(ctx, i):
        assert postgresql.status(ctx, i) == Status.not_running
        with instances.stopped(ctx, i):
            assert postgresql.status(ctx, i) == Status.not_running
            assert not postgresql.is_ready(ctx, i)
        with instances.running(ctx, i):
            assert postgresql.status(ctx, i) == Status.running
            assert postgresql.is_ready(ctx, i)
            with instances.running(ctx, i):
                assert postgresql.status(ctx, i) == Status.running
            with instances.stopped(ctx, i):
                assert postgresql.status(ctx, i) == Status.not_running
                assert not postgresql.is_ready(ctx, i)
            assert postgresql.status(ctx, i) == Status.running
            assert postgresql.is_ready(ctx, i)
        assert postgresql.status(ctx, i) == Status.not_running
    assert postgresql.status(ctx, i) == Status.not_running
    assert not postgresql.is_ready(ctx, i)


def test_apply(
    ctx: Context,
    pg_version: str,
    tmp_path: Path,
    instance_factory: Factory[Tuple[interface.Instance, system.Instance]],
    caplog: pytest.LogCaptureFixture,
) -> None:
    i = system.BaseInstance.get("test_apply", pg_version, ctx)
    assert postgresql.status(ctx, i) == Status.unspecified_datadir
    im, i = instance_factory(
        ctx.settings,
        name="test_apply",
        settings={
            "unix_socket_directories": str(tmp_path),
            "ssl": True,
        },
        restart_on_changes=False,
        roles=[{"name": "bob"}],
        databases=[
            {"name": "db1"},
            {"name": "db2", "owner": "bob", "extensions": ["unaccent"]},
        ],
        pgbackrest={"stanza": "test_apply_stanza"},
    )
    assert i.port == im.port
    pgconfig = i.config()
    assert pgconfig
    assert pgconfig.ssl

    result_apply = instances.apply(ctx, im)
    assert result_apply.change_state is None  # no-op

    assert postgresql.status(ctx, i) == Status.not_running
    im = im._copy_validate({"state": "started"})
    result_apply = instances.apply(ctx, im)
    assert result_apply.change_state == interface.ApplyChangeState.changed
    assert postgresql.status(ctx, i) == Status.running
    with db.connect(ctx, i) as conn:
        assert not instances.pending_restart(conn)

    with postgresql.running(ctx, i):
        assert databases.exists(ctx, i, "db1")
        assert databases.exists(ctx, i, "db2")
        db2 = databases.get(ctx, i, "db2")
        assert db2.extensions == ["unaccent"]
        assert db2.owner == "bob"

    newconfig = im.settings.copy()
    newconfig["listen_addresses"] = "*"  # requires restart
    newconfig["autovacuum"] = False  # requires reload
    im = im._copy_validate({"settings": newconfig})
    with caplog.at_level(logging.DEBUG, logger="pgflit"):
        result_apply = instances.apply(ctx, im)
        assert result_apply.change_state == interface.ApplyChangeState.changed
    assert (
        f"instance {i} needs restart due to parameter changes: listen_addresses"
        in caplog.messages
    )
    assert postgresql.status(ctx, i) == Status.running
    with db.connect(ctx, i) as conn:
        assert instances.pending_restart(conn)

    im = im._copy_validate({"state": "stopped"})
    result_apply = instances.apply(ctx, im)
    assert result_apply.change_state == interface.ApplyChangeState.changed
    assert postgresql.status(ctx, i) == Status.not_running

    im = im._copy_validate({"state": "absent"})
    assert instances.apply(ctx, im).change_state == interface.ApplyChangeState.dropped
    with pytest.raises(exceptions.InstanceNotFound):
        i.exists()
    assert postgresql.status(ctx, i) == Status.unspecified_datadir


def test_get(
    ctx: Context,
    instance: system.Instance,
    log_directory: Path,
    pgbackrest_available: bool,
    powa_available: bool,
) -> None:
    im = instances.get(ctx, instance)
    assert im is not None
    assert im.name == "test"
    config = im.settings
    assert im.port == instance.port
    # Pop host-dependent values.
    del config["effective_cache_size"]
    del config["shared_buffers"]
    spl = "passwordcheck"
    if powa_available:
        spl += ", pg_qualstats, pg_stat_statements, pg_stat_kcache"
    socket_directory = str(ctx.settings.postgresql.socket_directory).format(
        instance=instance
    )
    expected_config = {
        "cluster_name": "test",
        "lc_messages": "C",
        "lc_monetary": "C",
        "lc_numeric": "C",
        "lc_time": "C",
        "log_destination": "stderr",
        "log_directory": str(log_directory),
        "logging_collector": False,
        "shared_preload_libraries": spl,
        "unix_socket_directories": socket_directory,
    }
    if pgbackrest_available:
        del config["archive_command"]
        expected_config["archive_mode"] = True
        expected_config["wal_level"] = "replica"
    assert config == expected_config
    assert im.data_checksums is False
    assert im.state.name == "stopped"
    assert not im.pending_restart

    with postgresql.running(ctx, instance):
        im = instances.get(ctx, instance)
        assert not im.pending_restart
        assert im.locale


def test_list(ctx: Context, instance: system.Instance) -> None:
    not_instance_dir = Path(
        str(ctx.settings.postgresql.datadir).format(
            version="12", name="notAnInstanceDir"
        )
    )
    not_instance_dir.mkdir(parents=True)
    try:
        ilist = list(instances.list(ctx))

        for i in ilist:
            assert i.status == Status.not_running.name
            # this also ensure instance name is not notAnInstanceDir
            assert i.name == "test"

        for i in ilist:
            if (i.version, i.name) == (instance.version, instance.name):
                break
        else:
            assert False, f"Instance {instance.version}/{instance.name} not found"

        iv = next(instances.list(ctx, version=instance.version))
        assert iv == i
    finally:
        not_instance_dir.rmdir()


def test_standby_instance(
    ctx: Context,
    instance: system.Instance,
    replrole_password: str,
    standby_manifest: interface.Instance,
    standby_instance: system.Instance,
) -> None:
    standby = standby_manifest.standby
    assert standby
    slotname = standby.slot
    assert standby_instance.standby
    assert standby_instance.standby.primary_conninfo
    assert (
        standby_instance.standby.password
        and standby_instance.standby.password.get_secret_value() == replrole_password
    )
    assert standby_instance.standby.slot == slotname
    with postgresql.running(ctx, instance):
        rows = execute(ctx, instance, "SELECT slot_name FROM pg_replication_slots")
    assert [r["slot_name"] for r in rows] == [slotname]


def test_standby_pgpass(
    settings: Settings,
    postgresql_auth: AuthType,
    standby_instance: system.Instance,
) -> None:
    if postgresql_auth != AuthType.pgpass:
        pytest.skip(f"not applicable for auth:{postgresql_auth}")
    passfile = settings.postgresql.auth.passfile
    assert str(standby_instance.port) not in passfile.read_text()


def test_standby_replication(
    pg_version: str,
    ctx: Context,
    instance: system.Instance,
    instance_manifest: interface.Instance,
    settings: Settings,
    postgresql_auth: AuthType,
    surole_password: Optional[str],
    database_factory: DatabaseFactory,
    standby_instance: system.Instance,
) -> None:
    assert standby_instance.standby

    surole = instance_manifest.surole(settings)
    replrole = instance_manifest.replrole(settings)

    if surole.password:

        def get_stdby() -> Optional[Standby]:
            assert surole.password
            with patch.dict(
                "os.environ", {"PGPASSWORD": surole.password.get_secret_value()}
            ):
                return instances._get(ctx, standby_instance).standby

    else:

        def get_stdby() -> Optional[Standby]:
            return instances._get(ctx, standby_instance).standby

    class OutOfSync(AssertionError):
        pass

    @retry(
        retry=retry_if_exception_type(psycopg.OperationalError),
        wait=wait_fixed(2),
        stop=stop_after_attempt(5),
    )
    def assert_db_replicated() -> None:
        rows = execute(
            ctx,
            standby_instance,
            "SELECT * FROM t",
            role=replrole,
            dbname="test",
        )
        if rows[0]["i"] != 1:
            pytest.fail(f"table 't' not replicated; rows: {rows}")

    @retry(
        retry=retry_if_exception_type(OutOfSync),
        wait=wait_fixed(2),
        stop=stop_after_attempt(5),
    )
    def assert_replicated(expected: int) -> None:
        rlag = postgresql.replication_lag(standby_instance)
        assert rlag is not None
        row = execute(
            ctx,
            standby_instance,
            "SELECT * FROM t",
            role=replrole,
            dbname="test",
        )
        if row[0]["i"] != expected:
            assert rlag > 0
            raise OutOfSync
        if rlag > 0:
            raise OutOfSync
        if rlag != 0:
            pytest.fail(f"non-zero replication lag: {rlag}")

    with postgresql.running(ctx, instance), postgresql.running(ctx, standby_instance):
        database_factory("test", owner=replrole.name)
        execute(
            ctx,
            instance,
            "CREATE TABLE t AS (SELECT 1 AS i)",
            dbname="test",
            fetch=False,
            role=replrole,
        )
        stdby = get_stdby()
        assert stdby is not None
        assert stdby.primary_conninfo == standby_instance.standby.primary_conninfo
        assert stdby.password == replrole.password
        assert stdby.slot == standby_instance.standby.slot
        assert stdby.replication_lag is not None
        if pg_version >= "12":
            assert stdby.wal_sender_state == "streaming"

        assert execute(
            ctx,
            standby_instance,
            "SELECT * FROM pg_is_in_recovery()",
            role=replrole,
            dbname="template1",
        ) == [{"pg_is_in_recovery": True}]

        assert_db_replicated()

        execute(
            ctx,
            instance,
            "UPDATE t SET i = 42",
            dbname="test",
            role=replrole,
            fetch=False,
        )

        assert_replicated(42)

        stdby = get_stdby()
        assert stdby is not None
        assert stdby.replication_lag == 0
        if pg_version >= "12":
            assert stdby.wal_sender_state == "streaming"

        instances.promote(ctx, standby_instance)
        assert not standby_instance.standby
        assert execute(
            ctx,
            standby_instance,
            "SELECT * FROM pg_is_in_recovery()",
            role=replrole,
            dbname="template1",
        ) == [{"pg_is_in_recovery": False}]
        # Check that we can connect to the promoted instance.
        connargs = {
            "host": str(standby_instance.config().unix_socket_directories),
            "port": standby_instance.port,
            "user": surole.name,
        }
        if postgresql_auth == AuthType.peer:
            pass
        else:
            connargs["password"] = surole_password
        with psycopg.connect(**connargs) as conn:  # type: ignore[call-overload]
            if postgresql_auth == AuthType.peer:
                assert not conn.pgconn.used_password
            else:
                assert conn.pgconn.used_password


def test_upgrade(
    ctx: Context, instance: system.Instance, upgraded_instance: system.Instance
) -> None:
    assert upgraded_instance.name == "upgraded"
    assert upgraded_instance.version == instance.version
    assert postgresql.status(ctx, upgraded_instance) == Status.not_running
    with postgresql.running(ctx, upgraded_instance):
        assert databases.exists(ctx, upgraded_instance, "postgres")


def test_upgrade_pgpass(
    ctx: Context,
    postgresql_auth: AuthType,
    upgraded_instance: system.Instance,
    surole_password: Optional[str],
    pgbackrest_password: Optional[str],
) -> None:
    passfile = ctx.settings.postgresql.auth.passfile
    if postgresql_auth != AuthType.pgpass:
        pytest.skip(f"not applicable for auth:{postgresql_auth}")
    backuprole = ctx.settings.postgresql.backuprole.name
    port = upgraded_instance.port
    assert f"*:{port}:*:postgres:{surole_password}" in passfile_entries(passfile)
    assert f"*:{port}:*:{backuprole}:{pgbackrest_password}" in passfile_entries(
        passfile, role=backuprole
    )


def test_server_settings(ctx: Context, instance: system.Instance) -> None:
    with postgresql.running(ctx, instance), db.connect(ctx, instance) as conn:
        pgsettings = instances.settings(conn)
    port = next(p for p in pgsettings if p.name == "port")
    assert port.setting == str(instance.port)
    assert not port.pending_restart
    assert port.context == "postmaster"


def test_logs(
    ctx: Context, instance_manifest: interface.Instance, instance: system.Instance
) -> None:
    try:
        postgresql.start_postgresql(
            ctx, instance, foreground=False, wait=True, logging_collector="on"
        )
    finally:
        postgresql.stop_postgresql(ctx, instance, mode="immediate", wait=True)
    logs = list(instances.logs(ctx, instance))
    assert "database system is shut down" in logs[-1]


def test_get_locale(ctx: Context, instance: system.Instance) -> None:
    with postgresql.running(ctx, instance), db.connect(ctx, instance) as conn:
        assert instances.get_locale(conn) == "C"
    postgres_conf = instance.datadir / "postgresql.conf"
    original_conf = postgres_conf.read_text()
    with postgres_conf.open("a") as f:
        f.write("\nlc_numeric = ''\n")
    try:
        with postgresql.running(ctx, instance), db.connect(ctx, instance) as conn:
            assert instances.get_locale(conn) is None
    finally:
        postgres_conf.write_text(original_conf)


def test_data_checksums(
    ctx: Context,
    pg_version: str,
    instance_factory: Factory[Tuple[interface.Instance, system.Instance]],
    caplog: pytest.LogCaptureFixture,
) -> None:
    manifest, instance = instance_factory(ctx.settings, "datachecksums")

    assert execute(ctx, instance, "SHOW data_checksums") == [{"data_checksums": "off"}]

    # explicitly enabled
    manifest = manifest._copy_validate({"data_checksums": True})
    if pg_version <= PostgreSQLVersion.v11:
        with pytest.raises(
            exceptions.UnsupportedError,
            match=r"^PostgreSQL <= 11 doesn't have pg_checksums to enable data checksums$",
        ):
            instances.apply(ctx, manifest)
        return

    with caplog.at_level(logging.INFO, logger="pglift.instances"):
        result_apply = instances.apply(ctx, manifest)
        assert result_apply.change_state == interface.ApplyChangeState.changed
    assert execute(ctx, instance, "SHOW data_checksums") == [{"data_checksums": "on"}]
    assert "enabling data checksums" in caplog.messages
    caplog.clear()

    assert instances._get(ctx, instance).data_checksums

    # not explicitly disabled so still enabled
    result_apply = instances.apply(
        ctx, manifest._copy_validate({"data_checksums": None})
    )
    assert result_apply.change_state is None
    assert execute(ctx, instance, "SHOW data_checksums") == [{"data_checksums": "on"}]

    # explicitly disabled
    with caplog.at_level(logging.INFO, logger="pglift.instances"):
        result_apply = instances.apply(
            ctx, manifest._copy_validate({"data_checksums": False})
        )
        assert result_apply.change_state == interface.ApplyChangeState.changed
    assert execute(ctx, instance, "SHOW data_checksums") == [{"data_checksums": "off"}]
    assert "disabling data checksums" in caplog.messages
    caplog.clear()
    assert instances._get(ctx, instance).data_checksums is False

    # re-enabled with instance running
    with postgresql.running(ctx, instance):
        with pytest.raises(
            exceptions.InstanceStateError,
            match="could not alter data_checksums on a running instance",
        ):
            instances.apply(ctx, manifest._copy_validate({"data_checksums": True}))
    assert instances._get(ctx, instance).data_checksums is False
