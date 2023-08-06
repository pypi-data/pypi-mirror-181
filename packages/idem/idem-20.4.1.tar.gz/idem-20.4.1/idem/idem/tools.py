import copy
import fnmatch
import inspect
import warnings
from typing import Any
from typing import Dict
from typing import List


def gen_chunk_func_tag(hub, chunk):
    """
    Generate the unique tag used to track the execution of the chunk
    """
    if "sls_run_id" in chunk:
        return _gen_sls_run_tag(chunk, f'{_gen_tag(chunk)}{chunk["fun"]}')

    return f'{_gen_tag(chunk)}{chunk["fun"]}'


def gen_chunk_esm_tag(hub, chunk: Dict[str, str]) -> str:
    """
    Generate the unique tag used to track the execution of the chunk in the esm
    """
    if "sls_run_id" in chunk:
        return _gen_sls_run_tag(chunk, _gen_tag(chunk))

    return _gen_tag(chunk)


def _gen_sls_run_tag(chunk, tag):
    sls_run_tag = ""
    # As chuck has an attribute sls_run_id, it indicates this chunk is part of a sls.run.
    # so add the parent state. In this case parent state is sls
    sls_run_tag += "sls"

    # Add id of the chunk
    # This Identifies the tag uniquely. <sls.run name>:<Id of the resource>
    sls_run_tag += f'_|-{chunk["__id__"]}'

    # Add the rest of the tag as we do for a normal run
    sls_run_tag += f"_|-{tag}"

    return sls_run_tag


def _gen_tag(chunk: Dict[str, str]) -> str:
    """
    Generate the unique tag used to track the execution of the chunk

    This will be used at a module level, agnostic to function names
    """
    tag = f'{chunk["state"]}_|-{chunk["__id__"]}_|-{chunk["name"]}_|-'

    # if `name_prefix` is present and `name` is formed with `name_prefix`, then create tag based on `name_prefix`
    if chunk.get("name_prefix") and chunk.get("name_prefix") in chunk["name"]:
        tag = f'{chunk["state"]}_|-{chunk["__id__"]}_|-{chunk["name_prefix"]}_|-'

    return tag


def get_sls_run_chunks(hub, low, state, sls_run_id, path_args, from_esm=False):
    """
    Search in the low state for the chunk with the given state, sls_run_id and path_args
    we find the exact chunk inside group of sls_files in a sls.run with name sls_run_id.
    Example-: if we have path_args = [{'cloud2:state2:property_path': 'new_state:key'}]
    we will find the chunk in low data with state cloud2 and name state2 and sls_run of chunk
    should match sls_run_id and updated path_args would be [{property_path:'new_state:key'}]


    state4:
     cloud1.state_def:
      - parameters:
            arg1: ${sls:state1:sls:state2:cloud2:state3:property_path}

    In the above example the actual state or chunk is cloud2:state3:property_path which is part of a sls.run
    named state2 and state2 is part of another sls.run named state1. To find the exact chunk in low data we need to
    split and process the requisite recursively till we reach the exact chunk.

    In first run sls_run_id=state1 and path_args = [{'sls:state2:cloud2:state3:property_path': 'new_state:key'}]
    After first run we find chunks with name=state2 and state=sls, since state2 is also a sls.run we did not reach the exact chunk.

    In the second run sls_run_id=state1:sls:state2 and path_args = [{'cloud2:state2:property_path': 'new_state:key'}]
    In second run we search for state=cloud2 and name = state3 and sls_run_id=state1:sls:state2
    which indicates chunk is part of state2 and state2 should be part of state1

    the chunk we found after second un is not a sls.run. we reached the exact chunk,
    so return that chunk and updated_args (the value being referred in chunk)
    """
    chunks_found = []
    new_path_args = []
    for path_arg in path_args:
        name_def = next(iter(path_arg))
        name_def_list = name_def.split(":")
        if len(name_def_list) > 1:
            new_state = name_def_list.pop(0)
            new_name = name_def_list.pop(0)

            if from_esm:
                original_chunks = hub.tool.idem.esm.get_chunks_from_esm(
                    new_state, new_name, sls_run_id
                )
            else:
                original_chunks = hub.idem.tools.get_chunks(
                    low, new_state, sls_run_id + ":" + new_name
                )

            # check if chunks belong to same run else filter them
            original_chunks = [
                original_chunk
                for original_chunk in original_chunks
                if original_chunk["sls_run_id"] == sls_run_id
            ]
            if original_chunks:
                original_chunk = original_chunks[0]
                # After finding the exact chunk we need to check if the chunk is sls.run
                # if chunk is sls.run this means we have a nested sls.run, and we did not reach the exact chunk.
                # so we need to find the chunk recursively till we get a non sls.run chunk.
                # sls_run_id in the chunk for nested module will be <name of outer sls.run><hub.states.sls.SLS_RUN_SEPARATOR><name of inner sls.run>
                # so we call the method recursively with updated sls_run name, new state and new_path_args
                if (
                    original_chunk["state"] == "sls"
                    and original_chunk["fun"] == "run"
                    and len(name_def_list) > 1
                ):
                    hub.log.debug(
                        f"nested sls.run found. calling the function get_sls_run_chunks with updated sls_run_id {sls_run_id + hub.states.sls.SLS_RUN_SEPARATOR + new_name}"
                    )
                    new_arg_key = ":".join(name_def_list)
                    new_path_args.append({new_arg_key: path_arg[name_def]})
                    return hub.idem.tools.get_sls_run_chunks(
                        low,
                        new_state,
                        sls_run_id + hub.states.sls.SLS_RUN_SEPARATOR + new_name,
                        new_path_args,
                        from_esm,
                    )
            chunks_found.extend(original_chunks)
            new_arg_key = ":".join(name_def_list)
            new_path_args.append({new_arg_key: path_arg[name_def]})
        else:
            if from_esm:
                chunks_found = hub.tool.idem.esm.get_chunks_from_esm(
                    state, sls_run_id, sls_run_id
                )
            else:
                chunks_found = hub.idem.tools.get_chunks(low, state, sls_run_id)

            new_path_args = path_args
    return chunks_found[0] if chunks_found else None, new_path_args


def get_chunks(hub, low, state, name):
    """
    Search in the low state for the chunk with the given designation
    """
    rets = []
    for chunk in low:
        if state == "sls":
            if fnmatch.fnmatch(chunk["__sls__"], name):
                rets.append(chunk)
                continue
        if state == chunk["state"]:
            if fnmatch.fnmatch(chunk["name"], name) or fnmatch.fnmatch(
                chunk["__id__"], name
            ):
                rets.append(chunk)
    return rets


def find_name(hub, name, state, high):
    """
    Scan high data for the id referencing the given name and return a list of (IDs, state) tuples that match
    Note: if `state` is sls, then we are looking for all IDs that match the given SLS
    """
    ext_id = []
    if name in high:
        ext_id.append((name, state))
    # if we are requiring an entire SLS, then we need to add ourselves to everything in that SLS
    elif state == "sls":
        for nid, item in high.items():
            if item["__sls__"] == name:
                ext_id.append((nid, next(iter(item))))
    # otherwise we are requiring a single state, lets find it
    else:
        # We need to scan for the name
        for nid in high:
            if state in high[nid]:
                if isinstance(high[nid][state], list):
                    for arg in high[nid][state]:
                        if not isinstance(arg, dict):
                            continue
                        if len(arg) != 1:
                            continue
                        if arg[next(iter(arg))] == name:
                            ext_id.append((nid, state))
    return ext_id


def format_call(
    hub,
    fun,
    data,
    ignore_changes: List = None,
    expected_extra_kws=(),
    enforced_state: Dict[str, Any] = None,
):
    """
    Build the required arguments and keyword arguments required for the passed
    function.
    :param fun: The function to get the argspec from
    :param data: A dictionary containing the required data to build the
                 arguments and keyword arguments.
    :param ignore_changes: A list of path of parameters that will be assigned to None value
                           to ignore being updated in present().
    :param expected_extra_kws: Any expected extra keyword argument names which
                               should not trigger a :ref:`SaltInvocationError`
    :param enforced_state: A dictionary with the parameters from a previous run
    :returns: Function keyword arguments.
    """
    enforced_state = enforced_state or {}

    args = []
    kwargs = {}
    keywords = False

    sig = fun.signature
    for name, param in sig.parameters.items():
        if name == "hub":
            continue
        elif param.kind.name == "POSITIONAL_OR_KEYWORD":
            if param.default is inspect._empty:
                if name in enforced_state:
                    # get it from enforced state before state
                    kwargs[name] = enforced_state[name]
                else:
                    # Warn about required argument that is not stored in ESM
                    if enforced_state and name != "ctx":
                        msg = (
                            f"Function {fun.ref}.{fun.func.__name__} argument '{name}' is required, "
                            f"but is not found in ESM cache for {gen_chunk_func_tag(hub, data)}"
                        )
                        warnings.warn(msg, RuntimeWarning)
                        hub.log.warning(msg)
                    args.append(name)
            else:
                kwargs[name] = enforced_state.get(name, param.default)
                # Validate a boolean value for arguments of type boolean
                if isinstance(param.default, bool):
                    if data.get(name) and not isinstance(data.get(name), bool):
                        raise TypeError(
                            f"{fun.ref}.{fun.func.__name__} is expecting a boolean value for '{name}' but got '{data.get(name)}'"
                        )
        elif param.kind.name == "KEYWORD_ONLY":
            # get it from enforced state before default
            kwargs[name] = enforced_state.get(name, param.default)
        elif param.kind.name == "VAR_KEYWORD":
            keywords = True

    # Since we WILL be changing the data dictionary, let's change a copy of it
    data = data.copy()
    is_existing_resource = bool(enforced_state) or bool(data.get("resource_id"))

    missing_args = []

    for key in kwargs:
        try:
            # Do not override enforced_state value with None,
            # unless no value is set
            val = data.pop(key)
            if val is not None or kwargs[key] is inspect._empty:
                kwargs[key] = val

            # if the execution flow is for recreating a resource,
            # then we should override enforced_state value with None for resource_id
            if key == "resource_id" and data.get("recreation_flow", False):
                kwargs[key] = val
        except KeyError:
            # Let's leave the default value in place
            pass

    # If ignore_changes contains parameters, then we try to assign those parameters with None to skip updating.
    # For resource recreation flow, we should not nullify the parameters in ignore_changes.
    if (
        ignore_changes
        and is_existing_resource
        and not data.get("recreation_flow", False)
    ):
        hub.idem.tool.ignore_changes.ignore_parameter_changes(
            ignore_changes=ignore_changes,
            params=kwargs,
            param_signatures=sig.parameters,
        )

    while args:
        # Every function takes ctx as an argument.
        # All others are required function arguments that do not exist in ESM
        arg = args.pop(0)
        try:
            kwargs[arg] = data.pop(arg)
        except KeyError:
            missing_args.append(arg)

    if missing_args:
        raise ValueError(
            f"{fun.ref}.{fun.func.__name__} is missing required argument(s): {', '.join(missing_args)}"
        )

    if keywords:
        # The function accepts **kwargs, any non expected extra keyword
        # arguments will made available.
        for key, value in data.items():
            if key in expected_extra_kws:
                continue
            kwargs[key] = value

        # No need to check for extra keyword arguments since they are all
        # **kwargs now. Return
        return kwargs

    # Did not return yet? Lets gather any remaining and unexpected keyword
    # arguments
    extra = {}
    for key, value in data.items():
        if key in expected_extra_kws:
            continue
        extra[key] = copy.deepcopy(value)

    if extra:
        # Found unexpected keyword arguments, raise an error to the user
        if len(extra) == 1:
            msg = "'{0[0]}' is an invalid keyword argument for '{1}'".format(
                list(extra.keys()), f"{fun.__module__}.{fun.__name__}"
            )
        else:
            msg = "{} and '{}' are invalid keyword arguments for '{}'".format(
                ", ".join([f"'{e}'" for e in extra][:-1]),
                list(extra.keys())[-1],
                f"{fun.__module__}.{fun.__name__}",
            )
        warnings.warn(msg, RuntimeWarning)
        hub.log.warning(msg)
    return kwargs


def ishashable(hub, obj):
    """
    A simple test to verify if a given object is hashable and can therefore
    be used as a key in a dict
    """
    try:
        hash(obj)
    except TypeError:
        return False
    return True


def iter_high(hub, high):
    """
    Take a high-state structure and iterate over it yielding the elements down to the
    execution args
    Yields (id_, body, state, run, arg)
    """
    for id_, body in high.items():
        if not isinstance(body, dict):
            continue
        for state, run in body.items():
            if state.startswith("__"):
                continue
            for arg in run:
                yield id_, body, state, run, arg


def iter_high_leaf_args(hub, high):
    """
    Take a high-state structure and iterate over it yielding the elements down to the
    execution args
    Yields (id_, body, state, run, arg)
    """
    for id_, body in high.items():
        if not isinstance(body, dict):
            continue
        for state, run in body.items():
            if state.startswith("__"):
                continue
            for arg in run:
                yield from _iter_arg_chain(id_, body, state, run, "", arg)


def _iter_arg_chain(id_, body, state, run, arg_key_def, arg):
    if isinstance(arg, dict):
        for arg_key, arg_value in arg.items():
            # Escape dictionary references in the key definition to skip evaluating by arg_bind resolver.
            arg_key = arg_key.replace("[", "[\\")
            if arg_key_def:
                current_arg_key_def = arg_key_def + ":" + arg_key
            else:
                current_arg_key_def = arg_key

            if isinstance(arg_value, dict):
                yield from _iter_arg_chain(
                    id_, body, state, run, current_arg_key_def, arg_value
                )
            elif isinstance(arg_value, list):
                for index, arg_value_item in enumerate(arg_value):
                    yield from _iter_arg_chain(
                        id_,
                        body,
                        state,
                        run,
                        current_arg_key_def + f"[{index}]",
                        arg_value_item,
                    )
            else:
                yield id_, body, state, run, current_arg_key_def, arg_value
    elif isinstance(arg, list):
        for index, arg_value_item in enumerate(arg):
            yield from _iter_arg_chain(
                id_, body, state, run, arg_key_def + f"[{index}]", arg_value_item
            )
    else:
        yield id_, body, state, run, arg_key_def, arg


def get_enforced_state(hub, chunk, managed_state):
    tag = hub.idem.tools.gen_chunk_func_tag(chunk)
    esm_tag = hub.idem.tools.gen_chunk_esm_tag(chunk)
    new_chunk = {**chunk, "__id__": f"{chunk['__id__']}_create_new"}
    new_tag = hub.idem.tools.gen_chunk_func_tag(new_chunk)
    new_esm_tag = hub.idem.tools.gen_chunk_esm_tag(new_chunk)

    enforced_state = managed_state.get(new_esm_tag) or managed_state.get(new_tag)

    if not enforced_state:
        enforced_state = managed_state.get(esm_tag) or managed_state.get(tag)

    return enforced_state
