from typing import Literal, get_args

from openai import OpenAI
from openai.types import AudioModel, ChatModel, EmbeddingModel, ImageModel
from openai.types.audio.speech_model import SpeechModel

# Define the valid model types as a Literal
ModelTypes = Literal[
    "ChatModel", "AudioModel", "ImageModel", "EmbeddingModel", "SpeechModel"
]


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

    client = OpenAI()
    available_models = client.models.list().data

    # Get the predefined list of ChatModel IDs
    chat_model_ids = set(get_args(model_type_map[model_type]))

    # Filter available models to include only those matching ChatModel
    filtered_chat_models = [
        model.id for model in available_models if model.id in chat_model_ids
    ]

    return filtered_chat_models