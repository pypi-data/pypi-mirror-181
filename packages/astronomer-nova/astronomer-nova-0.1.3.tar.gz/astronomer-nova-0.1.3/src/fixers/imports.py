import logging

from redbaron import RedBaron


def fix_imports(class_import_map, red: RedBaron):
    import_nodes = red.find_all("FromImportNode")
    import_nodes = import_nodes.filter(lambda x: x.name.dumps() == "airflow")
    # it might be better only act against certain import paths like
    #   contrib_imports = [node for node in import_nodes if node.find("name", value="contrib")]
    # but for now acting on all imports
    for import_node in import_nodes:

        if len(import_node.targets) == 1:
            imported_class = import_node.targets[0].value
            new_imported_class = class_import_map.get(imported_class, None)
            if not new_imported_class:
                logging.warning(f"Unhandled import: {import_node.dumps()}")
                continue

            import_node.value = new_imported_class["value"]
        else:
            had_import_error = False
            for node in import_node.targets:

                imported_class = node.value
                new_imported_class = class_import_map.get(imported_class, None)
                if not new_imported_class:
                    had_import_error = True
                    logging.warning(f"Unhandled import: {import_node.dumps()}")
                    continue
                import_node.insert_after(
                    f"from {new_imported_class['value']} import {imported_class}"
                )
            if not had_import_error:
                # RedBaron doesn't handle weird indentation well
                # It's possible this throws the Exception
                #   Exception: It appears that you have indentation in your CommaList,
                #   for now RedBaron doesn't know how to handle this situation
                #   (which requires a lot of work), sorry about that. You can find
                #   more information here https://github.com/PyCQA/redbaron/issues/100
                del import_node.parent[import_node.index_on_parent]
