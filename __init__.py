"""
@author: Jason Schleifer
@title: ComfyUI Griptape Nodes
@nickname: ComfyUI-Griptape
@description: This extension offers various nodes that allow you to work with LLMs using the Griptape Python Framework (https://griptape.ai)
"""

from dotenv import load_dotenv

# AGENT
from .nodes.agent.CreateAgent import CreateAgent
from .nodes.agent.gtUICloudAssistant import gtUICloudAssistant
from .nodes.agent.gtUICreateAgentFromConfig import gtUICreateAgentFromConfig
from .nodes.agent.gtUIReplaceRulesetsOnAgent import gtUIReplaceRulesetsOnAgent
from .nodes.agent.gtUIReplaceToolsOnAgent import gtUIReplaceToolsOnAgent
from .nodes.agent.gtUISetDefaultAgent import gtUISetDefaultAgent
from .nodes.agent.RunAgent import RunAgent

# Chat
from .nodes.chat.gtUIChat import gtUIChat

# COMBINE
from .nodes.combine.gtUIMergeInputs import gtUIMergeInputs
from .nodes.combine.gtUIModuleList import gtUIModuleList
from .nodes.combine.MergeTexts import MergeTexts
from .nodes.combine.RulesList import RulesList
from .nodes.combine.ToolList import ToolList

# CONFIG
from .nodes.config.deprecated.gtUIAmazonBedrockStructureConfig import (
    gtUIAmazonBedrockStructureConfig,
)

# CONFIG - DEPRECATED
from .nodes.config.deprecated.gtUIAnthropicStructureConfig import (
    gtUIAnthropicStructureConfig,
)
from .nodes.config.deprecated.gtUIAzureOpenAiStructureConfig import (
    gtUIAzureOpenAiStructureConfig,
)
from .nodes.config.deprecated.gtUIGoogleStructureConfig import gtUIGoogleStructureConfig
from .nodes.config.deprecated.gtUIHuggingFaceStructureConfig import (
    gtUIHuggingFaceStructureConfig,
)
from .nodes.config.deprecated.gtUILMStudioStructureConfig import (
    gtUILMStudioStructureConfig,
)
from .nodes.config.deprecated.gtUIOllamaStructureConfig import gtUIOllamaStructureConfig
from .nodes.config.deprecated.gtUIOpenAiCompatibleConfig import (
    gtUIOpenAiCompatibleConfig,
)
from .nodes.config.deprecated.gtUIOpenAiStructureConfig import gtUIOpenAiStructureConfig
from .nodes.config.gtUIAmazonBedrockDriversConfig import gtUIAmazonBedrockDriversConfig
from .nodes.config.gtUIAnthropicDriversConfig import gtUIAnthropicDriversConfig
from .nodes.config.gtUIAzureOpenAiDriversConfig import gtUIAzureOpenAiDriversConfig
from .nodes.config.gtUICohereDriversConfig import gtUICohereDriversConfig
from .nodes.config.gtUIEnvConfig import gtUIEnvConfig
from .nodes.config.gtUIGoogleDriversConfig import gtUIGoogleDriversConfig
from .nodes.config.gtUIGroqDriversConfig import gtUIGroqDriversConfig
from .nodes.config.gtUIHuggingFaceDriversConfig import gtUIHuggingFaceDriversConfig
from .nodes.config.gtUILMStudioDriversConfig import gtUILMStudioDriversConfig
from .nodes.config.gtUIOllamaDriversConfig import gtUIOllamaDriversConfig
from .nodes.config.gtUIOpenAiCompatibleDriversConfig import (
    gtUIOpenAiCompatibleDriversConfig,
)
from .nodes.config.gtUIOpenAiDriversConfig import gtUIOpenAiDriversConfig
from .nodes.config.gtUIStructureConfig import gtUIStructureConfig

# CONVERT
from .nodes.convert.gtUITextToClipEncode import gtUITextToClipEncode
from .nodes.convert.gtUITextToCombo import gtUITextToCombo

# Load the routes
from .nodes.custom_routes import init_routes

# DISPLAY
from .nodes.display.gtUIOutputDataNode import gtUIOutputDataNode
from .nodes.display.gtUIOutputImageNode import gtUIOutputImageNode
from .nodes.display.gtUIOutputStringNode import gtUIOutputStringNode

# DRIVERS
# - Amazon Bedrock
from .nodes.drivers.gtUIAmazonBedrockPromptDriver import gtUIAmazonBedrockPromptDriver
from .nodes.drivers.gtUIAmazonBedrockStableDiffusionImageGenerationDriver import (
    gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
)
from .nodes.drivers.gtUIAmazonBedrockTitanEmbeddingDriver import (
    gtUIAmazonBedrockTitanEmbeddingDriver,
)
from .nodes.drivers.gtUIAmazonBedrockTitanImageGenerationDriver import (
    gtUIAmazonBedrockTitanImageGenerationDriver,
)

# - Amazon OpenSearch
from .nodes.drivers.gtUIAmazonOpenSearchVectorStoreDriver import (
    gtUIAmazonOpenSearchVectorStoreDriver,
)

# - Amazon SageMaker Jumpstart
from .nodes.drivers.gtUIAmazonSageMakerJumpstartEmbeddingDriver import (
    gtUIAmazonSageMakerJumpstartEmbeddingDriver,
)
from .nodes.drivers.gtUIAmazonSageMakerJumpstartPromptDriver import (
    gtUIAmazonSageMakerJumpstartPromptDriver,
)

# - Anthropic
# from .nodes.drivers.gtUIAnthropicImageQueryDriver import gtUIAnthropicImageQueryDriver
from .nodes.drivers.gtUIAnthropicPromptDriver import gtUIAnthropicPromptDriver
from .nodes.drivers.gtUIAzureMongoDbVectorStoreDriver import (
    gtUIAzureMongoDbVectorStoreDriver,
)

# - Azure
from .nodes.drivers.gtUIAzureOpenAiChatPromptDriver import (
    gtUIAzureOpenAiChatPromptDriver,
)
from .nodes.drivers.gtUIAzureOpenAiEmbeddingDriver import gtUIAzureOpenAiEmbeddingDriver
from .nodes.drivers.gtUIAzureOpenAiImageGenerationDriver import (
    gtUIAzureOpenAiImageGenerationDriver,
)

# - BlackForest Labs
from .nodes.drivers.gtUIBlackForestImageGenerationDriver import (
    gtUIBlackForestImageGenerationDriver,
)

# - Cohere
from .nodes.drivers.gtUICohereEmbeddingDriver import gtUICohereEmbeddingDriver
from .nodes.drivers.gtUICoherePromptDriver import gtUICoherePromptDriver
from .nodes.drivers.gtUICohereRerankDriver import gtUICohereRerankDriver

# - DuckDuckGo
from .nodes.drivers.gtUIDuckDuckGoWebSearchDriver import gtUIDuckDuckGoWebSearchDriver

# - ElevenLabs
from .nodes.drivers.gtUIElevenLabsTextToSpeechDriver import (
    gtUIElevenLabsTextToSpeechDriver,
)

# - Exa
from .nodes.drivers.gtUIExaWebSearchDriver import gtUIExaWebSearchDriver

# - Google
from .nodes.drivers.gtUIGoogleEmbeddingDriver import gtUIGoogleEmbeddingDriver
from .nodes.drivers.gtUIGooglePromptDriver import gtUIGooglePromptDriver
from .nodes.drivers.gtUIGoogleWebSearchDriver import gtUIGoogleWebSearchDriver

# - Griptape
from .nodes.drivers.gtUIGriptapeCloudVectorStoreDriver import (
    gtUIGriptapeCloudVectorStoreDriver,
)
from .nodes.drivers.gtUIGroqAudioTranscriptionDriver import (
    gtUIGroqAudioTranscriptionDriver,
)

# - Groq
from .nodes.drivers.gtUIGroqChatPromptDriver import gtUIGroqChatPromptDriver

# - HuggingFace
from .nodes.drivers.gtUIHuggingFaceHubEmbeddingDriver import (
    gtUIHuggingFaceHubEmbeddingDriver,
)
from .nodes.drivers.gtUIHuggingFaceHubPromptDriver import gtUIHuggingFaceHubPromptDriver

# - Leonardo.AI
from .nodes.drivers.gtUILeonardoImageGenerationDriver import (
    gtUILeonardoImageGenerationDriver,
)

# - LM Studio
from .nodes.drivers.gtUILMStudioChatPromptDriver import gtUILMStudioChatPromptDriver
from .nodes.drivers.gtUILMStudioEmbeddingDriver import gtUILMStudioEmbeddingDriver

# - Local
from .nodes.drivers.gtUILocalVectorStoreDriver import gtUILocalVectorStoreDriver

# - Marqo
from .nodes.drivers.gtUIMarqoVectorStoreDriver import gtUIMarqoVectorStoreDriver

# - Mongodb
from .nodes.drivers.gtUIMongoDbAtlasVectorStoreDriver import (
    gtUIMongoDbAtlasVectorStoreDriver,
)

# - Ollama
from .nodes.drivers.gtUIOllamaEmbeddingDriver import gtUIOllamaEmbeddingDriver
from .nodes.drivers.gtUIOllamaPromptDriver import gtUIOllamaPromptDriver

# - OpenAI
from .nodes.drivers.gtUIOpenAiAudioTranscriptionDriver import (
    gtUIOpenAiAudioTranscriptionDriver,
)
from .nodes.drivers.gtUIOpenAiChatPromptDriver import gtUIOpenAiChatPromptDriver
from .nodes.drivers.gtUIOpenAiCompatibleChatPromptDriver import (
    gtUIOpenAiCompatibleChatPromptDriver,
)
from .nodes.drivers.gtUIOpenAiCompatibleEmbeddingDriver import (
    gtUIOpenAiCompatibleEmbeddingDriver,
)
from .nodes.drivers.gtUIOpenAiCompatibleImageGenerationDriver import (
    gtUIOpenAiCompatibleImageGenerationDriver,
)
from .nodes.drivers.gtUIOpenAiEmbeddingDriver import gtUIOpenAiEmbeddingDriver
from .nodes.drivers.gtUIOpenAiImageGenerationDriver import (
    gtUIOpenAiImageGenerationDriver,
)
from .nodes.drivers.gtUIOpenAiTextToSpeechDriver import gtUIOpenAiTextToSpeechDriver

# - PGVector
from .nodes.drivers.gtUIPgVectorVectorStoreDriver import gtUIPgVectorVectorStoreDriver

# - Pinecone
from .nodes.drivers.gtUIPineconeVectorStoreDriver import gtUIPineconeVectorStoreDriver

# - Qdrant
from .nodes.drivers.gtUIQdrantVectorStoreDriver import gtUIQdrantVectorStoreDriver

# - Redis
from .nodes.drivers.gtUIRedisVectorStoreDriver import gtUIRedisVectorStoreDriver

# - Serper
from .nodes.drivers.gtUISerperWebSearchDriver import gtUISerperWebSearchDriver

# - Tavily
from .nodes.drivers.gtUITavilyWebSearchDriver import gtUITavilyWebSearchDriver

# - Voyage AI
from .nodes.drivers.gtUIVoyageAiEmbeddingDriver import gtUIVoyageAiEmbeddingDriver
from .nodes.expand.ExpandAgent import ExpandAgent
from .nodes.expand.gtUIExpandConfig import gtUIExpandConfig

# LOADERS
from .nodes.loaders.gtUIFetchImage import gtUIFetchImage
from .nodes.loaders.gtUILoadAudio import gtUILoadAudio
from .nodes.loaders.gtUILoadText import gtUILoadText

# PATCHES
from .nodes.patches.gemini_query_tool import GeminiQueryTool

# RAG
from .nodes.rag.gtUIFootnotePromptResponseRagModule import (
    gtUIFootnotePromptResponseRagModule,
)
from .nodes.rag.gtUIPromptResponseRagModule import gtUIPromptResponseRagModule
from .nodes.rag.gtUIRagEngine import gtUIRagEngine
from .nodes.rag.gtUITextChunksRerankRagModule import gtUITextChunksRerankRagModule
from .nodes.rag.gtUITextChunksResponseRagModule import gtUITextChunksResponseRagModule
from .nodes.rag.gtUITextLoaderRetrievalRagModule import gtUITextLoaderRetrievalRagModule
from .nodes.rag.gtUITranslateQueryRagModule import gtUITranslateQueryRagModule
from .nodes.rag.gtUIVectorStoreRetrievalRagModule import (
    gtUIVectorStoreRetrievalRagModule,
)
from .nodes.rules.gtUICloudRuleset import gtUICloudRuleset

# RULES
from .nodes.rules.gtUIRule import gtUIRule

# - Audio
from .nodes.tasks.gtUIAudioTranscriptionTask import gtUIAudioTranscriptionTask
from .nodes.tasks.gtUICloudStructureRunTask import gtUICloudStructureRunTask

# - Code
from .nodes.tasks.gtUICodeExecutionTask import gtUICodeExecutionTask
from .nodes.tasks.gtUIExtractionTask import gtUIExtractionTask

# - Image
from .nodes.tasks.gtUIImageQueryTask import gtUIImageQueryTask
from .nodes.tasks.gtUIInpaintingImageGenerationTask import (
    gtUIInpaintingImageGenerationTask,
)
from .nodes.tasks.gtUIParallelImageQueryTask import gtUIParallelImageQueryTask
from .nodes.tasks.gtUIPromptImageGenerationTask import gtUIPromptImageGenerationTask
from .nodes.tasks.gtUIPromptImageVariationTask import gtUIPromptImageVariationTask

# TASKS
# - Agent
from .nodes.tasks.gtUITask import gtUITask

# - Text
from .nodes.tasks.gtUITextSummaryTask import gtUITextSummaryTask
from .nodes.tasks.gtUITextToSpeechTask import gtUITextToSpeechTask

# - Vector Store
from .nodes.tasks.gtUIVectorStoreQueryTask import gtUIVectorStoreQueryTask
from .nodes.tasks.gtUIVectorStoreUpsertTextTask import gtUIVectorStoreUpsertTextTask

# TEXT
from .nodes.text.gtUICLIPTextEncode import gtUICLIPTextEncode
from .nodes.text.gtUIInputStringNode import gtUIInputStringNode
from .nodes.text.gtUISaveText import gtUISaveText

# TOOLS
from .nodes.tools.gtUIAudioTranscriptionClient import gtUIAudioTranscriptionClient
from .nodes.tools.gtUICalculator import gtUICalculator
from .nodes.tools.gtUIConvertAgentToTool import gtUIConvertAgentToTool
from .nodes.tools.gtUIDateTime import gtUIDateTime
from .nodes.tools.gtUIExtractionTool import gtUIExtractionTool
from .nodes.tools.gtUIFileManager import gtUIFileManager
from .nodes.tools.gtUIKnowledgeBaseTool import gtUIKnowledgeBaseTool
from .nodes.tools.gtUIPromptSummaryTool import gtUIPromptSummaryTool
from .nodes.tools.gtUIQueryTool import gtUIQueryTool
from .nodes.tools.gtUIRagTool import gtUIRagTool
from .nodes.tools.gtUITextToSpeechClient import gtUITextToSpeechClient
from .nodes.tools.gtUIVectorStoreClient import gtUIVectorStoreClient
from .nodes.tools.gtUIWebScraper import gtUIWebScraper
from .nodes.tools.gtUIWebSearch import gtUIWebSearch

# UTILS
from .nodes.utils.gtUICreateAgentModelfile import gtUICreateAgentModelfile
from .nodes.utils.gtUICreateModelFromModelfile import gtUICreateModelFromModelfile
from .nodes.utils.gtUIRemoveOllamaModel import gtUIRemoveOllamaModel
from .nodes.utils.gtUISwitchNode import gtUISwitchNode

# Load existing environment variables
load_dotenv()

print("\n\033[34m[Griptape Custom Nodes]:\033[0m")

# Initialize the routes
init_routes()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    # AGENT
    "Griptape Create: Agent": CreateAgent,
    "Griptape Create: Agent from Config": gtUICreateAgentFromConfig,
    "Griptape Run: Agent": RunAgent,
    "Griptape Run: Task": gtUITask,
    # "Griptape Run: Prompt Task": gtUIPromptTask,
    # "Griptape Run: Tool Task": gtUIToolTask,
    # "Griptape Run: Toolkit Task": gtUIToolkitTask,
    "Griptape Expand: Agent Nodes": ExpandAgent,
    "Griptape Set: Default Agent": gtUISetDefaultAgent,
    "Griptape Run: Cloud Assistant": gtUICloudAssistant,
    # AGENT CONFIG
    "Griptape Agent Config: Custom Structure": gtUIStructureConfig,
    "Griptape Agent Config: Environment Variables": gtUIEnvConfig,
    "Griptape Agent Config: Expand": gtUIExpandConfig,
    "Griptape Agent Config: Amazon Bedrock Drivers": gtUIAmazonBedrockDriversConfig,
    "Griptape Agent Config: Anthropic Drivers": gtUIAnthropicDriversConfig,
    "Griptape Agent Config: Azure OpenAI Drivers": gtUIAzureOpenAiDriversConfig,
    "Griptape Agent Config: Cohere Drivers": gtUICohereDriversConfig,
    "Griptape Agent Config: Google Drivers": gtUIGoogleDriversConfig,
    "Griptape Agent Config: Groq Drivers": gtUIGroqDriversConfig,
    "Griptape Agent Config: HuggingFace Drivers": gtUIHuggingFaceDriversConfig,
    "Griptape Agent Config: LM Studio Drivers": gtUILMStudioDriversConfig,
    "Griptape Agent Config: Ollama Drivers": gtUIOllamaDriversConfig,
    "Griptape Agent Config: OpenAI Drivers": gtUIOpenAiDriversConfig,
    "Griptape Agent Config: OpenAI Compatible Drivers": gtUIOpenAiCompatibleDriversConfig,
    # DEPRECATED
    "Griptape Agent Config: Amazon Bedrock [DEPRECATED]": gtUIAmazonBedrockStructureConfig,
    "Griptape Agent Config: Anthropic [DEPRECATED]": gtUIAnthropicStructureConfig,
    "Griptape Agent Config: Azure OpenAI [DEPRECATED]": gtUIAzureOpenAiStructureConfig,
    "Griptape Agent Config: Google [DEPRECATED]": gtUIGoogleStructureConfig,
    "Griptape Agent Config: HuggingFace [DEPRECATED]": gtUIHuggingFaceStructureConfig,
    "Griptape Agent Config: LM Studio [DEPRECATED]": gtUILMStudioStructureConfig,
    "Griptape Agent Config: Ollama [DEPRECATED]": gtUIOllamaStructureConfig,
    "Griptape Agent Config: OpenAI [DEPRECATED]": gtUIOpenAiStructureConfig,
    "Griptape Agent Config: OpenAI Compatible [DEPRECATED]": gtUIOpenAiCompatibleConfig,
    # PROMPT DRIVER
    "Griptape Prompt Driver: Amazon Bedrock": gtUIAmazonBedrockPromptDriver,
    "Griptape Prompt Driver: Amazon SageMaker Jumpstart": gtUIAmazonSageMakerJumpstartPromptDriver,
    "Griptape Prompt Driver: Anthropic": gtUIAnthropicPromptDriver,
    "Griptape Prompt Driver: Azure OpenAI": gtUIAzureOpenAiChatPromptDriver,
    "Griptape Prompt Driver: Cohere": gtUICoherePromptDriver,
    "Griptape Prompt Driver: Groq": gtUIGroqChatPromptDriver,
    "Griptape Prompt Driver: Google": gtUIGooglePromptDriver,
    "Griptape Prompt Driver: HuggingFace": gtUIHuggingFaceHubPromptDriver,
    "Griptape Prompt Driver: LM Studio": gtUILMStudioChatPromptDriver,
    "Griptape Prompt Driver: Ollama": gtUIOllamaPromptDriver,
    "Griptape Prompt Driver: OpenAI": gtUIOpenAiChatPromptDriver,
    "Griptape Prompt Driver: OpenAI Compatible": gtUIOpenAiCompatibleChatPromptDriver,
    # IMAGE GENERATION DRIVERS
    "Griptape Driver: Amazon Bedrock Stable Diffusion": gtUIAmazonBedrockStableDiffusionImageGenerationDriver,
    "Griptape Driver: Amazon Bedrock Titan": gtUIAmazonBedrockTitanImageGenerationDriver,
    "Griptape Driver: Azure OpenAI Image Generation": gtUIAzureOpenAiImageGenerationDriver,
    "Griptape Driver: Black Forest Labs Image Generation": gtUIBlackForestImageGenerationDriver,
    "Griptape Driver: Leonardo.AI": gtUILeonardoImageGenerationDriver,
    "Griptape Driver: OpenAI Image Generation": gtUIOpenAiImageGenerationDriver,
    "Griptape Driver: OpenAI Compatible Image Generation": gtUIOpenAiCompatibleImageGenerationDriver,
    # EMBEDDING DRIVER
    "Griptape Embedding Driver: Amazon Bedrock Titan": gtUIAmazonBedrockTitanEmbeddingDriver,
    "Griptape Embedding Driver: Amazon SageMaker Jumpstart": gtUIAmazonSageMakerJumpstartEmbeddingDriver,
    "Griptape Embedding Driver: Azure OpenAI": gtUIAzureOpenAiEmbeddingDriver,
    "Griptape Embedding Driver: Cohere": gtUICohereEmbeddingDriver,
    "Griptape Embedding Driver: Google": gtUIGoogleEmbeddingDriver,
    "Griptape Embedding Driver: HuggingFace": gtUIHuggingFaceHubEmbeddingDriver,
    "Griptape Embedding Driver: LM Studio": gtUILMStudioEmbeddingDriver,
    "Griptape Embedding Driver: Ollama": gtUIOllamaEmbeddingDriver,
    "Griptape Embedding Driver: OpenAI": gtUIOpenAiEmbeddingDriver,
    "Griptape Embedding Driver: OpenAI Compatible": gtUIOpenAiCompatibleEmbeddingDriver,
    "Griptape Embedding Driver: Voyage AI": gtUIVoyageAiEmbeddingDriver,
    # RERANK DRIVER
    "Griptape Rerank Driver: Cohere": gtUICohereRerankDriver,
    # VECTOR STORE DRIVERS
    "Griptape Vector Store Driver: Amazon OpenSearch": gtUIAmazonOpenSearchVectorStoreDriver,
    "Griptape Vector Store Driver: Azure MongoDB": gtUIAzureMongoDbVectorStoreDriver,
    "Griptape Vector Store Driver: Griptape Cloud": gtUIGriptapeCloudVectorStoreDriver,
    "Griptape Vector Store Driver: Marqo": gtUIMarqoVectorStoreDriver,
    "Griptape Vector Store Driver: MongoDB Atlas": gtUIMongoDbAtlasVectorStoreDriver,
    "Griptape Vector Store Driver: Local": gtUILocalVectorStoreDriver,
    "Griptape Vector Store Driver: PGVector": gtUIPgVectorVectorStoreDriver,
    "Griptape Vector Store Driver: Pinecone": gtUIPineconeVectorStoreDriver,
    "Griptape Vector Store Driver: Redis": gtUIRedisVectorStoreDriver,
    "Griptape Vector Store Driver: Qdrant": gtUIQdrantVectorStoreDriver,
    # TEXT TO SPEECH DRIVERS
    "Griptape Text To Speech Driver: ElevenLabs": gtUIElevenLabsTextToSpeechDriver,
    "Griptape Text To Speech Driver: OpenAI": gtUIOpenAiTextToSpeechDriver,
    # AUDIO DRIVERS
    "Griptape Audio Transcription Driver: Groq": gtUIGroqAudioTranscriptionDriver,
    "Griptape Audio Transcription Driver: OpenAI": gtUIOpenAiAudioTranscriptionDriver,
    # WEBSEARCH DRIVERS
    "Griptape WebSearch Driver: DuckDuckGo": gtUIDuckDuckGoWebSearchDriver,
    "Griptape WebSearch Driver: Exa": gtUIExaWebSearchDriver,
    "Griptape WebSearch Driver: Google": gtUIGoogleWebSearchDriver,
    "Griptape WebSearch Driver: Serper": gtUISerperWebSearchDriver,
    "Griptape WebSearch Driver: Tavily": gtUITavilyWebSearchDriver,
    # AGENT RULES
    "Griptape Create: Rules": gtUIRule,
    "Griptape Combine: Rules List": RulesList,
    "Griptape Replace: Rulesets on Agent": gtUIReplaceRulesetsOnAgent,
    "Griptape Retrieve: Cloud Ruleset": gtUICloudRuleset,
    # AGENT TOOLS
    "Griptape Convert: Agent to Tool": gtUIConvertAgentToTool,
    "Griptape Combine: Tool List": ToolList,
    "Griptape Replace: Tools on Agent": gtUIReplaceToolsOnAgent,
    "Griptape Tool: Audio Transcription": gtUIAudioTranscriptionClient,
    "Griptape Tool: Calculator": gtUICalculator,
    "Griptape Tool: DateTime": gtUIDateTime,
    "Griptape Tool: FileManager": gtUIFileManager,
    "Griptape Tool: Griptape Cloud KnowledgeBase": gtUIKnowledgeBaseTool,
    "Griptape Tool: Text to Speech": gtUITextToSpeechClient,
    "Griptape Tool: VectorStore": gtUIVectorStoreClient,
    "Griptape Tool: RAG": gtUIRagTool,
    "Griptape Tool: WebScraper": gtUIWebScraper,
    "Griptape Tool: WebSearch": gtUIWebSearch,
    "Griptape Tool: Extraction": gtUIExtractionTool,
    "Griptape Tool: Prompt Summary": gtUIPromptSummaryTool,
    "Griptape Tool: Query": gtUIQueryTool,
    # AGENT UTILS
    "Griptape Util: Create Agent Modelfile": gtUICreateAgentModelfile,
    "Griptape Util: Create Model from Modelfile": gtUICreateModelFromModelfile,
    "Griptape Util: Remove Ollama Model": gtUIRemoveOllamaModel,
    "Griptape Util: Switch Node": gtUISwitchNode,
    # DISPLAY
    "Griptape Display: Image": gtUIOutputImageNode,
    "Griptape Display: Text": gtUIOutputStringNode,
    "Griptape Display: Data as Text": gtUIOutputDataNode,
    # AUDIO
    "Griptape Run: Audio Transcription": gtUIAudioTranscriptionTask,
    "Griptape Run: Text to Speech": gtUITextToSpeechTask,
    "Griptape Load: Audio": gtUILoadAudio,
    # Image
    "Griptape Create: Image from Text": gtUIPromptImageGenerationTask,
    "Griptape Create: Image Variation": gtUIPromptImageVariationTask,
    "Griptape Create: Image Inpainting Variation": gtUIInpaintingImageGenerationTask,
    "Griptape Run: Image Description": gtUIImageQueryTask,
    "Griptape Run: Parallel Image Description": gtUIParallelImageQueryTask,
    "Griptape Load: Image From URL": gtUIFetchImage,
    # CODE
    "Griptape Code: Run Griptape Cloud Structure": gtUICloudStructureRunTask,
    "Griptape Code: Run Python [DEPRECATED]": gtUICodeExecutionTask,
    # TEXT
    "Griptape Create: Text": gtUIInputStringNode,
    "Griptape Create: CLIP Text Encode": gtUICLIPTextEncode,
    "Griptape Convert: Text to CLIP Encode": gtUITextToClipEncode,
    "Griptape Convert: Text to Combo": gtUITextToCombo,
    "Griptape Combine: Merge Texts": MergeTexts,
    "Griptape Combine: Merge Inputs": gtUIMergeInputs,
    "Griptape Load: Text": gtUILoadText,
    "Griptape Save: Text": gtUISaveText,
    "Griptape Run: Text Extraction": gtUIExtractionTask,
    "Griptape Run: Text Summary": gtUITextSummaryTask,
    "Griptape Vector Store: Add Text": gtUIVectorStoreUpsertTextTask,
    "Griptape Vector Store: Query": gtUIVectorStoreQueryTask,
    # "Griptape Display: Artifact": gtUIOutputArtifactNode,
    # "Griptape Config: Environment Variables": gtUIEnv,
    # RAG
    "Griptape RAG: Engine": gtUIRagEngine,
    "Griptape Combine: RAG Module List": gtUIModuleList,
    "Griptape RAG Query: Translate Module": gtUITranslateQueryRagModule,
    "Griptape RAG Retrieve: Text Loader Module": gtUITextLoaderRetrievalRagModule,
    "Griptape RAG Retrieve: Vector Store Module": gtUIVectorStoreRetrievalRagModule,
    "Griptape RAG Rerank: Text Chunks Module": gtUITextChunksRerankRagModule,
    "Griptape RAG Response: Prompt Module": gtUIPromptResponseRagModule,
    "Griptape RAG Response: Text Chunks Module": gtUITextChunksResponseRagModule,
    "Griptape RAG Response: Footnote Prompt Module": gtUIFootnotePromptResponseRagModule,
    # CHAT
    "Griptape Chat": gtUIChat,
}


__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]
print("   \033[34m- \033[92mDone!\033[0m\n")
