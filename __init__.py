"""
@author: Jason Schleifer
@title: ComfyUI Griptape Nodes
@nickname: ComfyUI-Griptape
@description: This extension offers various nodes that allow you to work with LLMs using the Griptape Python Framework (https://griptape.ai)
"""

import os

from dotenv import load_dotenv

# Load the griptape_config.json data
from .nodes.agent.create_agent import CreateAgent
from .nodes.agent.expand_agent import ExpandAgent
from .nodes.agent.run_agent import RunAgent
from .nodes.agent.set_default_agent import gtUISetDefaultAgent
from .nodes.combine.MergeInputs import gtUIMergeInputs
from .nodes.combine.MergeTexts import MergeTexts
from .nodes.combine.RulesList import RulesList
from .nodes.combine.ToolList import ToolList
from .nodes.config.AmazonBedrockStructureConfig import gtUIAmazonBedrockStructureConfig
from .nodes.config.AnthropicStructureConfig import gtUIAnthropicStructureConfig
from .nodes.config.AzureOpenAiStructureConfig import gtUIAzureOpenAiStructureConfig
from .nodes.config.GoogleStructureConfig import gtUIGoogleStructureConfig
from .nodes.config.HuggingFaceStructureConfig import gtUIHuggingFaceStructureConfig
from .nodes.config.LmStudioStructureConfig import gtUILMStudioStructureConfig
from .nodes.config.OllamaStructureConfig import gtUIOllamaStructureConfig
from .nodes.config.OpenAiCompatableConfig import gtUIOpenAiCompatableConfig
from .nodes.config.OpenAiConfig import gtUIOpenAiStructureConfig
from .nodes.convert.TextToClipEncode import gtUITextToClipEncode
from .nodes.convert.TextToCombo import gtUITextToCombo
from .nodes.display.OutputArtifactNode import gtUIOutputArtifactNode
from .nodes.display.OutputDataNode import gtUIOutputDataNode
from .nodes.display.OutputImageNode import gtUIOutputImageNode
from .nodes.display.OutputStringNode import gtUIOutputStringNode
from .nodes.drivers.AmazonBedrockStableDiffusionImageGenerationDriver import (
    gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
)
from .nodes.drivers.AmazonBedrockTitanImageGenerationDriver import (
    gtUIAmazonBedrockTitanImageGenerationDriver,
)
from .nodes.drivers.DuckDuckGoWebSearchDriver import gtUIDuckDuckGoWebSearchDriver
from .nodes.drivers.ElevenLabsTextToSpeechDriver import gtUIElevenLabsTextToSpeechDriver
from .nodes.drivers.GoogleWebSearchDriver import gtUIGoogleWebSearchDriver
from .nodes.drivers.LonardoImageGenerationDriver import (
    gtUILeonardoImageGenerationDriver,
)
from .nodes.drivers.OpenAiAudioTranscriptionDriver import (
    gtUIOpenAiAudioTranscriptionDriver,
)
from .nodes.drivers.OpenAiImageGenerationDriver import gtUIOpenAiImageGenerationDriver
from .nodes.loaders.FetchImage import gtUIFetchImage
from .nodes.loaders.LoadAudio import gtUILoadAudio
from .nodes.rules.Rule import gtUIRule
from .nodes.tasks.AudioTranscriptionTask import gtUIAudioTranscriptionTask

# from .nodes.tasks.csv_extraction_task import gtUICSVExtractionTask
from .nodes.tasks.ImageQueryTask import gtUIImageQueryTask

# from .nodes.tasks.json_extraction_task import gtUIJSONExtractionTask
from .nodes.tasks.ParallelImageQueryTask import gtUIParallelImageQueryTask
from .nodes.tasks.PromptImageGenerationTask import gtUIPromptImageGenerationTask
from .nodes.tasks.PromptImageVariationTask import gtUIPromptImageVariationTask
from .nodes.tasks.PromptTask import gtUIPromptTask
from .nodes.tasks.TextSummaryTask import gtUITextSummaryTask
from .nodes.tasks.TextToSpeechTask import gtUITextToSpeechTask
from .nodes.tasks.ToolkitTask import gtUIToolkitTask
from .nodes.tasks.ToolTask import gtUIToolTask
from .nodes.text.CLIPTextEncode import gtUICLIPTextEncode
from .nodes.text.InputStringNode import gtUIInputStringNode
from .nodes.tools.AudioTranscriptionClient import gtUIAudioTranscriptionClient
from .nodes.tools.Calculator import gtUICalculator
from .nodes.tools.ConvertAgentToTool import gtUIConvertAgentToTool
from .nodes.tools.DateTime import gtUIDateTime
from .nodes.tools.FileManager import gtUIFileManager
from .nodes.tools.KnowledgeBaseTool import gtUIKnowledgeBaseTool
from .nodes.tools.TextToSpeechClient import gtUITextToSpeechClient
from .nodes.tools.WebScraper import gtUIWebScraper
from .nodes.tools.WebSearch import gtUIWebSearch
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
    "Griptape Agent Config: Amazon Bedrock": gtUIAmazonBedrockStructureConfig,
    "Griptape Agent Config: Anthropic": gtUIAnthropicStructureConfig,
    # Unable to test AzureOpenAI config at the moment - so disabling for now
    "Griptape Agent Config: Azure OpenAI": gtUIAzureOpenAiStructureConfig,
    "Griptape Agent Config: Google": gtUIGoogleStructureConfig,
    "Griptape Agent Config: HuggingFace": gtUIHuggingFaceStructureConfig,
    "Griptape Agent Config: LM Studio": gtUILMStudioStructureConfig,
    "Griptape Agent Config: Ollama": gtUIOllamaStructureConfig,
    "Griptape Agent Config: OpenAI": gtUIOpenAiStructureConfig,
    "Griptape Agent Config: OpenAI Compatable": gtUIOpenAiCompatableConfig,
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
    "Griptape Tool: Text to Speech": gtUITextToSpeechClient,
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
    "Griptape Run: Text to Speech": gtUITextToSpeechTask,
    # AUDIO DRIVER
    "Griptape Audio Driver: OpenAI": gtUIOpenAiAudioTranscriptionDriver,
    "Griptape Audio Driver: ElevenLabs": gtUIElevenLabsTextToSpeechDriver,
    # WEBSEARCH DRIVERS
    "Griptape Driver: DuckDuckGo WebSearch": gtUIDuckDuckGoWebSearchDriver,
    "Griptape Driver: Google WebSearch": gtUIGoogleWebSearchDriver,
    # "Griptape Display: Artifact": gtUIOutputArtifactNode,
    # "Griptape Config: Environment Variables": gtUIEnv,
}


__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]
print("   \033[34m- \033[92mDone!\033[0m\n")
