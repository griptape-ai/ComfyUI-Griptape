# from griptape.drivers import GriptapeCloudKnowledgeBaseVectorStoreDriver
from griptape.drivers import GriptapeCloudVectorStoreDriver

from .gtUIBaseVectorStoreDriver import gtUIBaseVectorStoreDriver

# Initialize environment variables
BASE_URL = "https://cloud.griptape.ai"
API_KEY_ENV = "GRIPTAPE_CLOUD_API_KEY"


class gtUIGriptapeCloudVectorStoreDriver(gtUIBaseVectorStoreDriver):
    DESCRIPTION = "Griptape Cloud Vector Store Driver: https://cloud.griptape.ai"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        del inputs["optional"]["embedding_driver"]
        inputs["required"].update()
        inputs["optional"].update(
            {
                "api_key_env_var": (
                    "STRING",
                    {"default": API_KEY_ENV},
                ),
                "base_url": ("STRING", {"default": BASE_URL}),
                "knowledge_base_id": ("STRING", {"default": "12345-abcde-1434"}),
            }
        )

        return inputs

    def create(self, **kwargs):
        api_key_env_var = kwargs.get("api_key_env_var", API_KEY_ENV)
        base_url = kwargs.get("base_url", BASE_URL)
        knowledge_base_id = kwargs.get("knowledge_base_id", "12345-abcde-1434")

        if api_key_env_var:
            api_key = self.getenv(api_key_env_var)

        params = {}

        if api_key:
            params["api_key"] = api_key
        if base_url:
            params["base_url"] = base_url
        if knowledge_base_id:
            params["knowledge_base_id"] = knowledge_base_id
        driver = GriptapeCloudVectorStoreDriver(**params)
        return (driver,)
