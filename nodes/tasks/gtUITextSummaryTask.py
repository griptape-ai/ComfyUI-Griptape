from typing import Any, Tuple

from griptape.tasks import (
    TextSummaryTask,
)

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask


class gtUITextSummaryTask(gtUIBaseTask):
    DESCRIPTION = "Summarize a text prompt."
    CATEGORY = "Griptape/Text"

    def run(self, **kwargs) -> Tuple[Any, ...]:
        STRING = kwargs.get("STRING")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)

        if not agent:
            agent = Agent()
        prompt_text = self.get_prompt_text(STRING, input_string)
        task = TextSummaryTask(
            prompt_text,
            context=self.get_context_as_dict(kwargs.get("key_value_replacement", None)),
        )
        # if deferred_evaluation:
        #     return ("Text Summary Task Created", agent, task)
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)
        result = agent.run()
        return (result.output_task.output.value, agent, task)
