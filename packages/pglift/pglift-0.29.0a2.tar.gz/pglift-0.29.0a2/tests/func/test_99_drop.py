import pathlib

import pytest
import requests
from pgtoolkit.conf import Configuration

import pglift.pgbackrest.impl as pgbackrest
import pglift.prometheus.impl as prometheus
from pglift import exceptions, systemd
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import Settings
from pglift.systemd import scheduler, service_manager

from . import AuthType


def test_pgpass(
    settings: Settings,
    postgresql_auth: AuthType,
    instance_manifest: interface.Instance,
    to_be_upgraded_instance_dropped: Configuration,
    upgraded_instance_dropped: Configuration,
    instance_dropped: Configuration,
) -> None:
    if postgresql_auth != AuthType.pgpass:
        pytest.skip("not applicable")
    passfile = settings.postgresql.auth.passfile
    assert not passfile.exists()


@pytest.mark.usefixtures("require_systemd_scheduler")
def test_systemd_backup_job(
    ctx: Context, instance: system.Instance, instance_dropped: Configuration
) -> None:
    unit = scheduler.unit("backup", instance.qualname)
    assert not systemd.is_active(ctx, unit)
    assert not systemd.is_enabled(ctx, unit)


def test_pgbackrest_teardown(
    ctx: Context,
    instance: system.Instance,
    standby_instance_dropped: Configuration,
    upgraded_instance_dropped: Configuration,
    to_be_upgraded_instance_dropped: Configuration,
    instance_dropped: Configuration,
) -> None:
    pgbackrest_settings = pgbackrest.available(ctx.settings)
    if not pgbackrest_settings:
        pytest.skip("pgbackrest not available")
    stanza = f"mystanza-{instance.name}"
    assert (
        next((pgbackrest_settings.repopath / "archive").glob(f"{stanza}*"), None)
        is None
    )
    assert (
        next((pgbackrest_settings.repopath / "backup").glob(f"{stanza}*"), None) is None
    )
    assert not (pgbackrest_settings.configpath / "conf.d" / f"{stanza}.conf").exists()
    # global directories and files are preserved
    assert (pgbackrest_settings.configpath / "pgbackrest.conf").exists()
    assert (pgbackrest_settings.configpath / "conf.d").exists()
    assert pgbackrest_settings.repopath.exists()
    assert pgbackrest_settings.spoolpath.exists()
    assert pgbackrest_settings.lockpath.exists()
    assert pgbackrest_settings.logpath.exists()
    assert next(pgbackrest_settings.logpath.glob(f"{stanza}*.log"), None) is None


def test_prometheus_teardown(
    ctx: Context,
    instance: system.Instance,
    instance_dropped: Configuration,
) -> None:
    prometheus_settings = prometheus.available(ctx.settings)
    if not prometheus_settings:
        pytest.skip("prometheus not available")
    configpath = pathlib.Path(
        str(prometheus_settings.configpath).format(name=instance.qualname)
    )
    queriespath = pathlib.Path(
        str(prometheus_settings.queriespath).format(name=instance.qualname)
    )
    assert not configpath.exists()
    assert not queriespath.exists()
    if ctx.settings.service_manager == "systemd":
        assert not systemd.is_enabled(
            ctx, service_manager.unit("postgres_exporter", instance.qualname)
        )
        with pytest.raises(requests.ConnectionError):
            requests.get("http://0.0.0.0:9187/metrics")


def test_databases_teardown(
    instance: system.Instance,
    instance_dropped: Configuration,
) -> None:
    assert not instance.dumps_directory.exists()


def test_instance(
    ctx: Context, instance: system.Instance, instance_dropped: Configuration
) -> None:
    with pytest.raises(exceptions.InstanceNotFound, match=str(instance)):
        instance.exists()
