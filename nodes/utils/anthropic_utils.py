from typing import Literal, get_args

from anthropic.types.model_param import ModelParam

# Define the valid model types as a Literal
ModelTypes = Literal["ModelParam"]


def get_available_models(model_type: ModelTypes) -> list:
    """
    Retrieves a list of available models from the Anthropic API that match the specified model type.
    Args:
        model_type (type, optional): The type of model to filter by. Defaults to ChatModel.
    Returns:
        list: A list of models from the Anthropic API that match the specified model type.

    """
    # Map the Enum to the corresponding Literal
    model_type_map = {
        "ModelParam": ModelParam,
    }

    # Get the predefined list of model IDs for the selected model type
    model_literal = model_type_map[model_type]

    # Extract the Literal from the Union
    # The Literal is typically the second argument in the Union
    literal_values = get_args(get_args(model_literal)[1])

    return list(literal_values)
