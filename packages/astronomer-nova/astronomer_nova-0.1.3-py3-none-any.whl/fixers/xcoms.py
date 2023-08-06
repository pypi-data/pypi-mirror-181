from redbaron import Node, RedBaron


def fix_xcom_push(red: RedBaron):
    # Fix xcom_push -> do_xcom_push in Operator args
    xcom_push_nodes = red.find_all("NameNode", value="xcom_push")
    args_xcom_push_nodes = xcom_push_nodes.filter(
        lambda x: x.parent.type == "call_argument"
    )
    args_xcom_push_nodes.map(lambda x: x.replace("do_xcom_push"))


def fix_xcom_pull(red: RedBaron):
    # Fix xcom_push -> do_xcom_push in Operator args
    xcom_pull_nodes = red.find_all("NameNode", value="xcom_pull")
    args_xcom_pull_nodes = xcom_pull_nodes.filter(
        lambda x: x.parent.type == "call_argument"
    )
    for node in args_xcom_pull_nodes:
        arg = node.parent
        _remove_arg_via_fst(arg)


# Method to resolve https://github.com/PyCQA/redbaron/issues/100
def _remove_arg_via_fst(arg):
    call_fst = arg.parent.fst()
    # Account for commas in Call FST
    # Last argument or last argument with trailing comma
    if (
        len(call_fst["value"]) == arg.index_on_parent * 2
        or len(call_fst["value"]) == arg.index_on_parent * 2 + 1
    ):
        call_fst["value"] = call_fst["value"][: arg.index_on_parent * 2]
    # Not last argument
    else:
        call_fst["value"] = (
            call_fst["value"][: arg.index_on_parent * 2]
            + call_fst["value"][arg.index_on_parent * 2 + 2 :]
        )
    new_call_node = Node.from_fst(
        call_fst, parent=arg.parent.parent, on_attribute="call"
    )
    new_call_node.parent.call_.replace(new_call_node)
