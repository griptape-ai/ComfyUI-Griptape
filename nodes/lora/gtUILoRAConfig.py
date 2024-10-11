import folder_paths


class gtUILoRAConfig:
    DESCRIPTION = "Griptape LoRA: Configuration"

    @classmethod
    def INPUT_TYPES(s):
        #         VRAM (20G, 16G, 12G)
        # Repeat trains per image (10)
        # Max Train Epochs (16)
        # Expected training steps 0
        # Sample Image Prompts
        # Sample Image Every N Steps (0)
        # Advanced Options
        # Seed (42)
        # Workers (2)
        # Learning Rate (8e-4)
        # Save every N epochs (4)
        # Guidance Scale (1)
        # Timestep Sampling (shift)
        # LoRA Rank (4)
        # Resize dataset images (512)
        return {
            "required": {},
            "optional": {
                "model_settings_comment": (
                    "STRING",
                    {"default": "Model Settings"},
                ),
                "base_model": (
                    folder_paths.get_filename_list("checkpoints"),
                    {"tooltip": "The name of the checkpoint (model) to load."},
                ),
                "include_lora": ("BOOLEAN", {"default": False}),
                "base_lora": (
                    folder_paths.get_filename_list("loras"),
                    {"tooltip": "(Optional) The name of the lora to apply."},
                ),
                "lora_settings_comment": (
                    "STRING",
                    {"default": "New LoRA Settings"},
                ),
                "lora_name": ("STRING", {}),
                "test_image_settings_comment": (
                    "STRING",
                    {"default": "Test Image Settings"},
                ),
                "trigger_word": ("STRING", {}),
                "sample_image_prompts": ("STRING", {"multiline": True}),
                "sample_image_every_n_steps": ("INT", {"default": 10}),
                "training_settings_comment": (
                    "STRING",
                    {"default": "Training Settings"},
                ),
                "VRAM": (["20G", "16G", "12G"], {"default": "20G"}),
                "repeat_trains_per_image": ("INT", {"default": 10}),
                "max_train_epochs": ("INT", {"default": 16}),
                "expected_training_steps": ("INT", {"default": 10}),
                "advanced_settings_comment": (
                    "STRING",
                    {"default": "Advanced Settings"},
                ),
                "seed": ("INT", {"default": 42}),
                "workers": ("INT", {"default": 2}),
                "learning_rate": ("STRING", {"default": "8e-4"}),
                "save_every_n_epochs": ("INT", {"default": 4}),
                "guidance_scale": ("INT", {"default": 1}),
                "timestep_sampling": (["shift"], {"default": "shift"}),
                "lora_rank": ("INT", {"default": 4}),
                "resize_dataset_images": ("INT", {"default": 512}),
            },
        }

    RETURN_TYPES = ("LORA_CONFIG",)
    RETURN_NAMES = ("LORA_CONFIG",)

    FUNCTION = "create"
    OUTPUT_NODE = True
    CATEGORY = "Griptape/LoRA"

    def create(self, **kwargs):
        config = {
            "model": kwargs.get("base_model"),
            "include_lora": kwargs.get("include_lora"),
            "base_lora": kwargs.get("base_lora", None),
            "lora_name": kwargs.get("lora_name"),
            "VRAM": kwargs.get("VRAM"),
            "repeat_trains_per_image": kwargs.get("repeat_trains_per_image"),
            "max_train_epochs": kwargs.get("max_train_epochs"),
            "expected_training_steps": kwargs.get("expected_training_steps"),
            "trigger_word": kwargs.get("trigger_word"),
            "sample_image_prompts": [
                prompt.strip()
                for prompt in kwargs.get("sample_image_prompts").splitlines()
                if prompt.strip()
            ]
            if kwargs.get("sample_image_prompts")
            else [],
            "sample_image_every_n_steps": kwargs.get("sample_image_every_n_steps"),
            "seed": kwargs.get("seed"),
            "workers": kwargs.get("workers"),
            "learning_rate": kwargs.get("learning_rate"),
            "save_every_n_epochs": kwargs.get("save_every_n_epochs"),
            "guidance_scale": kwargs.get("guidance_scale"),
            "timestep_sampling": kwargs.get("timestep_sampling"),
            "lora_rank": kwargs.get("lora_rank"),
            "resize_dataset_images": kwargs.get("resize_dataset_images"),
        }

        return (config,)
