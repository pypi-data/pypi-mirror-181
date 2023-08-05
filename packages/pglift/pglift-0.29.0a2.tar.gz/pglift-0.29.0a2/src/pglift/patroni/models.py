import functools
import re
import socket
from datetime import timedelta
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

import attr
import pgtoolkit.conf
import yaml
from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConstrainedStr,
    DirectoryPath,
    Field,
    SecretStr,
    root_validator,
    validator,
)
from pydantic.utils import lenient_issubclass

from .. import instances, types

if TYPE_CHECKING:
    from ..ctx import Context
    from ..models import interface, system


class Address(ConstrainedStr):
    r"""Network address type <host or ip>:<port>.

    >>> class Cfg(BaseModel):
    ...     addr: Address
    >>> cfg = Cfg(addr="server:123")
    >>> cfg.addr
    'server:123'
    >>> cfg.addr.host, cfg.addr.port
    ('server', 123)

    >>> Cfg(addr="server")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Cfg
    addr
      string does not match regex "(?P<host>[^\s:?#]+):(?P<port>\d+)" (type=value_error.str.regex; pattern=...)
    >>> Cfg(addr="server:ab")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Cfg
    addr
      string does not match regex "(?P<host>[^\s:?#]+):(?P<port>\d+)" (type=value_error.str.regex; pattern=...)
    """

    __slots__ = ("host", "port")

    regex = re.compile(r"(?P<host>[^\s:?#]+):(?P<port>\d+)")

    A = TypeVar("A", bound="Address")

    def __new__(cls: Type[A], value: str, *, host: str, port: int) -> A:
        return str.__new__(cls, value)

    def __init__(self, value: str, *, host: str, port: int) -> None:
        str.__init__(value)
        self.host = host
        self.port = port

    @classmethod
    def validate(cls: Type[A], value: str) -> A:
        value = super().validate(value)
        m = cls.regex.match(value)
        assert m  # True, per parent validation.
        host, port = m.group("host"), m.group("port")
        return cls(value, host=host, port=int(port))

    @classmethod
    def get(cls: Type[A], port: int) -> A:
        host = socket.gethostbyname(socket.gethostname())
        if host.startswith("127."):  # loopback addresses
            host = socket.getfqdn()
        return cls.validate(f"{host}:{port}")


class _BaseModel(BaseModel):
    class Config:
        allow_mutation = False
        extra = "forbid"
        validate_always = True
        validate_assignment = True


class Bootstrap(_BaseModel):
    class DCS(_BaseModel):
        loop_wait: int = 10

    dcs: DCS = Field(default_factory=DCS)
    initdb: List[Union[str, Dict[str, str]]] = Field(default_factory=list)
    pg_hba: List[str] = Field(
        default_factory=list,
        title="pg_hba.conf",
        description="Lines of pg_hba.conf that Patroni will generate.",
    )
    pg_ident: List[str] = Field(
        default_factory=list,
        title="pg_ident.conf",
        description="Lines of pg_ident.conf that Patroni will generate.",
    )

    @classmethod
    def values(cls, ctx: "Context", manifest: "interface.Instance") -> Dict[str, Any]:
        settings = ctx.settings
        patroni_settings = settings.patroni
        assert patroni_settings
        initdb_options = manifest.initdb_options(settings.postgresql.initdb)
        initdb: List[Union[str, Dict[str, str]]] = [
            {key: value}
            for key, value in initdb_options.dict(exclude_none=True).items()
            if key != "data_checksums"
        ]
        if initdb_options.data_checksums:
            initdb.append("data-checksums")
        pg_hba = manifest.pg_hba(settings).splitlines()
        pg_ident = manifest.pg_ident(settings).splitlines()
        return dict(
            dcs=cls.DCS(loop_wait=patroni_settings.loop_wait),
            initdb=initdb,
            pg_hba=pg_hba,
            pg_ident=pg_ident,
        )


class Log(_BaseModel):
    class Config:
        extra = "allow"

    dir: Optional[DirectoryPath]


class RESTAPI(_BaseModel):
    connect_address: Address = Field(
        default_factory=functools.partial(Address.get, port=8008),
        description="IP address (or hostname) and port, to access the Patroni's REST API.",
    )
    listen: Address = Field(
        default=None,
        description="IP address (or hostname) and port that Patroni will listen to for the REST API.",
    )

    @validator("listen", always=True, pre=True)
    def __validate_listen_(cls, value: Optional[str], values: Dict[str, Any]) -> str:
        """Set 'listen' from 'connect_address' if unspecified.

        >>> RESTAPI(connect_address="localhost:8008")
        RESTAPI(connect_address='localhost:8008', listen='localhost:8008')
        >>> RESTAPI(connect_address="localhost:8008", listen="server:123")
        RESTAPI(connect_address='localhost:8008', listen='server:123')
        """
        if not value:
            value = values["connect_address"]
            assert isinstance(value, str)
        return value


class DCS(_BaseModel):
    pass


class Consul(DCS):
    host: Address = Field(description="Address of Consul local agent.")
    url: AnyHttpUrl = Field(description="URL for the Consul local agent.")


class Etcd(DCS):
    host: Address = Field(
        default="127.0.0.1:2379",
        description="address of the etcd endpoint.",
    )


class ZooKeeper(DCS):
    hosts: List[Address] = Field(
        description="List of ZooKeeper cluster members.",
        min_items=1,
        unique_items=True,
    )


class PostgreSQLPatroniConfig(_BaseModel):
    class Authentication(_BaseModel):
        """PostgreSQL authentication information for Patroni."""

        class User(_BaseModel):
            """PostgreSQL user information."""

            username: str
            password: Optional[SecretStr]

        superuser: User = Field(description="Super-user.")
        replication: User = Field(description="Replication user.")
        rewind: User = Field(default=None, description="User for pg_rewind.")

        @validator("rewind", always=True, pre=True)
        def __validate_rewind_(
            cls, value: Optional[User], values: Dict[str, User]
        ) -> User:
            if not value:
                value = values["superuser"]
            return value

    authentication: Authentication
    connect_address: Address
    data_dir: Path
    bin_dir: DirectoryPath
    listen: Address
    use_unix_socket: bool = False
    use_unix_socket_repl: bool = False
    pgpass: None = None
    # custom_conf
    parameters: Dict[str, Any]
    pg_hba: List[str] = Field(
        default_factory=list,
        title="pg_hba.conf",
        description="Lines of pg_hba.conf that Patroni will generate.",
    )
    pg_ident: List[str] = Field(
        default_factory=list,
        title="pg_ident.conf",
        description="Lines of pg_ident.conf that Patroni will generate.",
    )

    _C = TypeVar("_C", bound="PostgreSQLPatroniConfig")

    @classmethod
    def values(
        cls: Type[_C],
        ctx: "Context",
        instance: "system.BaseInstance",
        manifest: "interface.Instance",
        parameters: Dict[str, Any],
        postgresql_connect_host: Optional[str],
    ) -> Dict[str, Any]:
        settings = ctx.settings
        surole = manifest.surole(settings)
        replrole = manifest.replrole(settings)
        authentication = {
            "superuser": cls.Authentication.User(
                username=surole.name,
                password=(
                    surole.password.get_secret_value() if surole.password else None
                ),
            ),
            "replication": cls.Authentication.User(
                username=replrole.name,
                password=(
                    replrole.password.get_secret_value() if replrole.password else None
                ),
            ),
        }

        if postgresql_connect_host is not None:
            connect_address = Address.validate(
                f"{postgresql_connect_host}:{manifest.port}"
            )
        else:
            connect_address = Address.get(manifest.port)

        listen_addresses = parameters.get("listen_addresses", "*")
        listen = Address.validate(f"{listen_addresses}:{manifest.port}")

        pg_hba = manifest.pg_hba(settings).splitlines()
        pg_ident = manifest.pg_ident(settings).splitlines()

        return dict(
            authentication=authentication,
            connect_address=connect_address,
            data_dir=instance.datadir,
            bin_dir=instance.bindir,
            listen=listen,
            use_unix_socket=True,
            use_unix_socket_repl=True,
            # custom_conf
            parameters=parameters,
            pg_hba=pg_hba,
            pg_ident=pg_ident,
        )


class Patroni(_BaseModel):
    """A Patroni instance."""

    scope: str = Field(description="Cluster name.")
    name: str = Field(description="Host name.")
    log: Optional[Log] = None
    bootstrap: Optional[Bootstrap] = None
    restapi: RESTAPI = Field(default_factory=RESTAPI)
    consul: Optional[Consul]
    etcd: Optional[Etcd]
    etcd3: Optional[Etcd]
    zookeeper: Optional[ZooKeeper]
    postgresql: PostgreSQLPatroniConfig

    _P = TypeVar("_P", bound="Patroni")

    @classmethod
    def build(
        cls: Type[_P],
        scope: str,
        name: str,
        postgresql_connect_host: Optional[str],
        ctx: "Context",
        instance: "system.BaseInstance",
        manifest: "interface.Instance",
        pgconfig: Optional[pgtoolkit.conf.Configuration] = None,
        **args: Any,
    ) -> _P:
        if pgconfig is None:
            pgconfig = instances.configuration(ctx, manifest, instance)

        def s(entry: pgtoolkit.conf.Entry) -> Union[str, bool, int, float]:
            # Serialize pgtoolkit entry without quoting; specially needed to
            # timedelta.
            if isinstance(entry.value, timedelta):
                return entry.serialize().strip("'")
            return entry.value

        parameters = {k: s(e) for k, e in sorted(pgconfig.entries.items())}
        if "bootstrap" not in args:
            args["bootstrap"] = Bootstrap.values(ctx, manifest)
        if "postgresql" not in args:
            args["postgresql"] = PostgreSQLPatroniConfig.values(
                ctx, instance, manifest, parameters, postgresql_connect_host
            )
        return cls(scope=scope, name=name, **args)

    @root_validator
    def __validate_dcs_(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that exactly one DCS is defined.

        >>> Patroni(scope="foo", name="bar")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 2 validation errors for Patroni
        postgresql
          field required (type=value_error.missing)
        __root__
          at least one of ['consul', 'etcd', 'etcd3', 'zookeeper'] is required (type=type_error)

        >>> Patroni.parse_obj({"scope": "main", "name": "pg1", "etcd": {}, "zookeeper": {"hosts": ["server:123"]}})
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 2 validation errors for Patroni
        postgresql
          field required (type=value_error.missing)
        __root__
          at most one of ['consul', 'etcd', 'etcd3', 'zookeeper'] is expected (type=type_error)

        """
        dcs_fields = {
            name
            for name, ftype in cls.__fields__.items()
            if lenient_issubclass(ftype.outer_type_, DCS)
        }
        dcss = {d for d in dcs_fields if values.get(d) is not None}
        if len(dcss) == 0:
            raise TypeError(f"at least one of {sorted(dcs_fields)} is required")
        elif len(dcss) > 1:
            raise TypeError(f"at most one of {sorted(dcs_fields)} is expected")
        return values

    def yaml(self) -> str:
        class Dumper(yaml.SafeDumper):
            pass

        Dumper.add_representer(
            SecretStr,
            lambda dumper, data: dumper.represent_str(data.get_secret_value()),
        )
        Dumper.add_representer(Address, Dumper.represent_str)
        Dumper.add_representer(types.Port, Dumper.represent_int)
        Dumper.add_multi_representer(
            Path,
            lambda dumper, data: dumper.represent_str(str(data)),
        )

        data = self.dict(exclude_none=True)
        return yaml.dump(data, sort_keys=False, Dumper=Dumper)  # type: ignore[no-any-return]


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Service:
    """A Patroni service bound to a PostgreSQL instance."""

    cluster: str
    node: str


class ClusterMember(BaseModel):
    """An item of the list of members returned by Patroni API /cluster endpoint."""

    class Config:
        extra = "allow"
        frozen = True

    host: str
    name: str
    port: int
    role: str
    state: str


class ServiceManifest(types.ServiceManifest, service_name="patroni"):
    _cli_config: ClassVar[Dict[str, types.CLIConfig]] = {
        "cluster_members": {"hide": True},
    }
    _ansible_config: ClassVar[Dict[str, types.AnsibleConfig]] = {
        "cluster_members": {"hide": True},
    }

    # XXX Or simply use instance.qualname?
    cluster: str = Field(
        description="Name (scope) of the Patroni cluster.",
        readOnly=True,
    )
    node: str = Field(
        default_factory=socket.getfqdn,
        description="Name of the node (usually the host name).",
        readOnly=True,
    )
    etcd: Etcd = Field(default_factory=Etcd, description="etcd backend information")
    restapi: RESTAPI = Field(
        default_factory=RESTAPI, description="REST API configuration"
    )
    postgresql_connect_host: Optional[str] = Field(
        default=None,
        description="Host or IP address through which PostgreSQL is externally accessible.",
    )
    cluster_members: List[ClusterMember] = Field(
        default=[],
        description="Members of the Patroni this instance is member of.",
        readOnly=True,
    )
