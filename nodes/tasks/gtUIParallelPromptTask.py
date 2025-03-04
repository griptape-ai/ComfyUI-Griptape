from griptape.artifacts import TextArtifact
from griptape.drivers import LocalStructureRunDriver
from griptape.structures import Workflow
from griptape.tasks import StructureRunTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask


class gtUIParallelPromptTask(gtUIBaseTask):
    DESCRIPTION = "Create a parallel prompt task for an agent."
    CATEGORY = "Griptape/Agent"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        # Update optional inputs to include 'agent' and adjust others as necessary
        inputs["optional"].update(
            {
                "agent": ("AGENT",),
                "string_list": ("STRING_LIST",),
            }
        )
        return inputs

    def run(self, **kwargs):
        string_list = kwargs.get("string_list")
        agent = kwargs.get("agent", None)

        # if the tool is provided, keep going
        if not agent:
            agent = Agent()
        driver = LocalStructureRunDriver(create_structure=lambda: agent)

        workflow = Workflow()

        for prompt in string_list:
            task = StructureRunTask(prompt, structure_run_driver=driver)
            workflow.add_task(task)
        result = workflow.run()
        outputs = "\n\n".join([task.output.value for task in result.output_tasks])
        return (outputs, agent)
        output = result.output_task.output.value
        if isinstance(output, str):
            return (output, agent)
        elif isinstance(output, list):
            output_list = [item.value for item in output]
            output_str = "\n\n".join(output_list)
            return (output_str, agent)
        elif isinstance(output, TextArtifact):
            return (output.value, agent)
