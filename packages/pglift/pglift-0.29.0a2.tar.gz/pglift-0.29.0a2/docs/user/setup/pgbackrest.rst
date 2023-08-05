pgBackRest site configuration
=============================

pgBackRest satellite component can be enabled through site settings by
defining a non-``null`` ``pgbackrest`` key, e.g.:

.. code-block:: yaml
   :caption: settings.yaml

    pgbackrest:
      execpath: /usr/local/bin/pgbackrest
      repopath: /backups

.. note::
   Use ``pglift site-settings --schema`` (possibly piped through ``jq
   .definitions.PgBackRestSettings``) to retrieve possible settings for the
   ``pgbackrest`` section.

Then use the ``site-configure`` command to install base pgbackrest
configuration file and directories.

Upon instance creation, pgBackRest is set up by:

* adding some configuration to PostgreSQL,
* writing a pgBackRest configuration file for this instance, and,
* initializing the pgBackRest repository.

PostgreSQL configuration is handled through parameters set in
``postgresql.conf`` file as documented in :ref:`PostgreSQL site
configuration <postgresql-site-configuration>`. The default values for those
parameters are:

.. literalinclude:: ../../../src/pglift/postgresql/pgbackrest.conf

and can be overridden by providing a ``postgresql/pgbackrest.conf`` template
file in site configuration directory.
