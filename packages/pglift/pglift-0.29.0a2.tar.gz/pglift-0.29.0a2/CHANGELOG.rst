Changelog
---------

.. towncrier release notes start

0.29.0a2 - 2022-12-13
~~~~~~~~~~~~~~~~~~~~~

Removals
++++++++

- Change priority order of site config files. Order is now xdg > etc > dist.


0.29.0a1 - 2022-12-13
~~~~~~~~~~~~~~~~~~~~~

Features
++++++++

- Improve warning message when failing to connect to primary instance in
  ``instance get``.
- Make `replication` role a member of ``pg_read_all_stats``.
- Add WAL sender state (from `pg_stat_replication
  <https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-VIEW>`_
  view) to standby information (as available in ``instance get`` command).


Bug fixes
+++++++++

- Catch JSON decode exception when parsing ``SETTINGS`` environment variable.

  This prevents showing a traceback when the json provided for ``SETTINGS``
  environment variable is invalid.
- Catch :class:`~pglift.exceptions.SettingsError` when loading site settings
  in CLI.

  Prevents displaying a traceback if there's an error when parsing the site
  settings YAML file.
- Fix path to pglift in systemd service when using pre-built binary

  `ExecPath` in ``pglift-postgresql@`` systemd service which was wrongly set
  to an inexistent path.


Removals
++++++++

- Require pgbackrest>=2.41

  ``pglift instance backups`` now runs ``pgbackrest info --set=<backup set>
  --output=json`` which only works since pgbackrest 2.41.
- Hide ``standby.status`` field from ``instance get`` output: this field is
  not very useful since it will only appear on standby instances, which are by
  definition in *demoted* state.


0.28.0 - 2022-12-02
~~~~~~~~~~~~~~~~~~~

Features
++++++++

- If pgbackrest is enabled, log install and uninstall operations at
  ``site-configure``.
- Configure systemd timer for instance backup with a randomized delay.
- Add a ``--dry-run`` option to `apply` commands.
- Add support for "force" option for database drop.
- Improve logging when starting/stopping Prometheus `postgres_exporter` and
  `temboard-agent`.
- Allow to pass any command to ``instance exec`` (not just Postgres commands
  or absolute ones as previously).
- Make it possible to operate normal instances even when `patroni` is enabled
  in site settings.
- Add support for PostgreSQL 15.
- Make check for port availability more robust.
- Improve `systemd` unit template for PostgreSQL. It is now defined as a
  ``Type=notify`` service and does not use a ``PIDFile`` anymore, following
  more closely what's suggested in `PostgreSQL documentation
  <https://www.postgresql.org/docs/current/server-start.html>`_.


Bug fixes
+++++++++

- pglift 0.27.0 is now the minimum required version for the Ansible
  collection.
- Fixed error during enabling/disabling temboard service with systemd caused by a
  bad service name.
- Fix error in ``instance env`` command for a standby instance with pgbackrest
  enabled.
- Only start Patroni once at instance creation (avoid a stop and a start).
  This should make concurrent setups (e.g. from Ansible targeting different
  hosts in parallel) work without dead-locking Patroni.
- Avoid starting / stopping PostgreSQL many times at instance creation.


Removals
++++++++

- The Ansible collection got moved to its `own repository
  <https://gitlab.com/dalibo/pglift-ansible>`_.
- Avoid useless ``pgbackrest start`` invocation after stanza creation.
- Separate management of shared_preload_libraries and database extensions.

  The ``extensions`` key in instance's model has been dropped. To install
  extensions in an instance, you now need to provide the
  ``shared_preload_libraries`` in instance settings.
- No longer error out, but simply warn, upon invalid Patroni configuration as
  reported by ``patroni --validate-config``.
- Only validate generated Patroni configuration for Patroni version higher than
  2.1.5.



Documentation
+++++++++++++

- Extend how to about standby management with Ansible to illustrate promote
  operation.
- Add some details about `site configuration` in installation documentation.


Misc.
+++++

- Add a hidden ``--debug`` command-line flag to set log level to ``DEBUG`` and
  eventually get tracebacks displayed.
- Unconditionally call ``pgbackrest stanza-create`` upon instance.
  re-configuration whereas this was previously only done at instance creation.
  Conversely, the ``--no-online`` option is used to avoid superfluous instance
  startup. On the other hand the ``pgbackrest check`` command is still only
  emitted at instance creation.
- Add ``--output=json`` option to ``postgres_exporter apply`` command.
- Rework systemd installation through site-configure hook.
- Use pglift CLI in systemd unit for PostgreSQL.
- Use `towncrier <https://towncrier.readthedocs.io/>`_ to manage news
  fragments.


0.27.0 - 2022-11-02
~~~~~~~~~~~~~~~~~~~

Features
++++++++

- Support for RockyLinux 9
- Ability to provide a name for pgbackrest stanza
- Handling of ``REASSIGN OWNED`` and ``DROP OWNED`` when dropping a role
- Better handling of model validation errors in the CLI
- Ability to create a database as a clone of an existing one
- JSON output to ``instance env`` command
- JSON output to ``apply`` sub-commands
- Prometheus password change upon ``instance alter``
- Prometheus password kept upon instance upgrade
- Raise a specific error if role being dropped has dependent database objects
- Raise a specific error when Postgres binary directory for requested version
  does not exist

Bug fixes
+++++++++

- ``SETTINGS`` environment variable takes precedence over YAML setting file
- Fix systemd service name for Patroni-managed instances
- Fix service name inconsistency for temboard-agent
- Entries of ``postgresql.conf``, set by ``initdb``, no longer commented
- Fix a type error when retrieve instance environment from Ansible module
- Replication password passed through environment when invoking
  ``pg_basebackup``

Removals
++++++++

- Field ``pgbackrest_restore`` excluded from ``instance get`` command output
- Database auto discover in default postgres_exporter configuration
- CLI option ``--json``, replaced by ``--output-format=json``
- Instance model's ``configuration``, renamed as ``settings``, to be
  consistent with eponymous field on Database objects
- Standby's ``for`` field renamed as ``primary_conninfo`` in the declarative
  API

Documentation
+++++++++++++

- Added an example playbook for a standby instance
- Fix settings in Ansible tutorial (``pgpass`` fields missing for ``surole``
  and ``backuprole``)

Misc.
+++++

- Limit database connection openings in ``instance get``
- Installation of global pgbackrest configuration through ``site-configure``
  command
- Setting ``postgresql.versions`` now defined as a list
- Use pglift CLI in Ansible modules, instead of the Python API
- PyOxidizer configuration to build a binary version of pglift
