# from .conductor_tool.tool import ConductorTool


class gtUILoRADownloadJob:
    DESCRIPTION = "Griptape LoRA: Download Job"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "job_id": ("STRING", {"default": "0000"}),
                "status": (
                    "STRING",
                    {"default": ""},
                ),
                "links_comment": (
                    "STRING",
                    {"default": "Links"},
                ),
            },
        }

    RETURN_TYPES = ("IMAGE", "MODEL", "STRING")
    RETURN_NAMES = ("IMAGE", "LORA", "LOGS")

    FUNCTION = "create"

    CATEGORY = "Griptape/LoRA"

    def create(self, **kwargs):
        job_id = kwargs.get("job_id")
        status = "Succeeded"
        return {"ui": {"status": status}, "result": (None, None, "")}
