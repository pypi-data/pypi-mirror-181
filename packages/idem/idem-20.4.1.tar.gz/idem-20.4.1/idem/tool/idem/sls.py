def is_state_has_sls_run(hub, chunk):
    """
    Determine the state referred by chunk has flag __IS_SLS_RUN__ True
    """
    try:
        return getattr(hub.states[chunk["state"]], "__IS_SLS_RUN__")
    except Exception:
        return False
