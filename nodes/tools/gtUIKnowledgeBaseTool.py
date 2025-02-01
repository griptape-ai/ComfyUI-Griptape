from typing import List, cast

import requests
from griptape.drivers import GriptapeCloudVectorStoreDriver
from griptape.engines.rag import RagEngine
from griptape.engines.rag.modules import (
    BaseRetrievalRagModule,
    PromptResponseRagModule,
    VectorStoreRetrievalRagModule,
)
from griptape.engines.rag.stages import (
    ResponseRagStage,
    RetrievalRagStage,
)
from griptape.tools import RagTool

from ...py.griptape_settings import GriptapeSettings
from ..utilities import to_pascal_case
from .gtUIBaseTool import gtUIBaseTool


class gtUIKnowledgeBaseTool(gtUIBaseTool):
    """
    The Griptape Knowledge Base Tool
    """

    DESCRIPTION = "Access a Griptape Cloud Knowledge Base. Learn more at https://cloud.griptape.ai"

    @classmethod
    def INPUT_TYPES(cls):
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
                    {"default": "GT_CLOUD_API_KEY"},
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

    def create(self, **kwargs):
        off_prompt = kwargs.get("off_prompt", False)
        api_key_environment_variable = kwargs.get(
            "api_key_environment_variable", "GT_CLOUD_API_KEY"
        )
        base_url = kwargs.get("base_url", "https://cloud.griptape.ai")
        knowledge_base_id = kwargs.get("knowledge_base_id", "12345-abcde-1434")

        settings = GriptapeSettings()

        api_key = settings.get_settings_key_or_use_env(api_key_environment_variable)
        if api_key is None:
            api_key = ""
        # Use the Griptape API to grab the name and description of the knowledge base
        data = self.getKnowledgeBaseInfo(api_key, base_url, knowledge_base_id)
        name = data.get("name", "Griptape Knowledge Base")  # type: ignore[reportOptionalMemberAccess]
        description = data.get("description", "Contains helpful information")  # type: ignore[reportOptionalMemberAccess]

        name = to_pascal_case(name)
        retrieval_modules: List[BaseRetrievalRagModule] = cast(
            List[BaseRetrievalRagModule],
            [
                VectorStoreRetrievalRagModule(
                    vector_store_driver=GriptapeCloudVectorStoreDriver(
                        api_key=api_key,
                        base_url=base_url,
                        knowledge_base_id=knowledge_base_id,
                    )
                )
            ],
        )

        engine = RagEngine(
            retrieval_stage=RetrievalRagStage(retrieval_modules=retrieval_modules),
            response_stage=ResponseRagStage(
                response_modules=[
                    PromptResponseRagModule(),
                ]
            ),
        )
        tool = RagTool(
            description=description, rag_engine=engine, off_prompt=off_prompt
        )
        # tool = GriptapeCloudKnowledgeBaseTool(
        #     name=name,
        #     description=description,
        #     off_prompt=off_prompt,
        #     api_key=api_key,
        #     base_url=base_url,
        #     knowledge_base_id=knowledge_base_id,
        # )
        return ([tool],)
