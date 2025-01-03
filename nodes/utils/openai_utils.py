from typing import Literal, get_args

from openai import OpenAI
from openai.types import AudioModel, ChatModel, EmbeddingModel, ImageModel
from openai.types.audio.speech_model import SpeechModel

from ...py.griptape_settings import GriptapeSettings

# Define the valid model types as a Literal
ModelTypes = Literal[
    "ChatModel", "AudioModel", "ImageModel", "EmbeddingModel", "SpeechModel"
]
API_KEY = "OPENAI_API_KEY"


def get_available_models(model_type: ModelTypes) -> list:
    """
    Retrieves a list of available models from the OpenAI API that match the specified model type.
    Args:
        model_type (type, optional): The type of model to filter by. Defaults to ChatModel.
    Returns:
        list: A list of models from the OpenAI API that match the specified model type.

    """
    # Map the Enum to the corresponding Literal
    model_type_map = {
        "ChatModel": ChatModel,
        "AudioModel": AudioModel,
        "ImageModel": ImageModel,
        "EmbeddingModel": EmbeddingModel,
        "SpeechModel": SpeechModel,
    }

    settings = GriptapeSettings()
    api_key = settings.get_settings_key_or_use_env(API_KEY)
    if api_key is None:
        return []

    # Get the predefined list of ChatModel IDs
    model_ids = get_args(model_type_map[model_type])
    try:
        client = OpenAI(api_key=api_key)
        # Filter available models to include only those matching ChatModel
        chat_model_ids = set(model_ids)
        available_models = client.models.list().data
        filtered_chat_models = [
            model.id for model in available_models if model.id in chat_model_ids
        ]

        return filtered_chat_models
    except Exception:
        print("Warning: Could not connect to OpenAI API - returning all models.")
        chat_model_ids = list(model_ids)
        return chat_model_ids
