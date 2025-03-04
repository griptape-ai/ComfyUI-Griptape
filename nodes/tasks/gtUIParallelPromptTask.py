from griptape.structures import Workflow
from griptape.tasks import PromptTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class gtUIParallelPromptTask:
    DESCRIPTION = "Create a parallel prompt task for an agent."
    CATEGORY = "Griptape/Agent"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "agent": (
                    "AGENT",
                    {
                        "tooltip": "The agent to use for the task.",
                    },
                ),
                "string_list": (
                    "STRING_LIST",
                    {
                        "tooltip": "A list of prompts to send to the agent.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)

    FUNCTION = "run"

    def run(self, **kwargs):
        string_list = kwargs.get("string_list")
        agent = kwargs.get("agent", None)

        # if the tool is provided, keep going
        if not agent:
            agent = Agent()
        agent_task_dict = agent.task.to_dict()
        agent_dict = agent.to_dict()
        agent_prompt_driver_dict = agent_dict["tasks"][0]["prompt_driver"]
        agent_task_dict["prompt_driver"] = agent_prompt_driver_dict
        agent_dict_rulesets = agent_dict["rulesets"]
        for ruleset in agent_dict_rulesets:
            if ruleset:
                agent_task_dict["rulesets"].append(ruleset)

        workflow = Workflow()
        for x, prompt in enumerate(string_list):
            agent_task_dict["input"] = prompt
            agent_task_dict["id"] = f"input_{str(x)}"
            task = PromptTask().from_dict(agent_task_dict)
            workflow.add_task(task)
        result = workflow.run()
        outputs = ""
        for x, output in enumerate(result.output_tasks):
            outputs += f"### input_{x + 1}:\n----\n{output.output.value}\n\n"
        return (outputs,)
