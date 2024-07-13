"""
@author: Jason Schleifer
@title: ComfyUI Griptape Nodes
@nickname: ComfyUI-Griptape
@description: This extension offers various nodes that allow you to work with LLMs using the Griptape Python Framework (https://griptape.ai)
"""

import json
import os

from dotenv import load_dotenv

from .nodes.agent.convert_agent_to_tool import gtUIConvertAgentToTool

# Load the griptape_config.json data
from .nodes.agent.create_agent import CreateAgent
from .nodes.agent.expand_agent import ExpandAgent
from .nodes.agent.run_agent import RunAgent
from .nodes.agent.set_default_agent import gtUISetDefaultAgent
from .nodes.audio_drivers import gtUIOpenAiAudioTranscriptionDriver
from .nodes.audio_nodes import gtUILoadAudio
from .nodes.combine_nodes import MergeTexts, RulesList, ToolList, gtUIMergeInputs
from .nodes.config.amazon_bedrock_config import gtUIAmazonBedrockStructureConfig
from .nodes.config.anthropic_config import gtUIAnthropicStructureConfig
from .nodes.config.google_config import gtUIGoogleStructureConfig
from .nodes.config.lmstudio_config import gtUILMStudioStructureConfig
from .nodes.config.ollama_config import gtUIOllamaStructureConfig
from .nodes.config.openai_compatible_config import gtUIOpenAiCompatibleConfig
from .nodes.config.openai_config import gtUIOpenAiStructureConfig

# from .nodes.config.config_nodes import (
#     # gtUIEnv,
#     # gtUIGoogleStructureConfig,
#     # gtUILMStudioStructureConfig,
#     # gtUIOllamaStructureConfig,
#     # gtUIOpenAiStructureConfig,
# )
from .nodes.display_nodes import (
    # gtUIOutputArtifactNode,
    gtUIOutputDataNode,
    gtUIOutputImageNode,
    gtUIOutputStringNode,
)
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

# from .nodes.structure_nodes import (
#     gtUICreatePipeline,
#     gtUIPipelineAddTask,
#     gtUIPipelineInsertTask,
#     gtUIRunStructure,
# )
from .nodes.tasks import (
    gtUIAudioTranscriptionTask,
    gtUIImageQueryTask,
    gtUIParallelImageQueryTask,
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
    gtUITextToCombo,
)
from .nodes.tools import (
    gtUIAudioTranscriptionClient,
    gtUICalculator,
    gtUIDateTime,
    gtUIFileManager,
    gtUIKnowledgeBaseTool,
    gtUIWebScraper,
    gtUIWebSearch,
)
from .nodes.websearch_drivers import (
    gtUIDuckDuckGoWebSearchDriver,
    gtUIGoogleWebSearchDriver,
)
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
    # AGENT
    "Griptape Create: Agent": CreateAgent,
    "Griptape Run: Agent": RunAgent,
    "Griptape Expand: Agent Nodes": ExpandAgent,
    "Griptape Set: Default Agent": gtUISetDefaultAgent,
    # AGENT CONFIG
    "Griptape Agent Config: OpenAI": gtUIOpenAiStructureConfig,
    "Griptape Agent Config: OpenAI Compatible": gtUIOpenAiCompatibleConfig,
    "Griptape Agent Config: Amazon Bedrock": gtUIAmazonBedrockStructureConfig,
    "Griptape Agent Config: Google": gtUIGoogleStructureConfig,
    "Griptape Agent Config: Anthropic": gtUIAnthropicStructureConfig,
    "Griptape Agent Config: Ollama": gtUIOllamaStructureConfig,
    "Griptape Agent Config: LM Studio": gtUILMStudioStructureConfig,
    # AGENT CONVERSION
    "Griptape Convert: Agent to Tool": gtUIConvertAgentToTool,
    # AGENT RULES
    "Griptape Create: Rules": gtUIRule,
    "Griptape Combine: Rules List": RulesList,
    # TASKS
    "Griptape Run: Prompt Task": gtUIPromptTask,
    "Griptape Run: Text Summary": gtUITextSummaryTask,
    "Griptape Run: Tool Task": gtUIToolTask,
    "Griptape Run: Toolkit Task": gtUIToolkitTask,
    # # STRUCTURES
    # "Griptape Create: Pipeline": gtUICreatePipeline,
    # "Griptape Run: Structure": gtUIRunStructure,
    # "Griptape Pipeline: Add Task": gtUIPipelineAddTask,
    # "Griptape Pipeline: Insert Task": gtUIPipelineInsertTask,
    # AGENT TOOLS
    "Griptape Tool: Audio Transcription": gtUIAudioTranscriptionClient,
    "Griptape Tool: Calculator": gtUICalculator,
    "Griptape Tool: DateTime": gtUIDateTime,
    "Griptape Tool: FileManager": gtUIFileManager,
    "Griptape Tool: Griptape Cloud KnowledgeBase": gtUIKnowledgeBaseTool,
    "Griptape Tool: WebScraper": gtUIWebScraper,
    "Griptape Tool: WebSearch": gtUIWebSearch,
    "Griptape Combine: Tool List": ToolList,
    # TEXT
    "Griptape Create: Text": gtUIInputStringNode,
    "Griptape Create: CLIP Text Encode": gtUICLIPTextEncode,
    "Griptape Convert: Text to CLIP Encode": gtUITextToClipEncode,
    "Griptape Convert: Text to Combo": gtUITextToCombo,
    "Griptape Combine: Merge Texts": MergeTexts,
    "Griptape Combine: Merge Inputs": gtUIMergeInputs,
    # IMAGES
    "Griptape Create: Image from Text": gtUIPromptImageGenerationTask,
    "Griptape Create: Image Variation": gtUIPromptImageVariationTask,
    "Griptape Load: Image From URL": gtUIFetchImage,
    "Griptape Run: Image Description": gtUIImageQueryTask,
    "Griptape Run: Parallel Image Description": gtUIParallelImageQueryTask,
    # IMAGE DRIVERS
    "Griptape Driver: Amazon Bedrock Stable Diffusion": gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
    "Griptape Driver: Amazon Bedrock Titan": gtUIAmazonBedrockTitanImageGenerationDriver,
    "Griptape Driver: Leonardo.AI": gtUILeonardoImageGenerationDriver,
    "Griptape Driver: OpenAI Image Generation": gtUIOpenAiImageGenerationDriver,
    # DISPLAY
    "Griptape Display: Image": gtUIOutputImageNode,
    "Griptape Display: Text": gtUIOutputStringNode,
    "Griptape Display: Data as Text": gtUIOutputDataNode,
    # AUDIO
    "Griptape Load: Audio": gtUILoadAudio,
    "Griptape Run: Audio Transcription": gtUIAudioTranscriptionTask,
    # AUDIO DRIVER
    "Griptape Audio Driver: OpenAI": gtUIOpenAiAudioTranscriptionDriver,
    # WEBSEARCH DRIVERS
    "Griptape Driver: DuckDuckGo WebSearch": gtUIDuckDuckGoWebSearchDriver,
    "Griptape Driver: Google WebSearch": gtUIGoogleWebSearchDriver,
    # "Griptape Display: Artifact": gtUIOutputArtifactNode,
    # "Griptape Config: Environment Variables": gtUIEnv,
}

# NODE_DISPLAY_NAME_MAPPINGS = {
#     "gtUIInputNode": "Griptape Create: Text",
#     "gtUICLIPTextEncode": "Griptape Create: CLIP Text Encode",
#     "gtUITextToClipEncode": "Griptape Convert: Text to CLIP Encode",
#     "gtUIFetchImage": "Griptape Load: Image From URL",
#     "CreateAgent": "Griptape Create: Agent",
#     "RunAgent": "Griptape Run: Agent",
#     "PromptImageGenerationTask": "Griptape Create: Image from Text",
#     "PromptImageVariationTask": "Griptape Create: Image Variation",
#     "Rule": "Griptape Create: Rules",
#     "RulesList": "Griptape Create: Rules List",
#     "gtUIOpenAiAudioTranscriptionDriver": "Griptape Driver: OpenAI",
#     "gtUIAmazonBedrockStableDiffusionImageGenerationDriver": "Griptape Driver: Amazon Bedrock Stable Diffusion",
#     "gtUIAmazonBedrockTitanImageGenerationDriver": "Griptape Driver: Amazon Bedrock Titan",
#     "gtUILeonardoImageGenerationDriver": "Griptape Driver: Leonardo.AI",
#     "gtUIOutputStringNode": "Griptape Display: Text",
#     "gtUIOutputImageNode": "Griptape Display: Image",
#     "gtUIOutputArtifactNode": "Griptape Display: Artifact",
#     "ImageQueryTask": "Griptape Run: Image Description",
#     "ParallelImageQueryTask": "Griptape Run: Parallel Image Description",
#     "PromptTask": "Griptape Run: Prompt Task",
#     "ToolTask": "Griptape Run: Tool Task",
#     "ToolkitTask": "Griptape Run: Toolkit Task",
#     "TextSummaryTask": "Griptape Run: Text Summary",
#     "AudioTranscriptionTask": "Griptape Run: Audio Transcription",
#     "ExpandAgent": "Griptape Expand: Agent Nodes",
#     "gtUIOpenAiStructureConfig": "Griptape Agent Config: OpenAI",
#     "gtUIAmazonBedrockStructureConfig": "Griptape Agent Config: Amazon Bedrock",
#     "gtUIGoogleStructureConfig": "Griptape Agent Config: Google",
#     "gtUIAnthropicStructureConfig": "Griptape Agent Config: Anthropic",
#     "gtUIOllamaStructureConfig": "Griptape Agent Config: Ollama",
#     "gtUILMStudioStructureConfig": "Griptape Agent Config: LM Studio",
#     "Calculator": "Griptape Tool: Calculator",
#     "DateTime": "Griptape Tool: DateTime",
#     "WebScraper": "Griptape Tool: WebScraper",
#     "gtUIFileManager": "Griptape Tool: FileManager",
#     "gtAudioTranscriptionClient": "Griptape Tool: Audio Transcription",
#     "gtUIKnowledgeBaseTool": "Griptape Tool: Griptape Cloud KnowledgeBase",
#     "gtUIWebSearch": "Griptape Tool: WebSearch",
#     "ToolList": "Griptape Combine: Tool List",
#     "MergeTexts": "Griptape Combine: Merge Texts",
#     "EnvironmentConfig": "Griptape Config: Environment Variables",
#     "gtUIOpenAiImageGenerationDriver": "Griptape Audio Driver: OpenAI",
#     "gtUILoadAudio": "Griptape Load: Audio",
# }

__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]
print("   \033[34m- \033[92mDone!\033[0m\n")
