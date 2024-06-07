import os

import requests
from griptape.tools import (
    Calculator,
    DateTime,
    FileManager,
    GriptapeCloudKnowledgeBaseClient,
    WebScraper,
)

from ..py.griptape_config import get_config
from .base_tool import gtUIBaseTool
from .duckduckgo_client import DuckDuckGoTool


class gtUIFileManager(gtUIBaseTool):
    """
    The Griptape File Manager Tool
    """

    @classmethod
    def INPUT_TYPES(s):
        workdir = os.getenv("HOME")
        return {
            "required": {"off_prompt": ("BOOLEAN", {"default": True})},
            "optional": {"workdir": ("STRING", {"default": f"{workdir}"})},
        }

    def create(self, off_prompt, workdir=""):
        tool = FileManager(off_prompt=off_prompt, workdir=workdir)
        return ([tool],)


class gtUICalculator(gtUIBaseTool):
    """
    The Griptape Calculator Tool
    """

    def create(self, off_prompt):
        tool = Calculator(off_prompt=off_prompt)
        return ([tool],)


class gtUIWebSearch(gtUIBaseTool):
    """
    The Griptape Web Search Tool
    """

    def create(self, off_prompt):
        tool = DuckDuckGoTool(
            off_prompt=off_prompt,
        )
        return ([tool],)


# class gtUIImageQueryClient(gtUIBaseTool):
#     """
#     The Griptape Image Query Tool
#     """

#     def create(self, off_prompt):
#         tool = ImageQueryClient(off_prompt=off_prompt)
#         return ([tool],)


class gtUIWebScraper(gtUIBaseTool):
    """
    The Griptape WebScraper Tool
    """

    def create(self, off_prompt):
        tool = WebScraper(
            off_prompt=off_prompt,
        )
        return ([tool],)


class gtUIDateTime(gtUIBaseTool):
    """
    The Griptape DateTime Tool
    """

    def create(self, off_prompt):
        tool = DateTime(off_prompt=off_prompt)
        return ([tool],)


class gtUIKnowledgeBaseTool(gtUIBaseTool):
    """
    The Griptape Knowledge Base Tool
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "off_prompt": ("BOOLEAN", {"default": False}),
                "api_key_environment_variable": (
                    "STRING",
                    {"default": "GRIPTAPE_API_KEY"},
                ),
                "base_url": ("STRING", {"default": "https://cloud.griptape.ai"}),
                "knowledge_base_id": ("STRING", {"default": ""}),
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
        api_key = get_config(f"env.{api_key_environment_variable}")

        # Use the Griptape API to grab the name and description of the knowledge base
        data = self.getKnowledgeBaseInfo(api_key, base_url, knowledge_base_id)
        name = data.get("name", "Griptape Knowledge Base")
        description = data.get("description", "Contains helpful information")

        tool = GriptapeCloudKnowledgeBaseClient(
            name=name,
            description=description,
            off_prompt=off_prompt,
            api_key=api_key,
            base_url=base_url,
            knowledge_base_id=knowledge_base_id,
        )
        return ([tool],)
