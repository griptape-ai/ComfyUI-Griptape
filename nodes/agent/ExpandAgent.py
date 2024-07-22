class ExpandAgent:
    DESCRIPTION = "Expand the components of a Griptape Agent."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "agent": (
                    "AGENT",
                    {
                        "forceInput": True,
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "AGENT",
        "CONFIG",
        "RULESET",
        "TOOL_LIST",
        "MEMORY",
    )
    RETURN_NAMES = (
        "AGENT",
        "CONFIG",
        "RULESETS",
        "TOOLS",
        "MEMORY",
    )

    FUNCTION = "expand"

    CATEGORY = "Griptape/Agent"
    OUTPUT_NODE = True

    def expand(self, agent):
        rulesets = agent.rulesets
        tools = agent.tools
        conversation_memory = agent.conversation_memory
        config = agent.config
        return (
            agent,
            config,
            rulesets,
            tools,
            conversation_memory,
        )
