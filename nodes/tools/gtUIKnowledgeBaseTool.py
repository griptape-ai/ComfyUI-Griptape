import requests
from griptape.tools import (
    GriptapeCloudKnowledgeBaseTool,
)

from ...py.griptape_settings import GriptapeSettings
from ..utilities import to_pascal_case
from .gtUIBaseTool import gtUIBaseTool


class gtUIKnowledgeBaseTool(gtUIBaseTool):
    """
    The Griptape Knowledge Base Tool
    """

    DESCRIPTION = "Access a Griptape Cloud Knowledge Base. Learn more at https://cloud.griptape.ai"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "off_prompt": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "label_on": "True (Keep output private)",
                        "label_off": "False (Provide output to LLM)",
                    },
                ),
                "api_key_environment_variable": (
                    "STRING",
                    {"default": "GRIPTAPE_CLOUD_API_KEY"},
                ),
                "base_url": ("STRING", {"default": "https://cloud.griptape.ai"}),
                "knowledge_base_id": ("STRING", {"default": "12345-abcde-1434"}),
            },
        }

    def getKnowledgeBaseInfo(self, api_key, base_url, knowledge_base_id):
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        try:
            response = requests.get(
                f"{base_url}/api/knowledge-bases/{knowledge_base_id}", headers=headers
            )
        except requests.exceptions.RequestException as e:
            print(e)
            return
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data
        else:
            print(f"Failed to get knowledge base info: {response.status_code}")

    def create(
        self,
        off_prompt,
        api_key_environment_variable,
        base_url,
        knowledge_base_id,
    ):
        settings = GriptapeSettings()

        api_key = settings.get_settings_key_or_use_env(api_key_environment_variable)

        # Use the Griptape API to grab the name and description of the knowledge base
        data = self.getKnowledgeBaseInfo(api_key, base_url, knowledge_base_id)
        name = data.get("name", "Griptape Knowledge Base")
        description = data.get("description", "Contains helpful information")

        name = to_pascal_case(name)

        tool = GriptapeCloudKnowledgeBaseTool(
            name=name,
            description=description,
            off_prompt=off_prompt,
            api_key=api_key,
            base_url=base_url,
            knowledge_base_id=knowledge_base_id,
        )
        return ([tool],)
