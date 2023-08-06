from typing import List

SLS_RUN_SEPARATOR = ":sls:"

__IS_SLS_RUN__ = True

REQUISITES_TO_UPDATE_FOR_SLS_RUN = ["require", "require_in", "require_any", "listen"]


async def run(
    hub,
    ctx,
    name: str,
    sls_sources: List[str],
    params: List[str] = None,
    **kwargs,
):
    """
    State module to structure a group of SLS files into an independent construct that
    can be invoked from SLS code multiple times with different set of arguments and parameters

    Args:
        name(string):
            An idem name of the resource.

        sls_sources(list):
            List of sls files to run

        params(list, Optional):
            List of params files. All the params provided in these files will be consolidated and these consolidated params
            will override the params passed in Idem run. These consolidated params along with params passed to Idem run
            will be used to run the sls files provided in sls_sources. Defaults to None.

        kwargs(Dict[str, Any], Optional):
            parameters passed in kwargs are used as parameters to resolve parameters in sls_sources files.

        Request Syntax:
           .. code-block:: sls

              [sls-run-name]:
                sls.run:
                  - sls_sources:
                      - 'string'
                  - params:
                      - 'string'

        Returns:
            Dict[str, Any]

        Examples:
           .. code-block:: sls

               service4:
                sls.run:
                  - sls_sources:
                      - sls.service_file1
                      - sls.service_file2
                  - params:
                      - params.file1
    """

    result = dict(comment=[], name=name, old_state=None, new_state=None, result=True)

    # Name of the sls.run state if this state is inside another sls.run.
    # This parameter is used by idem execution internally to pass
    # current sls_run_id to the nested sls.run state executions
    sls_run_id = kwargs.get("sls_run_id", None)

    # The sls_sources and params provided to this state are paths to files.
    # To resolve the location of files and parse them we use this hub.OPT.idem.tree which gives us the base path.
    sls_sources_path = list()
    param_sources_path = list()
    if hub.OPT.idem.tree:
        tree = f"file://{hub.OPT.idem.tree}"
        hub.log.debug(f"Added tree to sls and param sources: {tree}")
        sls_sources_path.append(tree)
        param_sources_path.append(tree)

    main_run_name = ctx.run_name
    # Create a temporary run name to use while compiling the sls_sources passed to this state
    temporary_run_name = main_run_name + "." + name

    # Create a temporary run to process the new sls block
    await hub.idem.state.create(
        name=temporary_run_name,
        sls_sources=sls_sources_path,
        # Allow a different render pipe to be used for the new render block
        # Default to the renderer of the main run
        render=hub.idem.RUNS[main_run_name].get("render"),
        # Copy state.apply parameters from the main run
        **{
            k: hub.idem.RUNS[main_run_name].get(k)
            for k in (
                "runtime",
                "subs",
                "cache_dir",
                "test",
                "acct_file",
                "acct_key",
                "acct_profile",
                "acct_blob",
                "managed_state",
                "param_sources",
                "acct_data",
                "invert_state",
            )
        },
    )

    # Gather params files provided to this file and combine with idem run params
    # we gather params from idem run, params files provided to this state and inline params provided to this state.
    # will combine the params from all the three sources. If there are common params, Inline params takes precedence
    # followed by params files provided to this state.
    run_params_ret = await _gather_params(
        hub, main_run_name, temporary_run_name, params, param_sources_path, kwargs
    )
    if "errors" in run_params_ret:
        result["comment"] = [
            f"Error in gathering params files for sls.run {name}"
        ] + run_params_ret["errors"]
        result["result"] = False
        hub.idem.RUNS.pop(temporary_run_name, None)
        return result

    # parse the sls_sources provided to this state with the consolidated params and get high data
    src = hub.idem.sls_source.init.get_refs(sources=sls_sources_path, refs=sls_sources)

    # Resolve the new sls_sources with the main run
    gather_data = await hub.idem.resolve.init.gather(
        temporary_run_name,
        *src["sls"],
        sources=src["sls_sources"],
    )
    # Add the newly resolved blocks to the temporary run
    await hub.idem.sls_source.init.update(temporary_run_name, gather_data)

    if hub.idem.RUNS[temporary_run_name]["errors"]:
        result["comment"] = [
            f"Error in gathering sls_sources for sls.run {name}"
        ] + hub.idem.RUNS[temporary_run_name]["errors"]
        result["result"] = False
        hub.idem.RUNS.pop(temporary_run_name, None)
        return result

    # update the requisites in the high data of sls_sources passed to this state to include sls_run_id
    _update_requisites(hub, name, temporary_run_name, sls_run_id)

    # compile the high data to low data
    await hub.idem.state.compile(temporary_run_name)

    low_data = hub.idem.RUNS[temporary_run_name]["low"]

    sls_run_id = f"{sls_run_id}{SLS_RUN_SEPARATOR}{name}" if sls_run_id else name
    # Iterate over the states passed to this sls.run and add the extra attributes __sls_run_idm, sls_run_id
    # to identify these states from other states that are running in main idem run.
    for chunk in low_data:
        # sls_run_id is added to chunk to make requisite system understand this chunk is a part of sls.run
        chunk["sls_run_id"] = sls_run_id

        # sls_run_id is appended to __id__ of chunk to make this chunk unique as
        # different sls.run states can include same files
        chunk["__id__"] = f"{sls_run_id}:{chunk['__id__']}"

        # Add the low data gathered from sls_sources passed to this state to main run
        hub.idem.RUNS[main_run_name].get("add_low").append(chunk)

    result["new_state"] = {
        "Status": f"Added {len(low_data)} states to be run.",
        "is_sls_run": True,
    }
    hub.idem.RUNS.pop(temporary_run_name, None)
    return result


def is_pending(hub, ret):
    """
    Always skip reconciliation for sls.run because is_pending will be called for individual states
    """
    return False


# Utility methods to extract params and sls_sources passed to sls.run and update requisites


async def _gather_params(
    hub, main_run_name, temporary_run_name, params, param_sources_path, kwargs
):
    """Gather params passed to main Idem run, params files passed to the sls.run
       and inline parameters passed to sls.run
       will combine the params from all the three sources. If there are common params, Inline params takes precedence
       followed by params files provided to this state.

    Args:
        main_run_name(string):
            Name of the Idem run

        params(Dict[str, List[str]]):
            params sources and params files to get params from.

        param_sources_path(list):
            List of file paths of provided params

        kwargs(Dict[str, Any]):
            Inline params provided to the sls.run
    """
    run_params = {}
    # params given during Idem main run.
    run_params.update(hub.idem.RUNS[main_run_name]["params"] or {})

    # parse params files provide to this state.
    if params:
        params = hub.idem.sls_source.param.get_refs(
            sources=param_sources_path, refs=params
        )
        resolved_params_ret = await _gather_params_from_included_files(
            hub, temporary_run_name, params
        )
        if not resolved_params_ret or "errors" in resolved_params_ret:
            return {"errors": resolved_params_ret["errors"]}
        # combining the params provided to this file and idem run params.
        # if there is overlapping of params, params provided to this file will take precedence over idem run params.
        if "params" in resolved_params_ret:
            run_params.update(resolved_params_ret["params"])

    # update the params with inline params if provided.
    if kwargs:
        run_params.update(kwargs)
    hub.idem.RUNS[temporary_run_name]["params"] = run_params
    return {"params": run_params}


async def _gather_params_from_included_files(hub, temporary_run_name, params):
    """Gather parameters from the params files.

    Args:
        main_run_name(string):
            Name of the Idem run

        params(Dict[str, List[str]]):
            params sources and params files to get params from.
    """

    param_sources = params["param_sources"]
    params = params["params"]
    gather_data = await hub.idem.resolve.init.gather(
        temporary_run_name, *params, sources=param_sources
    )
    if gather_data["errors"]:
        return {"errors": gather_data["errors"]}
    hub.idem.sls_source.param.process_params(temporary_run_name, gather_data)

    return {"params": hub.idem.RUNS[temporary_run_name]["params"]}


def _update_requisites(hub, name, run_name, sls_run_id=None):
    _format_argument_binding(hub, name, run_name, sls_run_id)
    _format_require(hub, name, run_name, sls_run_id)


def _format_argument_binding(hub, name, run_name, sls_run_id=None):
    """Update argument binding requisite in the high data with the sls.run name
    Args:
        name(string):
            An Idem name of sls.run state

        run_name(string):
            Name of current sls.run combined with idem run name. <idem_run_name>.<sls_run_id>

        sls_run_id(string, Optional):
            Name of the sls.run state that this state is part of. If this sls.run is nested inside another sls.run
            sls_run_id is name of the parent sls.run state.

    """

    high_data = hub.idem.RUNS[run_name]["high"]
    # Iterate through high data leaf arguments
    for id_, body, state, run, arg_key, arg_value in hub.idem.tools.iter_high_leaf_args(
        high_data
    ):
        if (
            arg_value
            and isinstance(arg_value, str)
            and hub.idem.ccomps.arg_bind.ARG_REFERENCE_REGEX_PATTERN.search(arg_value)
        ):
            # checking for argument binding syntax
            for arg_ref in hub.idem.ccomps.arg_bind.ARG_REFERENCE_REGEX_PATTERN.findall(
                arg_value
            ):
                state_name = arg_ref.split(":")[1]
                # check the referred state is present in this sls.run
                # If it's present, update the argument binding by adding sls:<sls.run_name> prefix
                # This ensures we are referring correct state when we add this data to Idem run
                if state_name in high_data:
                    updated_arg_binding = arg_ref.replace(
                        "${",
                        f"${{sls:{(sls_run_id + SLS_RUN_SEPARATOR) if sls_run_id else ''}{name}:",
                    )
                    _replace_arg_bind_in_high_data(
                        hub,
                        high_data.get(id_).get(state),
                        arg_key,
                        arg_ref,
                        updated_arg_binding,
                    )
    hub.idem.RUNS[run_name]["high"] = high_data


def _format_require(hub, name, run_name, sls_run_id=None):
    """Update require requisite in the high data with the sls.run name
    Args:
        name(string):
            An Idem name of sls.run state

        run_name(string):
            Name of current sls.run combined with idem run name. <idem_run_name>.<sls_run_id>

        sls_run_id(string, Optional):
            Name of the sls.run state that this state is part of. If this sls.run is nested inside another sls.run
            sls_run_id is name of the parent sls.run state.

    """
    high_data = hub.idem.RUNS[run_name]["high"]
    for id_, body in high_data.items():
        if id_.startswith("__"):
            continue
        for state in body:
            if state.startswith("__"):
                continue
            for arg in body[state]:
                # update require requisite key to include sls run name.
                if isinstance(arg, dict):
                    for attribute_key, attribute_val in arg.items():
                        if attribute_key in REQUISITES_TO_UPDATE_FOR_SLS_RUN:
                            updated_require_requisites = []
                            for require_state in attribute_val:
                                require_arg_key = next(iter(require_state))
                                require_arg_value = require_state[require_arg_key]
                                updated_require_requisites.append(
                                    _prepare_sls_run_require_requisite(
                                        name,
                                        require_arg_key,
                                        require_arg_value,
                                        sls_run_id,
                                    )
                                )
                            arg[attribute_key] = updated_require_requisites
    hub.idem.RUNS[run_name]["high"] = high_data


def _replace_arg_bind_in_high_data(
    hub, high_data_resource, arg_key, arg_value, arg_value_to_replace
):
    """Replace the value in high data"""
    key_arr = arg_key.split(":")
    referred_key = key_arr.pop(0)
    key_to_parse, indexes = hub.tool.idem.arg_bind_utils.parse_index(referred_key)
    for index, resource_state in enumerate(high_data_resource):
        name_def = next(iter(resource_state))
        if key_to_parse == name_def:
            hub.idem.rules.arg_resolver.set_chunk_arg_value(
                resource_state,
                arg_value,
                arg_key.split(":"),
                arg_value_to_replace,
                None,
            )


def _prepare_sls_run_require_requisite(
    name, require_arg_key, require_arg_value, sls_run_id
):
    """
    modify require requisite to include sls.run name so that we point out the exact required resource
    This modification ensures that we require the resource in this sls.run only

    Example-:
        In the resources inside this sls.run, user will add require requisite like this

        state1:
         cloud1.state_def:
          - require:
             - cloud2: state2

        This same state "state1" and "state2" might be part of more than one sls.run. so to identify which exact state
        to require we need to add the sls.run name.

        Modified state:

            state1:
             cloud1.state_def:
              - require:
                 - sls: <sls.run.name>
                    - cloud2: state2

        If we have nested sls.runs, then sls_run_id is passed.
        Example-:

        state3 is a sls.run which contains state4 and state3 is part of State1 sls.run

        state4:
          test.present:
            - require:
                - test: test_include_sls_run_3

        This will be modified as

        state4:
          test.present:
            - require:
                - sls: state1
                    - sls: state3
                        - test: test_include_sls_run_3


    """
    require_sls_requisite = {}
    current_obj = [{require_arg_key: require_arg_value}]
    if sls_run_id:
        # If it's a nested sls.run we split the sls_run_id and add require requisites in hierarchy
        sls_run_states = sls_run_id.split(SLS_RUN_SEPARATOR)
        # Adding the current or innermost sls.run name
        sls_run_states.append(name)
        # loop through in reverse order since inner sls.run should be added first
        for sls_run_state in reversed(sls_run_states):
            current_obj = [{"sls": [{sls_run_state: current_obj}]}]
        # we need to output a dictionary so sending the first element of array
        # as array will always contain only one element
        return current_obj[0]
    else:
        require_sls_requisite["sls"] = [{name: current_obj}]
        return require_sls_requisite
