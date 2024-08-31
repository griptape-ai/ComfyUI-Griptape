from griptape.tools import RagTool

from .gtUIBaseTool import gtUIBaseTool


class gtUIRagTool(gtUIBaseTool):
    DESCRIPTION = "Griptape Rag Tool"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "description": (
                    "STRING",
                    {
                        "default": "Contains information about...",
                        "tooltip": "Description of the type of information you're querying for.",
                    },
                ),
                "rag_engine": (
                    "RAG_ENGINE",
                    {"tooltip": "Rag Engine used for the tool."},
                ),
            },
        }

    CATEGORY = "Griptape/RAG"

    def create(self, **kwargs):
        description = kwargs.get("description", "Contains information.")
        off_prompt = kwargs.get("off_prompt", False)
        rag_engine = kwargs.get("rag_engine", None)

        tool_params = {}

        tool_params["description"] = description
        tool_params["off_prompt"] = off_prompt
        tool_params["rag_engine"] = rag_engine

        tool = RagTool(**tool_params)
        return ([tool],)
