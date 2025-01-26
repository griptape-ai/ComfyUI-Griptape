import ast
from typing import Any, Tuple

from griptape.engines.rag.modules import BaseRagModule


class gtUIBaseRagModule:
    """
    Griptape Base Rag Module
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {},
            "hidden": {},
        }

    RETURN_TYPES = ("MODULE_LIST",)
    RETURN_NAMES = ("MODULE",)
    FUNCTION = "create"

    CATEGORY = "Griptape/RAG"

    def ensure_dict(self, params):
        if isinstance(params, dict):
            return params
        elif isinstance(params, str):
            # Try to evaluate the string as a dictionary
            try:
                # Convert string to AST
                tree = ast.literal_eval(f"dict({params})")
                return tree
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

    def create(self) -> Tuple[Any, ...]:
        return ([BaseRagModule()],)
