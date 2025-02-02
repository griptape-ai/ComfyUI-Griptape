class ContainsAnyDict(dict):
    def __contains__(self, key):
        return True


from griptape.structures import Agent

default_agent_response = "Summarize the incoming data for me."


class gtUIChat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "text": (
                    "STRING",
                    {
                        "forceInput": True,
                        "tooltip": "Something to inspect",
                    },
                ),
                "user_message_comment": (
                    "STRING",
                    {"default": "User Message"},
                ),
                "user_message_body": (
                    "STRING",
                    {
                        "default": "Chat with the LLM here. Hit <shift>+<return> or <shift>+<Enter> to send the message.",
                    },
                ),
                "user_message": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "Type whatever you want to talk to the LLM.\nHit <shift>+<return> or <shift>+<Enter> to send the message.",
                        "placeholder": "Type here...",
                    },
                ),
                "agent_response_comment": (
                    "STRING",
                    {"default": "Agent Response"},
                ),
                "agent_response_body": (
                    "STRING",
                    {
                        "default": "The LLM's response will appear here. When you execute the node, this text will be used for downstream evaluation.",
                    },
                ),
                "agent_response": (
                    "MARKDOWN",
                    {
                        "multiline": True,
                        "tooltip": "response from the LLM",
                        "placeholder": "Any response from the LLM will appear here.\nThis is the text that will be used for the next prompt.",
                        "default": default_agent_response,
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    CATEGORY = "Griptape/Chat"
    FUNCTION = "run"

    def run(self, *args, **kwargs):
        agent = Agent(stream=True)
        input_text = kwargs.get("text", "")
        agent_response = kwargs.get("agent_response", default_agent_response)
        if agent_response.strip() == "":
            agent_response = default_agent_response
        response = agent.run((agent_response, input_text))
        return (response.output,)
