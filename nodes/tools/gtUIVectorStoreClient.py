import ast
import json

from griptape.drivers import DummyVectorStoreDriver
from griptape.tools import VectorStoreClient

from .gtUIBaseTool import gtUIBaseTool


class gtUIVectorStoreClient(gtUIBaseTool):
    """
    The Griptape VectorStoreClient Tool
    """

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["required"].update(
            {
                "vector_store_driver": ("VECTOR_STORE_DRIVER", {"default": None}),
                "description": (
                    "STRING",
                    {"default": "This DB has information about...", "multiline": False},
                ),
                "optional_query_params": (
                    "STRING",
                    {"default": "{}", "multiline": False},
                ),
            }
        )
        inputs["hidden"].update({"prompt": "PROMPT"})
        return inputs

    DESCRIPTION = "Use the Vector Store to get information."

    def string_to_dict(self, s):
        s = s.strip()

        # Try JSON format first
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            pass

        # Try literal eval (for dict-like strings)
        try:
            return ast.literal_eval(s)
        except (ValueError, SyntaxError):
            pass

        # Try key-value pair format
        if ":" in s:
            return dict(
                map(str.strip, item.split(":", 1))
                for item in s.split("\n")
                if ":" in item
            )

        # If all else fails, return an empty dict
        return {}

    def create(self, **kwargs):
        off_prompt = kwargs.get("off_prompt", False)
        query_params = kwargs.get("optional_query_params", "{}")
        description = kwargs.get("description", "This DB has information about...")
        vector_store_driver = kwargs.get(
            "vector_store_driver", DummyVectorStoreDriver()
        )
        params = {}
        params["off_prompt"] = off_prompt
        if query_params or query_params.strip() == "{}":
            params["query_params"] = self.string_to_dict(query_params)
        if description:
            params["description"] = description
        if vector_store_driver:
            params["vector_store_driver"] = vector_store_driver

        tool = VectorStoreClient(**params)
        return ([tool],)
