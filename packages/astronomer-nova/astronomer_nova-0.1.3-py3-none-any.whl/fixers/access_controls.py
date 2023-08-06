import logging

from redbaron import RedBaron


def fix_access_controls(red: RedBaron):
    # Check for DAG access controls
    dag_access_control_nodes = red.find_all("NameNode", value="access_control")
    if len(dag_access_control_nodes):
        accts = []
        for node in dag_access_control_nodes:
            accts.append(node.parent.dict_.dictitem_.key_.dumps())
            arg = node.parent
            arg.value = "None"
        logging.warning(f"Contains DAG access controls. Setting to None: {accts}")
