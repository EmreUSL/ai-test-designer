def infer_action(ui_element):
    semantic = ui_element.semantic
    tag = ui_element.tag

    if semantic in ["USERNAME", "PASSWORD"]:
        return "SEND_KEYS"

    if semantic == "SUBMIT":
        return "CLICK"

    if tag in ["a", "button"]:
        return "CLICK"

    return "NONE"
