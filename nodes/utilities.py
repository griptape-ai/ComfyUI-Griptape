import base64
from io import BytesIO

import numpy as np
import requests
import torch
from jinja2 import Template
from PIL import Image, ImageOps, ImageSequence


def get_lmstudio_models(port="1234") -> list[str]:
    url = f"http://127.0.0.1:{port}/v1/models"

    try:
        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Failed to fetch models: {response.status_code}")

        # Parse the JSON response
        models_info = response.json()

        # Extract the model names
        models = [model["id"] for model in models_info["data"]]

        return models
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.RequestException,
        KeyError,
    ):
        # Return an empty list if there is any error
        return []


def get_ollama_models() -> list[str]:
    # URL to fetch the local models
    url = "http://127.0.0.1:11434/api/tags"

    try:
        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Failed to fetch models: {response.status_code}")

        # Parse the JSON response
        models_info = response.json()

        # Extract the model names
        # models = [model["name"].split(":")[0] for model in models_info["models"]]
        models = [model["name"] for model in models_info["models"]]

        return models
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.RequestException,
        KeyError,
    ):
        # Return an empty list if there is any error
        return []


def get_prompt_text(string_prompt, input_string):
    template = Template(string_prompt)
    return template.render(input_string=input_string)


def image_path_to_output(image_path):
    img = Image.open(image_path)
    output_images = []
    output_masks = []
    for i in ImageSequence.Iterator(img):
        i = ImageOps.exif_transpose(i)
        if i.mode == "I":
            i = i.point(lambda i: i * (1 / 255))
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if "A" in i.getbands():
            mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
        output_images.append(image)
        output_masks.append(mask.unsqueeze(0))

    if len(output_images) > 1:
        output_image = torch.cat(output_images, dim=0)
        output_mask = torch.cat(output_masks, dim=0)
    else:
        output_image = output_images[0]
        output_mask = output_masks[0]
    return (output_image, output_mask)


def convert_tensor_batch_to_base_64(image_batch):
    if isinstance(image_batch, torch.Tensor):
        # Ensure it's on CPU
        image_batch = image_batch.cpu()

        # If it's a 3D tensor, add a batch dimension
        if image_batch.dim() == 3:
            image_batch = image_batch.unsqueeze(0)

        # Permute dimensions if necessary (from B, C, H, W to B, H, W, C)
        if image_batch.shape[1] < image_batch.shape[3]:
            image_batch = image_batch.permute(0, 2, 3, 1)

        # Scale to 0-255 and convert to uint8
        image_batch = (255.0 * image_batch).clamp(0, 255).numpy().astype(np.uint8)

        base64_images = []
        for img_array in image_batch:
            img = Image.fromarray(img_array)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
            base64_images.append(base64_image)

        print(f"Converted {len(base64_images)} images to base64")
        return base64_images
    else:
        return None


def convert_tensor_to_base_64(image):
    if not isinstance(image, torch.Tensor):
        raise TypeError("Input must be a PyTorch tensor")

    # Ensure it's on CPU
    image = image.cpu()

    # Handle different tensor shapes
    if image.dim() == 2:  # Single channel image
        image = image.unsqueeze(0).unsqueeze(0)  # Add batch and channel dims
    elif image.dim() == 3:  # Single image with channels
        image = image.unsqueeze(0)  # Add batch dim
    elif image.dim() == 4:  # Batch of images or complex structure
        pass  # Already in the right format
    else:
        raise ValueError(f"Unexpected tensor shape: {image.shape}")

    # Permute dimensions if necessary (from B, C, H, W to B, H, W, C)
    if image.shape[1] < image.shape[3]:
        image = image.permute(0, 2, 3, 1)

    # Scale to 0-255 and convert to uint8
    image = (255.0 * image).clamp(0, 255).to(torch.uint8).numpy()

    base64_images = []
    for img_array in image.reshape(-1, *image.shape[-3:]):
        img = Image.fromarray(img_array)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        base64_images.append(base64_image)

    return base64_images
