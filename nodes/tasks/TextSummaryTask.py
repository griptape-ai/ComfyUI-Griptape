from griptape.tasks import (
    TextSummaryTask,
)

from ..agent.agent import gtComfyAgent as Agent
from .BaseTask import gtUIBaseTask


class gtUITextSummaryTask(gtUIBaseTask):
    DESCRIPTION = "Summarize a text prompt."

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string)
        task = TextSummaryTask(prompt_text)
        # if deferred_evaluation:
        #     return ("Text Summary Task Created", agent, task)
        try:
            agent.add_task(TextSummaryTask(prompt_text))
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent, task)
