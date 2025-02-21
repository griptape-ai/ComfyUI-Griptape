from server import PromptServer


class ContainsAnyDict(dict):
    def __contains__(self, key):
        return True


default_agent_response = "Summarize the incoming data for me."


class gtUIChat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "agent": ("AGENT",),
                "text_context": (
                    "STRING",
                    {
                        "forceInput": True,
                        "multiline": True,
                        "tooltip": "Something to inspect",
                    },
                ),
                "user_message_comment": (
                    "STRING",
                    {"default": "Collaborate with an Agent"},
                ),
                "user_message_body": (
                    "STRING",
                    {
                        "default": "Hit <SHIFT>+<ENTER> to talk to the Agent. Connect nodes to provide context.",
                    },
                ),
                "user_message": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "Type whatever you want to talk to the LLM.\nHit <shift>+<return> or <shift>+<Enter> to send the message.",
                        "placeholder": "Type here and hit <shift>+<enter> to send the message.",
                    },
                ),
                "agent_response": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "Response from the Agent",
                        "placeholder": "Responses from the Agent will appear here.",
                    },
                ),
                "agent_output_comment": (
                    "STRING",
                    {"default": "Output"},
                ),
                # "agent_output_body": (
                #     "STRING",
                #     {
                #         "default": "The output that will be used when the workflow is run.",
                #     },
                # ),
                "output_selector": (
                    "INT",
                    {
                        "default": 0,
                        "tooltip": "Select the output to use.",
                        "min": 0,
                    },
                ),
                "agent_output": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "This will be output that will go from the LLM.",
                        "placeholder": "The Agent's suggested prompt will appear here. Iterate together on it, and hit Queue when you're ready to send it on.",
                    },
                ),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    CATEGORY = "Griptape/Chat"
    FUNCTION = "run"
    OUTPUT_NODE = True

    def run(self, *args, **kwargs):
        agent = kwargs.get("agent", None)
        text_context = kwargs.get("text_context", "")
        unique_id = kwargs.get("unique_id", {})
        if not agent:
            agent_dict = {}
        else:
            agent_dict = agent.to_dict()

        PromptServer.instance.send_sync(
            "griptape.chat_node",
            {
                "text_context": text_context,
                "agent": agent_dict,
                "id": unique_id,
            },
        )

        agent_output = kwargs.get("agent_output", default_agent_response)
        return {
            "ui": {
                "text_context": text_context,
                "agent": agent_dict,
            },
            "result": (agent_output,),
        }
