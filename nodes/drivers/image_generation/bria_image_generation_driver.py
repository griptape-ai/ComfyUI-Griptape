from __future__ import annotations

import io
import json
from typing import Literal, Optional

import requests
from attrs import Factory, define, field
from griptape.artifacts import ImageArtifact
from griptape.drivers import BaseImageGenerationDriver
from griptape.utils import import_optional_dependency


@define
class BriaImageGenerationDriver(BaseImageGenerationDriver):
    """Driver for the Bria image generation API.

    Details on Bria image generation parameters can be found here:
    https://bria-ai-api-docs.redoc.ly/tag/Image-Generation#operation/text-to-image/

    Attributes:
        model: The ID of the model to use when generating images. ["base", "fast", "hd"]
        model_version: The version of the model to use when generating images.
        api_key: The API key to use when making requests to the Bria API.
        api_base: The base URL of the Bria API.
        max_attempts: The maximum number of times to poll the Bria API for a completed image.
        aspect_ratio: The aspect ratio of the image.
        steps_num: Optionally specify the number of inference steps to run for each image generation request, [30, 60].
        seed: Optionally provide a consistent seed to generation requests, increasing consistency in output.
        prompt_enhancement: Optionally set to true if you want to enhance the prompt using Meta llama 3.
        text_guidance_scale: Determines how closely the generated image should adhere to the input text description.
        medium: Which medium should be included in your generated images. This parameter is optional. ["photography", "art"]
        negative_prompt: Optionally provide a negative prompt to guide the generation.
        guidance_method_1: Which guidance type you would like to include in the generation. Up to 4 guidance methods can be combined during a single inference. This parameter is optional.
        guidance_method_1_scale: The impact of the guidance
    """

    model_version: str = field(
        default="2.3", kw_only=True, metadata={"serializable": True}
    )
    api_key: str = field(kw_only=True, metadata={"serializable": True})
    api_base: str = "https://engine.prod.bria-api.com/v1/text-to-image/"
    requests_session: requests.Session = field(
        default=Factory(lambda: requests.Session()), kw_only=True
    )
    max_attempts: int = field(default=10, kw_only=True, metadata={"serializable": True})
    aspect_ratio: Optional[
        Literal["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9"]
    ] = field(
        default=None,
        kw_only=True,
        metadata={"serializable": True},
    )
    steps_num: Optional[int] = field(
        default=None, kw_only=True, metadata={"serializable": True}
    )
    seed: Optional[int] = field(
        default=None, kw_only=True, metadata={"serializable": True}
    )
    prompt_enhancement: Optional[bool] = field(
        default=False, kw_only=True, metadata={"serializable": True}
    )
    text_guidance_scale: Optional[float] = field(
        default=5,
        kw_only=True,
        metadata={"serializable": True},
    )
    medium: Optional[
        Literal[
            "photography",
            "art",
        ]
    ] = field(
        default=None,
        kw_only=True,
        metadata={"serializable": True},
    )

    guidance_methods = Literal[
        "controlnet_canny",
        "controlnet_depth",
        "controlnet_recoloring",
        "controlnet_color_grid",
    ]
    # Guidance methods for image variation
    guidance_method_1: Optional[guidance_methods] = field(
        default="controlnet_canny",
        kw_only=True,
        metadata={"serializable": True},
    )
    guidance_method_1_scale: Optional[float] = field(
        default=0.5,
        kw_only=True,
        metadata={"serializable": True},
    )

    guidance_method_2: Optional[guidance_methods] = field(
        default="controlnet_canny",
        kw_only=True,
        metadata={"serializable": True},
    )
    guidance_method_2_scale: Optional[float] = field(
        default=0.5,
        kw_only=True,
        metadata={"serializable": True},
    )
    guidance_method_3: Optional[guidance_methods] = field(
        default="controlnet_canny",
        kw_only=True,
        metadata={"serializable": True},
    )
    guidance_method_3_scale: Optional[float] = field(
        default=0.5,
        kw_only=True,
        metadata={"serializable": True},
    )
    guidance_method_4: Optional[guidance_methods] = field(
        default="controlnet_canny",
        kw_only=True,
        metadata={"serializable": True},
    )
    guidance_method_4_scale: Optional[float] = field(
        default=0.5,
        kw_only=True,
        metadata={"serializable": True},
    )

    def try_text_to_image(
        self, prompts: list[str], negative_prompts: Optional[list[str]] = None
    ) -> ImageArtifact:
        if negative_prompts is None:
            negative_prompts = []

        generation_result = self._create_generation(
            prompts=prompts, negative_prompts=negative_prompts
        )
        image_urls = self._get_image_url(data=generation_result)
        image_data = self._download_image(url=image_urls[0])
        image_width, image_height = self._get_image_dimensions(image_data)
        artifact = ImageArtifact(
            value=image_data,
            format="png",
            width=image_width,
            height=image_height,
            meta={
                "model": self.model,
                "model_version": self.model_version,
                "prompt": ", ".join(prompts),
            },
        )

        return artifact

    def try_image_variation(
        self,
        prompts: list[str],
        image: ImageArtifact,
        negative_prompts: Optional[list[str]] = None,
    ) -> ImageArtifact:
        if negative_prompts is None:
            negative_prompts = []

        # Get the base64 encoded image data
        image_data = image.base64

        # Confirm the image_data is indeed base64 encoded
        if not self._is_base64(image_data):
            raise ValueError("Image data is not base64 encoded.")

        generation_result = self._create_generation(
            prompts=prompts,
            negative_prompts=negative_prompts,
            image=image_data,
        )
        image_urls = self._get_image_url(data=generation_result)
        new_image_data = self._download_image(url=image_urls[0])
        image_width, image_height = self._get_image_dimensions(new_image_data)

        artifact = ImageArtifact(
            value=new_image_data,
            format="png",
            width=image_width,
            height=image_height,
            meta={
                "model": self.model,
                "model_version": self.model_version,
                "prompt": ", ".join(prompts),
            },
        )
        return artifact

    def try_image_outpainting(
        self,
        prompts: list[str],
        image: ImageArtifact,
        mask: ImageArtifact,
        negative_prompts: Optional[list[str]] = None,
    ) -> ImageArtifact:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support outpainting"
        )

    def try_image_inpainting(
        self,
        prompts: list[str],
        image: ImageArtifact,
        mask: ImageArtifact,
        negative_prompts: Optional[list[str]] = None,
    ) -> ImageArtifact:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support inpainting"
        )

    def _is_base64(self, s: str) -> bool:
        base64 = import_optional_dependency("base64")

        if len(s) % 4 != 0:
            return False

        try:
            # Decode and then re-encode to check if it matches the original
            return base64.b64encode(base64.b64decode(s)).decode("utf-8") == s
        except Exception:
            return False

    def _get_image_dimensions(self, image_data: bytes) -> tuple:
        pil_image = import_optional_dependency("PIL.Image")

        # Open the image in memory
        with pil_image.open(io.BytesIO(image_data)) as img:
            width, height = img.size
        return width, height

    def _create_generation(
        self,
        prompts: list[str],
        negative_prompts: list[str],
        image: Optional[str] = None,
    ) -> str:
        prompt = ", ".join(prompts)
        negative_prompt = ", ".join(negative_prompts)
        model = self.model
        model_version = self.model_version
        aspect_ratio = self.aspect_ratio
        request = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_results": 1,  # default to 1 result
            "aspect_ratio": aspect_ratio,
            "sync": True,
        }

        if self.steps_num is not None:
            request["steps_num"] = self.steps_num
        if self.aspect_ratio is not None:
            request["aspect_ratio"] = self.aspect_ratio
        if self.seed is not None:
            request["seed"] = self.seed
        if self.prompt_enhancement is not None:
            request["prompt_enhancement"] = self.prompt_enhancement
        if self.text_guidance_scale is not None:
            request["text_guidance_scale"] = self.text_guidance_scale
        if self.medium is not None:
            request["medium"] = self.medium

        # For image variation
        if image is not None:
            if self.guidance_method_1 is not None:
                request["guidance_method_1_image_file"] = image
                request["guidance_method_1"] = self.guidance_method_1
                if self.guidance_method_1_scale is not None:
                    request["guidance_method_1_scale"] = self.guidance_method_1_scale
            if self.guidance_method_2 is not None:
                request["guidance_method_2_image_file"] = image
                request["guidance_method_2"] = self.guidance_method_2
                if self.guidance_method_2_scale is not None:
                    request["guidance_method_2_scale"] = self.guidance_method_2_scale
            if self.guidance_method_3 is not None:
                request["guidance_method_3_image_file"] = image
                request["guidance_method_3"] = self.guidance_method_3
                if self.guidance_method_3_scale is not None:
                    request["guidance_method_3_scale"] = self.guidance_method_3_scale
            if self.guidance_method_4 is not None:
                request["guidance_method_4_image_file"] = image
                request["guidance_method_4"] = self.guidance_method_4
                if self.guidance_method_4_scale is not None:
                    request["guidance_method_4_scale"] = self.guidance_method_4_scale

        response = self._make_api_request(model, model_version, request=request)

        if not response:
            raise Exception(f"failed to create generation: {response}")

        result = json.loads(response)["result"]
        return result

    def _make_api_request(
        self, model: str, model_version: str, request: dict, method: str = "POST"
    ) -> dict:
        url = f"{self.api_base}{model}/{model_version}"
        headers = {"api_token": self.api_key, "Content-Type": "application/json"}

        try:
            response = self.requests_session.request(
                method=method, url=url, json=request, headers=headers
            )
        except Exception as e:
            print(e)
            return None
            raise Exception(f"failed to make API request: {e}") from e
        if not response.ok:
            raise Exception(f"failed to make API request: {response.text}")
        try:
            return str(response.text)
        except ValueError:
            return json.loads(response.text)

    def _get_image_url(self, data: dict) -> str:
        image_urls = [item["urls"][0] for item in data if "urls" in item]
        if image_urls:
            pass
        else:
            print("No image URLs found in response.")
        return image_urls

    def _download_image(self, url: str) -> bytes:
        response = self.requests_session.get(
            url=url, headers={"api_token": f"{self.api_key}"}
        )

        return response.content
