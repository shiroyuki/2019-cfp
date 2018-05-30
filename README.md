# Yak-Bak

Future home of a tech conference call for proposals and program selection app.

## Running it Locally

Yak-Bak requires Python 3.6 or newer.

1. Install requirements: `pip install -r test-requirements.txt`

    You may want to use [virtualenv](https://virtualenv.pypa.io/en/stable/)
    or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
    to prevent interference with or by other installed packages and projects.

2. Copy the `yakbak.toml-local` file to `yakbak.toml`.

    The `yakbak.toml-local` file contains sensible defaults for local
    development, but not proper values for production configuration. On your
    production systems, you will have to manage the configuration file outside
    of the repository. Be a good citizen and don't ever check production
    configuration into the source code repo!

3. Choose a database and enter an appropriate URI in `yakbak.toml`

    For local development with Postgres, you may use
    `postgres+psycopg2://localhost/yakbak`, assuming a database name of
    `yakbak`.

    For local development with SQLite, you may use `sqlite://yakbak.sqlite3`,
    which will create a file named `yakbak.sqlite3` in the repository root.

    We recommend that you use PostgreSQL 10 or newer. You will also need to
    install the PostgreSQL driver for python with `pip install psycopg2`.

4. Create tables in the database with `alembic upgrade head`

5. Run the Flask development server: `FLASK_APP=wsgi flask run`

    You may find the `--debugger` and `--reload` flags helpful during
    development.

6. Run tests with `py.test yakbak`, check style compliance with `tox -e
   style`, check types with `tox -e mypy`, or run the full CI suite (tests,
   style check, and type check) simply with `tox`.
