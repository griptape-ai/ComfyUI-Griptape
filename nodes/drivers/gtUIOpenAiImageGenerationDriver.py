from typing import get_args, Optional
import os, base64, requests
from io import BytesIO

from PIL import Image  # to detect format/size from bytes

from griptape.drivers.image_generation.openai import OpenAiImageGenerationDriver as _GTDriver
from griptape.artifacts import ImageArtifact
from openai.types import ImageModel

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver

# ---------------------------
# Config & UI lists
# ---------------------------
DEFAULT_API_KEY = "OPENAI_API_KEY"

# Models from SDK hints; ensure modern entries exist even if typing lags
try:
    _sdk_models = list(get_args(ImageModel))
except Exception:
    _sdk_models = []
_PREFERRED = ["gpt-image-1", "dall-e-3", "dall-e-2"]
models: list[str] = []
for m in _PREFERRED + _sdk_models:
    if m and m not in models:
        models.append(m)

DEFAULT_MODEL = (
    "gpt-image-1"
    if "gpt-image-1" in models
    else ("dall-e-3" if "dall-e-3" in models else "dall-e-2")
)

sizes = [
    "256x256",
    "512x512",
    "1024x1024",
    "1024x1792",  # portrait
    "1792x1024",  # landscape
]


# ---------------------------
# Compat driver: calls Images API directly and returns ImageArtifact with format/size
# ---------------------------
class PatchedOpenAiImageGenerationDriver(_GTDriver):
    """
    Griptape-compatible driver that mirrors Comfy's working Images call.

    - Uses OpenAI Images API for all supported models (gpt-image-1, dall-e-3, dall-e-2)
    - Accepts either b64_json or url responses
    - Returns ImageArtifact(value=bytes, format=str, width=int, height=int)
    - Does NOT pass response_format (some bases reject it)
    - Does NOT force organization/base_url (use same defaults as other working nodes)
    """

    def __init__(self, *args, **kwargs):
        self._model: str = (kwargs.get("model") or DEFAULT_MODEL).lower()
        self._image_size: str = kwargs.get("image_size") or "1024x1024"
        self._api_key: Optional[str] = kwargs.get("api_key") or os.getenv("OPENAI_API_KEY")
        super().__init__(*args, **kwargs)

    @staticmethod
    def _normalize_size(model: str, size: str) -> str:
        if model == "dall-e-2":
            # DALL·E 2 is square only (256/512/1024)
            return (
                "1024x1024"
                if size in ("1024x1792", "1792x1024")
                else (size if size in ("256x256", "512x512", "1024x1024") else "1024x1024")
            )
        if model in ("dall-e-3", "gpt-image-1"):
            # These do not accept 256/512 short side
            return "1024x1024" if size in ("256x256", "512x512") else size
        return size

    def try_text_to_image(self, prompts, negative_prompts=None):
        # Griptape passes a list of prompts; flatten to a single string
        prompt_text = " ".join([p for p in (prompts or []) if p]).strip()
        if not prompt_text:
            raise RuntimeError("Empty prompt provided to image generation driver.")

        model = self._model
        size = self._normalize_size(model, self._image_size)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self._api_key)  # rely on same defaults as other working nodes

            # Do NOT pass response_format; accept whatever server returns (b64_json or url)
            resp = client.images.generate(model=model, prompt=prompt_text, size=size)
            d0 = resp.data[0]

            if getattr(d0, "b64_json", None):
                img_bytes = base64.b64decode(d0.b64_json)
            elif getattr(d0, "url", None):
                r = requests.get(d0.url, timeout=60)
                r.raise_for_status()
                img_bytes = r.content
            else:
                raise RuntimeError(f"OpenAI returned no image data for model={model} size={size}")

            # Detect format and dimensions for ImageArtifact constructor
            with Image.open(BytesIO(img_bytes)) as im:
                width, height = im.size
                fmt = (im.format or "PNG")
            # Some builds prefer lowercase format; normalize safely
            fmt_str = str(fmt)
            # Return ImageArtifact with required kwargs for your Griptape version
            return ImageArtifact(value=img_bytes, format=fmt_str, width=width, height=height)

        except Exception as e:
            raise RuntimeError(f"OpenAI image generation failed: {e}") from e


# ---------------------------
# Comfy node wrapper
# ---------------------------
class gtUIOpenAiImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "OpenAI Image Generation Driver"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "image_generation_model": (
                    models,
                    {
                        "default": DEFAULT_MODEL,
                        "tooltip": "Select the image generation model.",
                    },
                ),
                "size": (
                    sizes,
                    {"default": "1024x1024", "tooltip": "Select the desired image size."},
                ),
                "api_key_env_var": (
                    "STRING",
                    {
                        "default": DEFAULT_API_KEY,
                        "tooltip": "Enter the environment variable name for the API key, not the actual API key.",
                    },
                ),
            }
        )
        return inputs

    def adjust_size_based_on_model(self, model, size):
        return PatchedOpenAiImageGenerationDriver._normalize_size(model.lower(), size)

    def build_params(self, **kwargs):
        model = (kwargs.get("image_generation_model") or DEFAULT_MODEL).lower()
        size = self.adjust_size_based_on_model(model, kwargs.get("size", "1024x1024"))
        api_key = self.getenv(kwargs.get("api_key_env_var", DEFAULT_API_KEY))

        params = {}
        if model:
            params["model"] = model
        if size:
            params["image_size"] = size
        if api_key:
            params["api_key"] = api_key
        return params

    def create(self, **kwargs):
        params = self.build_params(**kwargs)
        driver = PatchedOpenAiImageGenerationDriver(**params)
        return (driver,)
