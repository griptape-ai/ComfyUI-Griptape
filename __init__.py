"""
@author: Jason Schleifer
@title: ComfyUI Griptape Nodes
@nickname: ComfyUI-Griptape
@description: This extension offers various nodes that allow you to work with LLMs using the Griptape Python Framework (https://griptape.ai)
"""

import json
import os

from dotenv import load_dotenv

# Load the griptape_config.json data
from .nodes.agent import CreateAgent, ExpandAgent
from .nodes.combine_nodes import MergeTexts, ToolList
from .nodes.config import (
    gtUIAmazonBedrockStructureConfig,
    gtUIAnthropicStructureConfig,
    gtUIGoogleStructureConfig,
    gtUIOpenAiStructureConfig,
)
from .nodes.display_nodes import gtUIOutputImageNode, gtUIOutputStringNode
from .nodes.image_drivers import (
    gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
    gtUIAmazonBedrockTitanImageGenerationDriver,
    gtUILeonardoImageGenerationDriver,
    gtUIOpenAiImageGenerationDriver,
)
from .nodes.image_nodes import (
    gtUIFetchImage,
)
from .nodes.rules import gtUIRule
from .nodes.tasks import (
    gtUIImageQueryTask,
    gtUIPromptImageGenerationTask,
    gtUIPromptImageVariationTask,
    gtUIPromptTask,
    gtUITextSummaryTask,
    gtUIToolkitTask,
    gtUIToolTask,
)
from .nodes.text_nodes import (
    gtUICLIPTextEncode,
    gtUIInputStringNode,
    gtUITextToClipEncode,
)
from .nodes.tools import gtUICalculator, gtUIDateTime, gtUIFileManager, gtUIWebScraper
from .py.griptape_config import (
    load_and_prepare_config,
    set_environment_variables_from_config,
)

# Setup to compute file paths relative to the directory containing this script

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(THIS_DIR, "griptape_config.json.default")
USER_CONFIG_FILE = os.path.join(THIS_DIR, "griptape_config.json")

# Load existing environment variables
load_dotenv()

print("\n\033[34m[Griptape Custom Nodes]:\033[0m")


# Now load and prepare the configuration
config = load_and_prepare_config(DEFAULT_CONFIG_FILE, USER_CONFIG_FILE)

# Optionally set environment variables from this config if needed
set_environment_variables_from_config(config)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    "gtUIInputNode": gtUIInputStringNode,
    "gtUIFetchImage": gtUIFetchImage,
    "gtUITextToClipEncode": gtUITextToClipEncode,
    "gtUICLIPTextEncode": gtUICLIPTextEncode,
    "gtUIOpenAiImageGenerationDriver": gtUIOpenAiImageGenerationDriver,
    "gtUIAmazonBedrockStableDiffusionImageGenerationDriver": gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
    "gtUIAmazonBedrockTitanImageGenerationDriver": gtUIAmazonBedrockTitanImageGenerationDriver,
    "gtUILeonardoImageGenerationDriver": gtUILeonardoImageGenerationDriver,
    "gtUIOutputStringNode": gtUIOutputStringNode,
    "gtUIOutputImageNode": gtUIOutputImageNode,
    "CreateAgent": CreateAgent,
    "ExpandAgent": ExpandAgent,
    "gtUIOpenAiStructureConfig": gtUIOpenAiStructureConfig,
    "gtUIAmazonBedrockStructureConfig": gtUIAmazonBedrockStructureConfig,
    "gtUIGoogleStructureConfig": gtUIGoogleStructureConfig,
    "gtUIAnthropicStructureConfig": gtUIAnthropicStructureConfig,
    "Calculator": gtUICalculator,
    "DateTime": gtUIDateTime,
    "WebScraper": gtUIWebScraper,
    "gtUIFileManager": gtUIFileManager,
    "ToolList": ToolList,
    "MergeTexts": MergeTexts,
    "PromptTask": gtUIPromptTask,
    "ToolTask": gtUIToolTask,
    "ToolkitTask": gtUIToolkitTask,
    "ImageQueryTask": gtUIImageQueryTask,
    "PromptImageGenerationTask": gtUIPromptImageGenerationTask,
    "PromptImageVariationTask": gtUIPromptImageVariationTask,
    "TextSummaryTask": gtUITextSummaryTask,
    "Rule": gtUIRule,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "gtUIInputNode": "Griptape Create: Text",
    "gtUIFetchImage": "Griptape Load: Image From URL",
    "gtUITextToClipEncode": "Griptape Convert: Text to CLIP Encode",
    "gtUICLIPTextEncode": "Griptape Create: CLIP Text Encode",
    "CreateAgent": "Griptape Create: Agent",
    "PromptImageGenerationTask": "Griptape Create: Image from Text",
    "PromptImageVariationTask": "Griptape Create: Image Variation",
    "Rule": "Griptape Create: Rules",
    "gtUIOpenAiImageGenerationDriver": "Griptape Driver: OpenAI",
    "gtUIAmazonBedrockStableDiffusionImageGenerationDriver": "Griptape Driver: Amazon Bedrock Stable Diffusion",
    "gtUIAmazonBedrockTitanImageGenerationDriver": "Griptape Driver: Amazon Bedrock Titan",
    "gtUILeonardoImageGenerationDriver": "Griptape Driver: Leonardo.AI",
    "gtUIOutputStringNode": "Griptape Display: Text",
    "gtUIOutputImageNode": "Griptape Display: Image",
    "ImageQueryTask": "Griptape Run: Image Description",
    "PromptTask": "Griptape Run: Prompt Task",
    "ToolTask": "Griptape Run: Tool Task",
    "ToolkitTask": "Griptape Run: Toolkit Task",
    "TextSummaryTask": "Griptape Run: Text Summary",
    "ExpandAgent": "Griptape Expand: Agent Nodes",
    "gtUIOpenAiStructureConfig": "Griptape Agent Config: OpenAI",
    "gtUIAmazonBedrockStructureConfig": "Griptape Agent Config: Amazon Bedrock",
    "gtUIGoogleStructureConfig": "Griptape Agent Config: Google",
    "gtUIAnthropicStructureConfig": "Griptape Agent Config: Anthropic",
    "Calculator": "Griptape Tool: Calculator",
    "DateTime": "Griptape Tool: DateTime",
    "WebScraper": "Griptape Tool: WebScraper",
    "gtUIFileManager": "Griptape Tool: FileManager",
    "ToolList": "Griptape Combine: Tool List",
    "MergeTexts": "Griptape Combine: Merge Text",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
print("   \033[34m- \033[92mDone!\033[0m\n")
