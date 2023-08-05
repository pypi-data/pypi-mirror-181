import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from pglift import exceptions
from pglift.ctx import Context
from pglift.models.system import Instance
from pglift.settings import DataPath, PostgreSQLSettings, Settings, SiteSettings


def test_json_config_settings_source(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(
        '{"postgresql": {"datadir": "/mnt/postgresql/{version}/{name}/data"}}'
    )
    with monkeypatch.context() as m:
        m.setenv("SETTINGS", f"@{settings}")
        s = SiteSettings()
    assert s.postgresql.datadir == Path("/mnt/postgresql/{version}/{name}/data")
    with monkeypatch.context() as m:
        m.setenv(
            "SETTINGS",
            '{"postgresql": {"datadir": "/data/postgres/{version}/{version}-{name}/data"}}',
        )
        s = SiteSettings()
    assert s.postgresql.datadir == Path(
        "/data/postgres/{version}/{version}-{name}/data"
    )
    with monkeypatch.context() as m:
        m.setenv("SETTINGS", f"@{tmp_path / 'notfound'}")
        with pytest.raises(FileNotFoundError):
            SiteSettings()


def test_yaml_settings(site_settings: MagicMock, tmp_path: Path) -> None:
    configdir = tmp_path / "pglift"
    configdir.mkdir()
    settings_fpath = configdir / "settings.yaml"
    settings_fpath.write_text("prefix: /tmp")
    site_settings.return_value = settings_fpath
    s = SiteSettings()
    assert str(s.prefix) == "/tmp"

    settings_fpath.write_text("hello")
    site_settings.return_value = settings_fpath
    with pytest.raises(exceptions.SettingsError, match="expecting an object"):
        SiteSettings()


def test_custom_sources_order(
    site_settings: MagicMock, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    configdir = tmp_path / "pglift"
    configdir.mkdir()
    settings_fpath = configdir / "settings.yaml"
    settings_fpath.write_text("prefix: /tmp")
    site_settings.return_value = settings_fpath

    with monkeypatch.context() as m:
        m.setenv("SETTINGS", '{"prefix": "/tmp/foo"}')
        s = SiteSettings()
    assert str(s.prefix) == "/tmp/foo"


def test_libpq_environ(ctx: Context, settings: Settings, instance: Instance) -> None:
    assert settings.postgresql.libpq_environ(
        ctx, instance, settings.postgresql.surole.name, base={}
    ) == {"PGPASSFILE": str(settings.postgresql.auth.passfile)}
    assert settings.postgresql.libpq_environ(
        ctx,
        instance,
        settings.postgresql.surole.name,
        base={"PGPASSFILE": "/var/lib/pgsql/pgpass"},
    ) == {"PGPASSFILE": "/var/lib/pgsql/pgpass"}


def test_libpq_environ_password_command(
    ctx: Context, instance: Instance, pg_version: str, tmp_path: Path
) -> None:
    settings = PostgreSQLSettings.parse_obj(
        {
            "auth": {
                "password_command": [
                    sys.executable,
                    "-c",
                    "import sys; print(f'{{sys.argv[1]}}-secret')",
                    "{instance}",
                    "--blah",
                ],
                "passfile": str(tmp_path / "pgpass"),
            }
        }
    )
    assert settings.libpq_environ(ctx, instance, settings.surole.name, base={}) == {
        "PGPASSFILE": str(tmp_path / "pgpass"),
        "PGPASSWORD": f"{pg_version}/test-secret",
    }


def test_settings(tmp_path: Path) -> None:
    s = Settings(prefix="/")
    assert hasattr(s, "postgresql")
    assert hasattr(s.postgresql, "datadir")
    assert s.postgresql.datadir == Path("/srv/pgsql/{version}/{name}/data")
    assert s.logpath == Path("/log")

    with pytest.raises(Exception) as e:
        s.postgresql.datadir = DataPath("/tmp/new_root/{version}/{name}/data")
    assert "is immutable and does not support item assignment" in str(e)

    datadir = tmp_path / "{version}" / "{name}"
    s = Settings.parse_obj(
        {
            "prefix": "/prefix",
            "run_prefix": "/runprefix",
            "postgresql": {"datadir": str(datadir)},
        }
    )
    assert s.postgresql.datadir == datadir


def test_validate_templated_path() -> None:
    with pytest.raises(
        ValueError,
        match="/var/lib/{name} template doesn't use expected variables: name, version",
    ):
        Settings.parse_obj(
            {
                "postgresql": {
                    "datadir": "/var/lib/{name}",
                },
            }
        )


def test_postgresql_versions(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config = {
        "postgresql": {
            "bindir": "/usr/lib/pgsql/{version}/bin",
            "versions": [
                {
                    "version": "11",
                    "bindir": "/opt/pgsql-11/bin",
                },
            ],
        },
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config))
    with monkeypatch.context() as m:
        m.setenv("SETTINGS", f"@{config_path}")
        s = SiteSettings()
    pgversions = s.postgresql.versions
    assert set(v.version for v in pgversions) == {"11", "12", "13", "14", "15"}
    assert (
        str(next(v.bindir for v in pgversions if v.version == "11"))
        == "/opt/pgsql-11/bin"
    )
    assert (
        str(next(v.bindir for v in pgversions if v.version == "12"))
        == "/usr/lib/pgsql/12/bin"
    )

    config["postgresql"]["default_version"] = "7"
    config_path.write_text(json.dumps(config))
    with monkeypatch.context() as m:
        m.setenv("SETTINGS", f"@{config_path}")
        with pytest.raises(
            ValidationError, match="value is not a valid enumeration member; permitted:"
        ):
            SiteSettings()

    config["postgresql"]["default_version"] = "13"
    config_path.write_text(json.dumps(config))
    with monkeypatch.context() as m:
        m.setenv("SETTINGS", f"@{config_path}")
        s = SiteSettings()
    assert s.postgresql.default_version == "13"


def test_systemd_systemctl() -> None:
    with patch("shutil.which", return_value=None) as which:
        with pytest.raises(ValidationError, match="systemctl command not found"):
            Settings(systemd={})
    which.assert_called_once_with("systemctl")


def test_systemd_sudo_user() -> None:
    with pytest.raises(ValidationError, match="'user' mode cannot be used with 'sudo'"):
        Settings.parse_obj({"systemd": {"user": True, "sudo": True}})


def test_systemd_disabled() -> None:
    with pytest.raises(ValidationError, match="cannot use systemd"):
        Settings.parse_obj({"scheduler": "systemd"})
    with pytest.raises(ValidationError, match="cannot use systemd"):
        Settings.parse_obj({"service_manager": "systemd"})


def test_systemd_service_manager_scheduler() -> None:
    with patch("shutil.which", return_value=True) as which:
        assert Settings(systemd={}).service_manager == "systemd"
    which.assert_called_once_with("systemctl")
    with patch("shutil.which", return_value=True) as which:
        assert (
            Settings(systemd={}, service_manager="systemd").service_manager == "systemd"
        )
    which.assert_called_once_with("systemctl")
    with patch("shutil.which", return_value=True) as which:
        assert Settings(systemd={}, service_manager=None).service_manager is None
    which.assert_called_once_with("systemctl")
