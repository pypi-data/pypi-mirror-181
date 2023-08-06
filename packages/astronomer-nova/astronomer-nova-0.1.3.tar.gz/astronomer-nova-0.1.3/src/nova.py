import importlib
import inspect
import logging
import os
import pkgutil
import sys
import warnings
from typing import List, Optional

from flake8.api import legacy as flake8

from redbaron import RedBaron
from baron.parser import ParsingError

from fixers import fix_access_controls, fix_imports, fix_xcom_pull, fix_xcom_push

# logging.basicConfig(level=logging.DEBUG)

warnings.filterwarnings("error")

LOG_FORMAT = "[%(name)s] [%(levelname)s] %(message)s"
LOG_LEVEL = logging.INFO
formatter = logging.Formatter(LOG_FORMAT)
nova_logger = logging.getLogger("nova")
nova_logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(formatter)
nova_logger.addHandler(handler)

# TODO Give control over fixers to run
_fixers = [
    "fix_imports",
    "fix_access_controls",
    "fix_xcom_push",
    "fix_xcom_pull",
    "update_dag_name",
    # TODO Worker Queues
]
_reports = [
    # TODO Async Optimizations
    # TODO Worker Queues
]

common_dag_class_imports = [
    "airflow.hooks",
    "airflow.operators",
    "airflow.sensors",
    "airflow.providers",
]


def _get_class_import_map(root_module) -> dict:
    found_packages = list(pkgutil.iter_modules(root_module.__path__))
    if not found_packages:
        return {}
    # action_names = [
    #     (name.split(".")[-1], ispkg) for _, name, ispkg in found_packages
    # ]
    # importer = found_packages[0][0]
    class_import_map = {}
    for x, name, ispkg in found_packages:
        if ispkg:
            try:
                module = importlib.import_module(f"{root_module.__name__}.{name}")
            except Exception as e:
                breakpoint()
            submodule_class_import_map = _get_class_import_map(module)
            class_import_map = {**submodule_class_import_map, **class_import_map}

        else:
            try:
                module = importlib.import_module(f"{root_module.__name__}.{name}")
                if f"{root_module.__name__}.{name}" not in sys.modules:
                    continue
                classes = inspect.getmembers(module, inspect.isclass)
                for class_name, c in classes:
                    if c.__module__ != f"{root_module.__name__}.{name}":
                        continue
                    class_import_map[class_name] = {
                        "value": f"{root_module.__name__}.{name}",
                        "targets": class_name,
                    }
            except DeprecationWarning as err:
                nova_logger.debug(
                    f"Skip deprecated module {root_module.__name__}.{name}: {err}"
                )
            except ModuleNotFoundError as err:
                nova_logger.error(
                    f"Cannot load modules from {root_module.__name__}.{name}: {err}"
                )
            except UserWarning as err:
                continue
    return class_import_map


def _generate_import_map() -> dict:
    class_import_map = {}
    for common_dag_class_import in common_dag_class_imports:
        root_module = importlib.import_module(common_dag_class_import)
        class_import_map = {
            **_get_class_import_map(root_module),
            **class_import_map,
        }
    return class_import_map


def _upgrade_dag_file(
    filename: str, out_dir: str, class_import_map, rename_dag: Optional[bool] = False
) -> None:
    if "upgraded" in filename:
        return
    red = _load_dag_file(filename)
    if red is None:
        return
    fix_imports(class_import_map, red)
    fix_access_controls(red)
    fix_xcom_push(red)
    fix_xcom_pull(red)
    if rename_dag:
        _update_dag_name(red)
    updated_filename = _write_updated_dag_file(filename, out_dir, red)
    _validate_updated_dag(updated_filename)


def _load_dag_file(filename: str) -> RedBaron:
    try:
        with open(filename, "r") as f:
            code = f.read()
        return RedBaron(code)
    except ParsingError as pe:
        nova_logger.error(f'{filename} contains errors and is not valid Python.\n {pe}')


def _write_updated_dag_file(filename: str, out_dir: str, red: RedBaron) -> str:
    upgraded_filename = filename
    upgraded_filename = os.path.join(out_dir, os.path.basename(upgraded_filename))

    with open(upgraded_filename, "w") as f:
        f.write(red.dumps())

    return upgraded_filename


def _validate_updated_dag(filename: str) -> None:
    style_guide = flake8.get_style_guide(ignore=[])
    report = style_guide.check_files([filename])
    if len(report.get_statistics('E999')) > 0:
        nova_logger.error(f'{filename} contains errors and is not valid Python.')


def _update_dag_name(red: RedBaron) -> None:
    # update dag name
    dag_def = red.find("NameNode", value="DAG").parent
    dag_name = dag_def.call_[0].string_.value
    file_name = dag_name[:-1]
    ext = dag_name[-1]
    dag_def.call_[0].value = f"{file_name}_upgraded{ext}"


def _create_out_dir_if_not_exists(out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)


def _get_dag_files_from_dir(dag_dir: str) -> List[str]:
    return [
        os.path.join(dag_dir, f)
        for f in os.listdir(dag_dir)
        if os.path.isfile(os.path.join(dag_dir, f)) and f[-3:] == ".py"
    ]


def upgrade_dag_files(
    dag_dir: str,
    out_dir: Optional[str] = None,
    rename_dag: Optional[bool] = False,
):
    if not dag_dir:
        nova_logger.error("No DAG directory provided.")
        exit()
    if not out_dir:
        out_dir = os.path.join(dag_dir, "upgraded/")

    _create_out_dir_if_not_exists(out_dir)
    class_import_map = _generate_import_map()

    dag_files = _get_dag_files_from_dir(dag_dir)
    for dag_file in dag_files:
        _upgrade_dag_file(dag_file, out_dir, class_import_map, rename_dag)


def upgrade_dag_file(
    dag_file: str,
    out_dir: Optional[str] = None,
    rename_dag: Optional[bool] = False,
):
    _create_out_dir_if_not_exists(out_dir)
    class_import_map = _generate_import_map()
    _upgrade_dag_file(dag_file, out_dir, class_import_map, rename_dag)
