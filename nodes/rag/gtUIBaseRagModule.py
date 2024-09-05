from griptape.engines.rag.modules import BaseRagModule


class gtUIBaseRagModule:
    """
    Griptape Base Rag Module
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
            "hidden": {},
        }

    RETURN_TYPES = ("MODULE_LIST",)
    RETURN_NAMES = ("MODULE",)
    FUNCTION = "create"

    CATEGORY = "Griptape/RAG"

    def ensure_dict(params):
        if isinstance(params, dict):
            return params
        elif isinstance(params, str):
            # Try to evaluate the string as a dictionary
            try:
                return eval(f"dict({params})")
            except Exception:
                # If evaluation fails, try to parse it as JSON
                import json

                try:
                    return json.loads(params)
                except json.JSONDecodeError:
                    # If JSON parsing fails, split by comma and colon
                    return dict(item.split(":") for item in params.split(","))
        elif params is None:
            return {}
        else:
            # If it's any other type, try to convert it to a dict
            try:
                return dict(params)
            except Exception:
                raise ValueError(f"Could not convert {type(params)} to dictionary")

    def create(self):
        return ([BaseRagModule()],)
