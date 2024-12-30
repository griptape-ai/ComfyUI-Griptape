from griptape.engines import CsvExtractionEngine, JsonExtractionEngine
from griptape.tasks import ExtractionTask

from ..agent.gtComfyAgent import gtComfyAgent as Agent
from .gtUIBaseTask import gtUIBaseTask

extraction_engines = ["csv", "json"]


class gtUIExtractionTask(gtUIBaseTask):
    """
    The Griptape Text Extraction Task
    """

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "extraction_type": (
                    extraction_engines,
                    {
                        "default": "json",
                        "tooltip": "The type of extraction to perform.",
                    },
                ),
                "column_names": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Comma separated list of column names to extract. Example:\n name, age",
                    },
                ),
                "template_schema": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": 'Schema template for the json extraction. Example:\n {"name": str, "age": int}',
                    },
                ),
            }
        )
        del inputs["required"]["STRING"]
        inputs["optional"].update(
            {
                "STRING": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Text to extract from. If you are also providing an input_string, this will be added before that.",
                    },
                ),
            }
        )
        return inputs

    DESCRIPTION = "Extract text using csv or json."
    CATEGORY = "Griptape/Text"

    def run(self, **kwargs):
        STRING = kwargs.get("STRING")
        input_string = kwargs.get("input_string", None)
        agent = kwargs.get("agent", None)
        extraction_type = kwargs.get("extraction_type", "json")
        column_names_string = kwargs.get("column_names", "")
        column_names = [
            column_name.strip() for column_name in column_names_string.split(",")
        ]
        template_schema = kwargs.get("template_schema", "")
        engine = None
        output = None
        if not agent:
            agent = Agent()
        prompt_driver = agent.drivers_config.prompt_driver
        if extraction_type == "csv":
            print("CSV Extraction")
            print(column_names)
            engine = CsvExtractionEngine(
                prompt_driver=prompt_driver, column_names=column_names
            )
        elif extraction_type == "json":
            engine = JsonExtractionEngine(
                prompt_driver=prompt_driver, template_schema=template_schema
            )

        prompt_text = self.get_prompt_text(STRING, input_string)

        task = ExtractionTask(extraction_engine=engine)  # type: ignore[reportArgumentType]
        try:
            agent.add_task(task)
        except Exception as e:
            print(e)
        result = agent.run(prompt_text)
        artifacts = result.output_task.output.value
        if extraction_type == "csv":
            output = [artifact.value.split("\n") for artifact in artifacts]
        elif extraction_type == "json":
            output = [artifact.value for artifact in artifacts]
        return (
            output,
            agent,
        )
