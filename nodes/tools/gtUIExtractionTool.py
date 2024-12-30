from griptape.drivers import OpenAiChatPromptDriver
from griptape.engines import CsvExtractionEngine, JsonExtractionEngine
from griptape.rules import Rule
from griptape.tools import ExtractionTool

from .gtUIBaseTool import gtUIBaseTool

extraction_engines = ["csv", "json"]


class gtUIExtractionTool(gtUIBaseTool):
    """
    The Griptape Text Extraction Tool
    """

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()

        inputs["optional"].update(
            {
                "prompt_driver": ("PROMPT_DRIVER", {}),
                "extraction_type": (extraction_engines, {"default": "json"}),
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
        del inputs["required"]["off_prompt"]

        return inputs

    DESCRIPTION = (
        "Prompt Summary Tool - Summarizes information that is found in Task Memory."
    )

    def create(self, **kwargs):
        prompt_driver = kwargs.get("prompt_driver", None)
        extraction_type = kwargs.get("extraction_type", "json")
        column_names_string = kwargs.get("column_names", "")
        column_names = [column_name.strip() for column_name in column_names_string]
        template_schema = kwargs.get("template_schema", "")
        engine = None
        params = {}

        if not prompt_driver:
            prompt_driver = OpenAiChatPromptDriver(model="gpt-4o-mini")
        if extraction_type == "csv":
            engine = CsvExtractionEngine(
                prompt_driver=prompt_driver, column_names=column_names
            )
        elif extraction_type == "json":
            engine = JsonExtractionEngine(
                prompt_driver=prompt_driver, template_schema=template_schema
            )

        params["extraction_engine"] = engine
        tool = ExtractionTool(**params, rules=[Rule("Raw output please")])
        return ([tool],)
