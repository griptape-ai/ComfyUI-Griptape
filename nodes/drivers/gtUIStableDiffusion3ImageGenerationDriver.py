import folder_paths
from griptape.drivers import (
    HuggingFacePipelineImageGenerationDriver,
    StableDiffusion3ImageGenerationPipelineDriver,
)

from .gtUIBaseImageDriver import gtUIBaseImageGenerationDriver


def filter_checkpoint_list(filter):
    filename_list = folder_paths.get_filename_list("checkpoints")
    return [filename for filename in filename_list if filter in filename]


class gtUIStableDiffusion3ImageGenerationDriver(gtUIBaseImageGenerationDriver):
    DESCRIPTION = "Stable Diffusion 3 Image Generation Driver"

    @classmethod
    def INPUT_TYPES(s):
        inputs = super().INPUT_TYPES()
        inputs["optional"].update(
            {
                "ckpt_name": (filter_checkpoint_list(filter="sd3"),),
                "width": (
                    "INT",
                    {"default": 512, "min": 64, "max": 2048, "step": 64},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 64, "max": 2048, "step": 64},
                ),
                "steps": (
                    "INT",
                    {"default": 20, "min": 1, "max": 100, "step": 1},
                ),
                "guidance_scale": (
                    "INT",
                    {"default": 7, "min": 1, "max": 20, "step": 1},
                ),
                "device": (["cuda", "mps"], {"default": "cuda"}),
                "enable_model_cpu_offload": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 12345}),
            }
        )
        return inputs

    def create(self, **kwargs):
        ckpt_name = kwargs.get("ckpt_name", None)
        model = folder_paths.get_full_path("checkpoints", ckpt_name)
        width = kwargs.get("width", 512)
        height = kwargs.get("height", 512)
        steps = kwargs.get("steps", 20)
        device = kwargs.get("device", "cuda")
        guidance_scale = kwargs.get("guidance_scale", 7)
        enable_model_cpu_offload = kwargs.get("enable_model_cpu_offload", True)
        seed = kwargs.get("seed", 12345)

        # model = "C:\\Users\\jason\\Documents\\GitHub\\ComfyUI\\models\\checkpoints\\sd3_medium_incl_clips_t5xxlfp16.safetensors"
        pipeline_driver = StableDiffusion3ImageGenerationPipelineDriver(
            drop_t5_encoder=True,
            enable_model_cpu_offload=enable_model_cpu_offload,
            height=height,
            width=width,
            steps=steps,
            seed=seed,
            guidance_scale=guidance_scale,
        )
        driver = HuggingFacePipelineImageGenerationDriver(
            device=device,
            model=model,
            output_format="png",
            pipeline_driver=pipeline_driver,
        )

        return (driver,)
