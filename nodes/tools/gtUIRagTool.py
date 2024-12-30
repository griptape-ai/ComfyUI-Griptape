from griptape.rules import Rule, Ruleset
from griptape.tools import RagTool

from .gtUIBaseTool import gtUIBaseTool


class gtUIRagTool(gtUIBaseTool):
    DESCRIPTION = "Griptape Rag Tool"

    @classmethod
    def INPUT_TYPES(cls):
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
                # "use_rules": (
                #     "BOOLEAN",
                #     {
                #         "default": True,
                #         "tooltip": "If enabled, will include helpful rules to sculpt the response of the agent to suit RAG.",
                #     },
                # ),
            },
        }

    RETURN_TYPES = (
        "TOOL_LIST",
        "RULESET",
    )
    RETURN_NAMES = (
        "TOOL",
        "RULES",
    )

    def create(self, **kwargs):
        description = kwargs.get("description", "Contains information.")
        off_prompt = kwargs.get("off_prompt", False)
        rag_engine = kwargs.get("rag_engine", None)
        # use_rules = kwargs.get("use_rules", True)

        tool_params = {}

        tool_params["description"] = description
        tool_params["off_prompt"] = off_prompt
        tool_params["rag_engine"] = rag_engine

        tool = RagTool(**tool_params)
        ruleset = Ruleset(
            name="GriptapeRagToolWithRules",
            rules=[
                Rule(
                    "Mandatory: Include all provided footnotes in your response, without exception."
                ),
                Rule("Use the RAG Tool to get answers to your questions."),
            ],
        )

        return ([tool], [ruleset])
