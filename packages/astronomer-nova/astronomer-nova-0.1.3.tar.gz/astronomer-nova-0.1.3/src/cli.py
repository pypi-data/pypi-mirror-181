import logging
import os.path

import click

from nova import upgrade_dag_file, upgrade_dag_files


@click.command()
@click.argument("dag_path", default="dags/")
@click.argument("out_dir", default="dags/upgraded")
@click.option(
    "-r",
    "--rename-dag",
    "rename_dag",
    is_flag=True,
    show_default=True,
    default=False,
    help="Append `_updated` to dag_id.",
)
def cli(dag_path: str, out_dir: str, rename_dag):
    """
    Upgrade all dags in `dag_path` and saves them to `out_dir`.
    :param ctx: Click context
    :param dag_path: "The path to the `dags` folder."
    :param out_dir: "The output directory to store upgraded `dags`."
    :param rename_dag: "Append `_updated` to dag_id."
    :return: None
    """

    LOG_FORMAT = "[%(name)s] [%(levelname)s] %(message)s"
    LOG_LEVEL = logging.INFO
    formatter = logging.Formatter(LOG_FORMAT)
    airflow_logger = logging.getLogger("airflow_modules")
    airflow_logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(formatter)
    airflow_logger.addHandler(handler)

    if os.path.isfile(dag_path):
        upgrade_dag_file(dag_path, out_dir, rename_dag)
    else:
        upgrade_dag_files(dag_path, out_dir, rename_dag)
