# Astronomer Nova
### (Formerly Airflow V2 Upgrader)

This project aims to automate common tasks when upgrading DAGs from Airflow 1 to Airflow 2,
making use of [RedBaron](https://redbaron.readthedocs.io/en/latest/) to parse and manipulate the Python syntax tree.

# Features

- Automatically upgrade DAG source code from Airflow 1 to Airflow 2
- Scan Dags and report changes (Coming Soon)

# Installation
You can install the Astronomer Nova CLI through Pip

```shell
pip install astronomer-nova
```

The simplest way to get started with Astronomer Nova is by using the astro cli.
Simply add `astronomer-nova` to your list of dependencies in `requirements.txt`.
Then you can run it with the following commands:

```shell
astro dev start
astro dev bash
nova
```

## Installation from sources

To install astronomer-nova in [development mode](https://pip.pypa.io/en/latest/cli/pip_install/#install-editable):

```shell
pip install --editable .[lint,test]
```

To build from sources:

```
python -m build
```

OR

```
python -m pip wheel .
```

## Running tests:

```shell
python -m pytest
```

# How to Use

```shell
nova dags/ dags/upgraded/
```

For more information, you can access the help menu with:

```shell
nova --help
```

# How it works

Astronomer Nova performs the upgrade by:

1. Building an import map for classes in `airflow.hooks`, `airflow.operators`, `airflow.sensors`, and `airflow.providers`, which maps the classes to the current Airflow version import path.
2. Modifying Python files in a DAG directory to update
   - Imports
   - DAG access controls
   - XCOM push
   - XCOM pull
3. Writing updated DAG to either the same DAG directory or a parameter output directory with `_upgraded` added to the filename.

The script is configured to run against `./dags` and to write output to `./dags/upgraded` by default.

## Caveats

In order to load the Airflow import map, Airflow provider packages must be installed. There are often cross-dependencies within Airflow providers (eg `airflow.operators.s3_to_hive_operator` required the Hive provider), so make sure the `requirements.txt` file includes all necessary .

The script currently tries to correct imports that do not need to be changed going from Airflow 1 to 2, and logging does not include which files are currently being acted against.

The code uses Astronomer-centric opinions, like removing DAG-level RBAC. In the future, I'd rather have these decisions configurable at runtime, as well as generating per-DAG reports on the DAGs that can be used for further remediation, as well as understanding of DAG requirements, like the use of Connections and Variables.


# Contribute

- Issue Tracker: https://github.com/astronomer/astronomer-nova/issues
- Source Code: https://github.com/astronomer/astronomer-nova

# Contact

cabella@astronomer.io