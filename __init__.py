"""
@author: Jason Schleifer
@title: ComfyUI Griptape Nodes
@nickname: ComfyUI-Griptape
@description: This extension offers various nodes that allow you to work with LLMs using the Griptape Python Framework (https://griptape.ai)
"""

import os
import json

from dotenv import load_dotenv

from .py.griptape_config import (
    load_and_prepare_config,
    set_environment_variables_from_config,
)  # Load the griptape_config.json data

from .nodes.agent import CreateAgent, RunAgent, ExpandAgent
from .nodes.config import (
    gtUIOpenAiStructureConfig,
    gtUIAmazonBedrockStructureConfig,
    gtUIGoogleStructureConfig,
    gtUIAnthropicStructureConfig,
)
from .nodes.tools import gtUIDateTime, gtUICalculator, gtUIWebScraper, gtUIFileManager
from .nodes.list import ToolList
from .nodes.tasks import (
    gtUIGroqPromptTask,
    gtUIPromptTask,
    gtUIToolTask,
    gtUITextSummaryTask,
    gtUIToolkitTask,
    gtUIImageQueryTask,
    gtUIPromptImageGenerationTask,
    gtUIPromptImageVariationTask,
)
from .nodes.drivers import (
    gtUIOpenAiImageGenerationDriver,
    gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
    gtUIAmazonBedrockTitanImageGenerationDriver,
    gtUILeonardoImageGenerationDriver,
)

from .nodes.output_nodes import gtUIOutputStringNode, gtUIOutputImageNode
from .nodes.input_nodes import gtUIInputStringNode
from .nodes.html_node import HtmlNode
from .nodes.rules import gtUIRule
from .nodes.string_nodes import JoinStringListNode

# Setup to compute file paths relative to the directory containing this script

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(THIS_DIR, "griptape_config.json.default")
USER_CONFIG_FILE = os.path.join(THIS_DIR, "griptape_config.json")

# Load existing environment variables
load_dotenv()

# Now load and prepare the configuration
config = load_and_prepare_config(DEFAULT_CONFIG_FILE, USER_CONFIG_FILE)

# Optionally set environment variables from this config if needed
set_environment_variables_from_config(config)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    # "HtmlNode": HtmlNode,
    "gtUIInputNode": gtUIInputStringNode,
    "gtUIOpenAiImageGenerationDriver": gtUIOpenAiImageGenerationDriver,
    "gtUIAmazonBedrockStableDiffusionImageGenerationDriver": gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
    "gtUIAmazonBedrockTitanImageGenerationDriver": gtUIAmazonBedrockTitanImageGenerationDriver,
    "gtUILeonardoImageGenerationDriver": gtUILeonardoImageGenerationDriver,
    "gtUIOutputStringNode": gtUIOutputStringNode,
    "gtUIOutputImageNode": gtUIOutputImageNode,
    "gtUIGroqPromptTask": gtUIGroqPromptTask,
    "CreateAgent": CreateAgent,
    "RunAgent": RunAgent,
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
    "PromptTask": gtUIPromptTask,
    "ToolTask": gtUIToolTask,
    "ToolkitTask": gtUIToolkitTask,
    "ImageQueryTask": gtUIImageQueryTask,
    "PromptImageGenerationTask": gtUIPromptImageGenerationTask,
    "PromptImageVariationTask": gtUIPromptImageVariationTask,
    "TextSummaryTask": gtUITextSummaryTask,
    "JoinStringListNode": JoinStringListNode,
    "Rule": gtUIRule,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # "HtmlNode": "Griptape: HTML",
    "gtUIInputNode": "Griptape Input: String",
    "gtUIOpenAiImageGenerationDriver": "Griptape Driver: OpenAI Image Generation",
    "gtUIAmazonBedrockStableDiffusionImageGenerationDriver": "Griptape Driver: Amazon Bedrock Stable Diffusion Image Generation",
    "gtUIAmazonBedrockTitanImageGenerationDriver": "Griptape Driver: Amazon Bedrock Titan Image Generation",
    "gtUILeonardoImageGenerationDriver": "Griptape Driver: Leonardo Image Generation",
    "gtUIOutputStringNode": "Griptape Preview: String",
    "gtUIOutputImageNode": "Griptape Preview: Image",
    "gtUIGroqPromptTask": "Griptape Task: Groq Prompt",
    "CreateAgent": "Griptape: Create Agent",
    "RunAgent": "Griptape: Run Agent",
    "ExpandAgent": "Griptape: Expand Agent Nodes",
    "gtUIOpenAiStructureConfig": "Griptape Config: OpenAI",
    "gtUIAmazonBedrockStructureConfig": "Griptape Config: Amazon Bedrock",
    "gtUIGoogleStructureConfig": "Griptape Config: Google",
    "gtUIAnthropicStructureConfig": "Griptape Config: Anthropic",
    "Calculator": "Griptape Tool: Calculator",
    "DateTime": "Griptape Tool: DateTime",
    "WebScraper": "Griptape Tool: WebScraper",
    "gtUIFileManager": "Griptape Tool: FileManager",
    "ToolList": "Griptape List: Create Tool List",
    "PromptTask": "Griptape Task: Prompt",
    "ToolTask": "Griptape Task: Tool",
    "ToolkitTask": "Griptape Task: Toolkit",
    "ImageQueryTask": "Griptape Task: Image Query",
    "PromptImageGenerationTask": "Griptape Task: Image Generation",
    "PromptImageVariationTask": "Griptape Task: Image Variation",
    "TextSummaryTask": "Griptape Task: Text Summary",
    "JoinStringListNode": "Griptape: Join String List",
    "Rule": "Griptape: Create Rules",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
