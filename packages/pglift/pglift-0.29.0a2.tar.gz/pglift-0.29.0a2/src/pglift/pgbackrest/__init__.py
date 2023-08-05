import logging
from typing import TYPE_CHECKING, Dict, Literal, Optional, Type

import pgtoolkit.conf as pgconf

from .. import exceptions, hookimpl, util
from ..models import interface, system
from ..postgresql import Standby
from ..settings import PostgreSQLVersion
from . import impl, models
from .impl import available as available
from .impl import backup as backup
from .impl import config_directory
from .impl import expire as expire
from .impl import get_settings
from .impl import iter_backups as iter_backups
from .impl import restore as restore
from .models import ServiceManifest

if TYPE_CHECKING:
    import click

    from ..ctx import Context
    from ..settings import Settings

__all__ = ["available", "backup", "expire", "iter_backups", "restore"]

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


@hookimpl
def site_configure_install(settings: "Settings") -> None:
    s = get_settings(settings)
    global_config = impl.base_config(s)
    logger.info("installing base pgbackrest configuration")
    config_template = util.template("pgbackrest", "pgbackrest.conf")
    pgbackrest_config = config_template.format(**s.dict())
    global_config.parent.mkdir(parents=True, exist_ok=True)
    with global_config.open("w") as f:
        f.write(pgbackrest_config)
    s.repopath.mkdir(exist_ok=True, parents=True)
    s.logpath.mkdir(exist_ok=True, parents=True)
    s.spoolpath.mkdir(exist_ok=True, parents=True)
    s.lockpath.mkdir(exist_ok=True, parents=True)
    config_directory(s).mkdir(mode=0o750, exist_ok=True)


@hookimpl
def site_configure_uninstall(settings: "Settings") -> None:
    s = get_settings(settings)
    if not util.rmdir(config_directory(s)):
        return
    logger.info("uninstalling base pgbackrest configuration")
    impl.base_config(s).unlink(missing_ok=True)
    util.rmdir(s.configpath)


@hookimpl
def system_lookup(
    ctx: "Context", instance: "system.PostgreSQLInstance"
) -> Optional[models.Service]:
    settings = get_settings(ctx.settings)
    return impl.system_lookup(instance.datadir, settings)


@hookimpl
def get(
    ctx: "Context", instance: "system.Instance"
) -> Optional[models.ServiceManifest]:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(stanza=s.stanza)


@hookimpl
def instance_settings(
    ctx: "Context", manifest: "interface.Instance", instance: "system.BaseInstance"
) -> pgconf.Configuration:
    settings = get_settings(ctx.settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    stanza = service_manifest.stanza or instance.qualname
    return impl.postgresql_configuration(stanza, settings)


@hookimpl
def interface_model() -> Type[models.ServiceManifest]:
    return models.ServiceManifest


@hookimpl
def instance_configure(
    ctx: "Context",
    manifest: "interface.Instance",
    config: pgconf.Configuration,
    creating: bool,
    upgrading_from: Optional[system.Instance],
) -> None:
    """Install pgBackRest for an instance when it gets configured."""
    settings = get_settings(ctx.settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    instance = system.PostgreSQLInstance.system_lookup(
        ctx, (manifest.name, manifest.version)
    )
    if instance.standby:
        return

    stanza = service_manifest.stanza or instance.qualname
    service = models.Service(
        stanza=stanza, path=impl.config_directory(settings) / f"{stanza}.conf"
    )
    if creating and upgrading_from is None and impl.enabled(instance, settings):
        if not ctx.confirm(
            f"Stanza '{stanza}' already bound to another instance, continue by overwriting it?",
            False,
        ):
            raise exceptions.Cancelled("Pgbackrest repository already exists")
        impl.revert_init(ctx, instance, service, settings, None)
        impl.revert_setup(ctx, service, settings, config, instance.datadir)

    impl.setup(ctx, service, settings, config, instance.datadir)

    password = None
    backup_role = role(ctx.settings, manifest)
    assert backup_role is not None
    if not backup_role.pgpass and backup_role.password is not None:
        password = backup_role.password.get_secret_value()
    if upgrading_from is not None:
        impl.upgrade(ctx, instance, service, settings, password)
    else:
        impl.init(ctx, instance, service, settings, password, run_check=creating)


@hookimpl
def initdb(
    ctx: "Context", manifest: "interface.Instance", instance: system.BaseInstance
) -> Optional[Literal[True]]:
    service_manifest = manifest.service_manifest(ServiceManifest)
    if service_manifest.restore is None:
        return None
    settings = get_settings(ctx.settings)
    logger.info("creating instance from pgbackrest backup")
    cmd = [
        str(settings.execpath),
        "--log-level-file=off",
        "--log-level-stderr=info",
        "--config-path",
        str(settings.configpath),
        "--stanza",
        service_manifest.restore.stanza,
        "--pg1-path",
        str(instance.datadir),
    ]
    if manifest.standby:
        cmd.append("--type=standby")
    cmd.append("restore")
    ctx.run(cmd, check=True)
    return True


@hookimpl
def instance_init_replication(
    ctx: "Context",
    instance: system.BaseInstance,
    manifest: "interface.Instance",
    standby: Standby,
) -> Optional[bool]:
    service_manifest = manifest.service_manifest(ServiceManifest)
    if service_manifest.restore is None:
        return None
    if instance.version == PostgreSQLVersion.v11:
        path = instance.datadir / "recovery.conf"
    else:
        path = instance.datadir / "postgresql.auto.conf"
    config = pgconf.parse(str(path))
    logger.info("configure standby from pgbackrest backup")
    with config.edit() as entries:
        entries.add("primary_conninfo", standby.full_primary_conninfo)
        if standby.slot:
            entries.add("primary_slot_name", standby.slot)
    config.save()
    return True


@hookimpl
def instance_drop(ctx: "Context", instance: system.Instance) -> None:
    """Uninstall pgBackRest from an instance being dropped."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    settings = get_settings(ctx.settings)
    nb_backups = len(impl.backup_info(ctx, service, settings)["backup"])
    if not nb_backups or ctx.confirm(
        f"Confirm deletion of {nb_backups} backup(s) for instance {instance}?",
        True,
    ):
        impl.revert_init(ctx, instance, service, settings, None)
        impl.revert_setup(ctx, service, settings, instance.config(), instance.datadir)


@hookimpl
def instance_env(ctx: "Context", instance: "system.Instance") -> Dict[str, str]:
    pgbackrest_settings = impl.get_settings(ctx.settings)
    try:
        service = instance.service(models.Service)
    except ValueError:
        return {}
    return impl.env_for(service, pgbackrest_settings)


@hookimpl
def rolename(settings: "Settings") -> str:
    return settings.postgresql.backuprole.name


@hookimpl
def role(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional["interface.Role"]:
    name = rolename(settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    password = None
    if service_manifest.password:
        password = service_manifest.password.get_secret_value()
    pgpass = settings.postgresql.backuprole.pgpass
    return interface.Role(
        name=name,
        password=password,
        login=True,
        superuser=True,
        pgpass=pgpass,
    )


@hookimpl
def cli() -> "click.Command":
    from .cli import pgbackrest

    return pgbackrest


@hookimpl
def instance_cli(group: "click.Group") -> None:
    from .cli import instance_backup, instance_backups, instance_restore

    group.add_command(instance_backup)
    group.add_command(instance_backups)
    group.add_command(instance_restore)
