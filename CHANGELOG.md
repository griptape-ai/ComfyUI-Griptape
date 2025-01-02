# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- ## [Unreleased]

### Added 
### Changed 
### Deprecated 
### Removed 
### Fixed 
### Security  -->

## [2.1.01] - 2025-03-01
### Fixed
- Updated `attrs` library to `>=24.3.0`

## [2.1.00] - 2025-03-01
### Changed
- Updated Griptape Framework to 1.1.0
- Updated Poetry to version 1.8.5
- Set default `max_attempts_on_fail` for prompt drivers to 2 instead of 10.
### Removed
- `Griptape Code: Run Python` node was echoing code to console.log. This has been removed.

## [2.0.17] - 2025-02-01
### Fixed
- Updated text when running Python code is not enabled.
### Removed
- in `gtUICodeExecutionTask.py` removed unused `unique_id` variable.

## [2.0.16] - 2025-02-01
### Added
- [Example](examples/README.md#sorting-a-csv---by-using-generic-python) for using the `Griptape Code: Run Python` node.
  ![](examples/sort_list_with_python_code.png)
### Fixed
- Templates not listed for `Griptape Code: Run Python` node.

## [2.0.15] - 2025-02-01
### Added 
- `Griptape Code: Run Griptape Cloud Structure` - Runs a structure from [Griptape Cloud Structures](https://cloud.griptape.ai/structures). Requires a `GRIPTAPE_CLOUD_API_KEY` and a `structure_id`. 
- `Griptape Code: Run Python` - Creates a node that lets you execute Python code. The output of the node is any data supplied to the `output` variable.
- `Code Execution Templates` - A list of templated code examples the user can pick from.
- `Griptape Settings`
  - `Enable Griptape Code: Run Python Nodes` - user option to enable the `Griptape Code: Run Python` node
  - `Enable Insecure Griptape Code: Run Python [DANGER]` - additional user option to skip any checking for dangerous code. Recommended to keep this OFF - and only enable it if you know what you're doing.
### Fixed 
- `@Griptape` was missing from settings due to a ComfyUI change. Renamed to `Griptape`.


## [2.0.14] - 2025-01-01
### Fixed
- Griptape settings restored. It was not showing up with the name `@Griptape` so I renamed the category to `!Griptape`.

## [2.0.13] - 2024-31-12
### Fixed
- Quick fix for CHANGELOG link in release notes.

## [2.0.12] - 2024-31-12
### Added
- Updated CHANGELOG.md
- Standard testing for spelling errors, Typing, and more.

### Removed
- Manual version tracking in `versions.js` and instead am pulling information from `pyproject.toml`
- `griptape_config.py`


## Historical Changelog

Entries below were recorded before moving to this new `CHANGELOG.md` method.

### Dec 31, 2024
 * Removed manual version tracking in versions.js and now pulling the information from the `pyproject.toml`. To see what version you're running, choose RMB -> Griptape and look at the `Version` information.
 * Removed `griptape_config.py` as it's no longer being used
 * Added testing to catch spelling, type, and other errors. _Note_: This was a massive effort - hopefully it didn't introduce any errors.

### Dec 27, 2024
 * Fixed missing classmethod for OllamaPromptDriver
 
### Dec 24, 2024
 * Fixed missing api key for OpenAI when getting a list of available models.
 * Removed Ollama's model check using the library in favor of a javascript option.
 
### Dec 21, 2024
 * Fixed issue where Griptape Agent Config: Custom Structure node was still requiring OPENAI_API_KEY.
 * Updated to Griptape v1.0.2
 * OpenAi, Anthropic, and Ollama nodes pull directly from their apis now to get the available models.
 * Added check to ensure Ollama not running doesn't cause Griptape Nodes to fail.
 
### Dec 12, 2024
 * Updated to Griptape Framework 1.0! 
 * Added check for BlackForest install issues to not block Griptape Nodes running

### Nov 30, 2024
* New Nodes:
  * `Griptape Driver: Black Forest Labs Image Generation` - Now generate images with the incredible Flux models - `flux-pro-1.1`, `flux-pro`, `flux-dev`, and `flux-pro-1.1-ultra`. 
    - Requires an API_KEY from Black Forest Labs (https://docs.bfl.ml/)
    - Utilizes new Griptape Extension: https://github.com/griptape-ai/griptape-black-forest
  
  ![Black Forest Labs - Create Image](examples/griptape_black_forest_labs_create_image.png)
   
    - It also works with the `Griptape Create: Image Variation` node.

    ![Black Forest Labs - Image Variation](examples/griptape_black_forest_labs_create_variation.png)

  * `Griptape Create: Image Inpainting Variation` to the Griptape -> Image menu. Gives the ability to paint a mask and replace that part of the image.
  
  ![Black Forest Labs - Inpainting](examples/griptape_black_forest_flux_inpainting.png)

### Nov 29, 2024
* Iterating on configuration settings to improve compatibility with ComfyUI Desktop

### Nov 28, 2024
* ⚠️ **Temporarily removed BlackForestLabs Driver nodes while resolving install issues**. There appears to be an installation issue for these nodes, so I'm _temporarily_ removing them until it's resolved.
* Removed old configuration settings - now relying completely on ComfyUI's official settings

### Nov 27, 2024

* Added example: [PDF -> Profile Pic](examples/pdf_to_profile_pic.png) where a resume in pdf form is summarized, then used as inspiration for an image generation prompt to create a profile picture.

* Fixed: `gtUIKnowledgeBaseTool` was breaking if a Griptape Cloud Knowledge Base had an `_` in the name. It now handles that situation.

### Nov 26, 2024
* Upgrade to Griptape Framework v0.34.3
* New Nodes:
  * `Griptape Create: Image Inpainting Variation` to the Griptape -> Image menu. Gives the ability to paint a mask and replace that part of the image.
  
  ![Inpainting](examples/inpainting.png)

  * `Griptape Run: Task` - Combines/Replaces `Griptape Run: Prompt Task`, `Griptape Run: Tool Task`, and `Griptape Run Toolkit Task` into a single node that knows what to do.
  * `Griptape Run: Text Extraction` to the Griptape -> Text menu
* Added `keep_alive` parameter to `Ollama Prompt Driver` to give the user the ability to control how long to keep the model running. Setting it to 0 will do the same as an `ollama stop <model>` command-line execution. Default setting is 240 seconds to match the current default.

* Moved node: `Griptape Run: Text Summary` to the Griptape -> Text menu
* Updated `Griptape RAG Retrieve: Text Loader Module` to take a file input or text input.
* Fixed ExtractionTool to use a default of `gpt-4o-mini`
* Added some text files for testing text loading
* Added Examples to [Examples Readme](examples/README.md)
  * [Render Log Review](examples/render_log_review.png)
  * [Flux Pro 1.1 Image Generation](examples/griptape_black_forest_labs_create_image.png)
  * [Flux Pro 1.0-Canny Image Variation](examples/griptape_black_forest_labs_create_variation.png)
  * [Flux Pro 1.0-Fill Image InPainting](examples/griptape_black_forest_flux_inpainting.png)

### Nov 9, 2024
* Upgrade to Griptape Framework v0.34.2
* Fixed combine nodes breaking when re-connecting output

### Nov 6, 2024
* Upgrade to Griptape Framework v0.34.1
  * Fix to `WebScraperTool` provides better results when using `off_prompt`.
* Fixed bug where urls were dropping any text after the `:`. Example: "What is https://griptape.ai" was being converted to "What is https:". This is due to the `dynamicprompt` functionality of ComfyUI, so I've disabled that.
* Added context string to all BOOLEAN parameters to give the user a better idea as to what the particular boolean option does. For example, instead of just `True` or `False`, the tools now explain `off_prompt`.

  ![WebsScraper tool with off_prompt](docs/images/off_prompt_parameter.png)

### Nov 4, 2024
* Fixed bug where OPENAI_API_KEY was still required, and was causing some install issues.
* Added video to README with how to manage api keys.

### Nov 1, 2024
* Major reworking of how API keys are set. Now you can use the ComfyUI Settings window and add your API keys there. This should simplify things quite a bit as you no longer need to create a `.env` file in your ComfyUI folder.

  * Note: Existing environment variables will be picked up automatically.

  ![Griptape Settings](docs/images/griptape_settings.png)

### Oct 31, 2024
* Added tooltips for all drivers to help clarify properties
* Added fix for Ollama Driver Config so it wouldn't fail if no embedding driver was specified.
* Fix for Convert Agent to Tool node.

### Oct 30, 2024
* Updated to Griptape Framework v0.34.0
* **Breaking Changes**
  * `AnthropicDriversConfig` node no longer includes Embedding Driver. If you wish to use Claude within a RAG pipeline, build a `Config: Custom Structure` using a Prompt Driver, Embedding Driver, and Vector Store Driver. See the attached image for an example:
  
    ![alt text](docs/images/anthropic_custom_structure.png)  

### Oct 23, 2024
* Updated Anthropic Claude Prompt Driver to include `claude-3-5-sonnet-20241022`
* Updated Anthropic Claude Config to offer option to not use Voyage API for Embedding Driver. Just set `ignore_voyage_embedding_driver` to `True`

### Oct 11, 2024
* Updated to Griptape Framework v0.33.1 to resolve install bugs

### Oct 10, 2024
* Updated to Griptape Framework v0.33
* Added `TavilyWebSearchDriver`. Requires a Tavily [api key](https://app.tavily.com/).
* Added `ExaWebSearchDriver`. Requires an Exa [api key](https://dashboard.exa.ai/api-keys). 

### Sept 20, 2024
* Hotfix for `Griptape Agent Config: LM Studio Drivers`. The `base_url` parameter wasn't being set properly causing a connection error. 

### Sept 12, 2024
* Hotfix for `Griptape Run: Tool Task` node. It now properly handles the output of the tool being a list.

### Sept 11, 2024
* Added `top_p` and `top_k` to Anthropic and Google Prompt Drivers
* Fixed automatic display node text resizing
* Fixed missing display of the Env node

### Sept 10, 2024
* **New Nodes** Griptape now has the ability to generate new models for `Ollama` by creating a Modelfile. This is an interesting technique that allows you to create new models on the fly.
  * `Griptape Util: Create Agent Modelfile`. Given an agent with rules and some conversation as an example, create a new Ollama Modelfile with a SYSTEM prompt (Rules), and MESSAGES (Conversation).
  * `Griptape Util: Create Model from Modelfile`. Given a Modelfile, create a new Ollama model.
  * `Griptape Util: Remove Ollama Model`. Given an Ollama model name, remove the model from Ollama. This will help you cleanup unnecessary models. _Be Careful with this one, as there is no confirmation step!_

  ![Create New Model](examples/createNewModel.png)

### Sept 5, 2024
**MAJOR UPDATE**
* Update to Griptape Framework to v0.31.0

* There are some New Configuration Drivers nodes! These new nodes replace the previous `Griptape Agent Config` nodes (which still exist, but have been deprecated). They display the various drivers that are available for each general config, and allow you to make changes per driver. See the image for examples:

![alt text](docs/images/release_030_2_config_nodes.png)

* Old `Griptape Agent Config` nodes still exist, but have been deprecated. They will be removed in a future release. Old workflows should automatically display the older nodes as deprecated. It's **highly recommended** to replace these old nodes with the new ones. I have tried to minimize breaking nodes, but if some may exist. I apologize for this if it happens.

![alt text](docs/images/config_deprecated.png)

* New Nodes
  * `Griptape Agent Config: Cohere Drivers`: A New Cohere node.
  * `Griptape Agent Config: Expand`: A node that lets you expand Config Drivers nodes to get to their individual drivers.
  * `Griptape RAG Nodes` a whole new host of nodes related to Retrieval Augmented Generation (RAG). I've included a sample in the [examples](examples/retrieval_augmented_generation.json) folder that shows how to use these nodes. 
  
  The new nodes include:
    * `Griptape RAG: Tool` - A node that lets you create a tool for RAG.
    * `Griptape RAG: Engine` - A node that lets you create an engine for RAG containing multiple stages. Learn more here: https://docs.griptape.ai/stable/griptape-framework/engines/rag-engines/:
      * Query stage - a stage that allows you to manipulate a user's query before RAG starts.
      * Retrieval stage - the stage where you gather the documenents and vectorize them. This stage can contain multiple "modules" which can be used to gather documents from different sources.
      * Rerank stage - a stage that re-ranks the results from the retrieval stage.
      * Response stage - a stage that uses a prompt model to generate a response to the user's question. It also includes multiple modules.
    * `Griptape Combine: RAG Module List` - A node that lets you combine modules for a stage.
    * Various Modules:
      * `Griptape RAG Query: Translate Module` - A module that translates the user's query into another language.
      * `Griptape RAG Retrieve: Text Loader Module` - A module that lets you load text and vectorize it in real time.
      * `Griptape RAG Retrieve: Vector Store Module` - A module that lets you load text from an existing Vector Store.
      * `Griptape RAG Rerank: Text Chunks Module` - A module that re-ranks the text chunks from the retrieval stage.
      * `Griptape RAG Response: Prompt Module` - Uses an LLM Prompt Driver to generate a response.
      * `Griptape RAG Response: Text Chunks Module` - Just responds with Text Chunks.
      * `Griptape RAG Response: Footnote Prompt Module` - A Module that ensures proper footnotes are included in the response.

### Aug 30, 2024
* Added `max_tokens` to most configuration and prompt_driver nodes. This gives you the ability to control how many tokens come back from the LLM. _Note: It's a known issue that AmazonBedrock doesn't work with max_tokens at the moment._
* Added `Griptape Tool: Extraction` node that lets you extract either json or csv text with either a json schema or column header definitions. This works well with TaskMemory.
* Added `Griptape Tool: Prompt Summary` node that will summarize text. This works well with TaskMemory.

### Aug 29, 2024
* Updated griptape version to 0.30.2 - This is a major change to how Griptape handles configurations, but I tried to ensure all nodes and workflows still work. Please let us know if there are any issues.
* Added `Griptape Tool: Query` node to allow Task Memory to go "Off Prompt"

### Aug 27, 2024
* Fixed bugs where inputs of type "*" weren't working
* Updated frontend display of type `string` for `Griptape Display: Data as Text` node.

### Aug 21, 2024
* Fixed querying for models in LMStudio and Ollama on import

### Aug 20, 2024
* Update Griptape Framework to v029.2
* Modified ImageQueryTask to switch to a workflow if more than 2 images are specified
* Updated tests

### Aug 4, 2024
* Updating Griptape Framework to v029.1
* Added `Griptape Config: Environment Variables` node to allow you to add environment variables to the graph
* Added `Griptape Text: Load` node to load a text file from disk
* Added Ollama Embedding Model
* Added GriptapeCloudKnowledgeBaseVectorStoreDriver that allows you to query a knowledge base in Griptape Cloud. Requires a Griptape Cloud account (https://cloud.griptape.ai), a Data Source, and a Knowledge Base. Also requires an API key: `GRIPTAPE_CLOUD_API_KEY` that you can get from your [Griptape Cloud API Page](https://cloud.griptape.ai/account/api-keys).


### Aug 3, 2024
* Reverted ollama and lmstudio configuration nodes to a list of installed models using new method for grabbing them. 

### July 29, 2024
* Temporarily replaceing the ollama config nodes with a string input for specifying the model instead of a list of installed models.

### July 27, 2024
* Updated menu items to be in a better order. Please provide feedback!

### July 25, 2024
* Added separators to menu items in the RMB->Griptape menu to help group similar items.

### July 24, 2024
* Added default colors to help differentiate between types of nodes. Tried to keep it minimal and distinct.
  * Agent support nodes (Rules, Tools, Drivers, Configurations): `Blue`
    Rationale: Blue represents stability and foundational elements. Using it for all agent-supporting nodes shows their interconnected nature.
  
  * Agents: `Purple`
    Rationale: Purple often represents special or unique elements. This makes Agents stand out as the central, distinct entities in the system.

  * Tasks: `Red`
    Rationale: Red signifies important actions, fitting for task execution nodes.

  * Output nodes: `Black`
    Rationale: Black provides strong contrast, suitable for final output display.

  * Utility nodes (Merge, Conversion, Text creation, Loaders): No color (`gray`)
    Rationale: Keeping utility functions in a neutral color helps reduce visual clutter and emphasizes their supporting role.

* **New Node** SaveText. This is a simple SaveText node as requested by a user. Please check it out and give feedback.
    
### July 23, 2024
* Fixed bug with VectorStoreDrivers that would cause ComfyUI to fail loading if no OPENAI_API_KEY was present.

### July 22, 2024
* **New Nodes** A massive amount of new nodes, allowing for ultimate configuration of an Agent.
  * **Griptape Agent Configuration**
    * **Griptape Agent: Generic Structure** - A Generic configuration node that lets you pick any combination of `prompt_driver`, `image_generation_driver`, `embedding_driver`, `vector_store_driver`, `text_to_speech_driver`, and `audio_transcription_driver`.
    * **Griptape Replace: Rulesets on Agent** - Gives you the ability to replace or remove rulesets from an Agent.
    * **Griptape Replace: Tools on Agent** - Gives you the ability to replace or remove tools from an Agent

  * **Drivers**
    * **Prompt Drivers** - Unique chat prompt drivers for `AmazonBedrock`, `Cohere`, `HuggingFace`, `Google`, `Ollama`, `LMStudio`, `Azure OpenAi`, `OpenAi`, `OpenAiCompatible`
    * **Image Generation Drivers** - These all existed before, but adding here for visibility: `Amazon Bedrock Stable Diffusion`, `Amazon Bedrock Titan`, `Leonardo AI`, `Azure OpenAi`, `OpenAi`
    * **Embedding Drivers** - Agents can use these for generating embeddings, allowing them to extract relevant chunks of data from text. `Azure OpenAi`, `Voyage Ai`, `Cohere`, `Google`, `OpenAi`, `OpenAi compatible`
    * **Vector Store Drivers** - Allows agents to access Vector Stores to query data: ``Azure MongoDB`, `PGVector`, `Pinecone`, `Amazon OpenSearch`, `Qdrant`, `MongoDB Atlas`, `Redis`, `Local Vector Store`
    * **Text To Speech Drivers** - Gives agents the ability to convert text to speech. `OpenAi`, `ElevenLabs`
    * **Audio Transcription Driver** - Gives agents the ability to transcribe audio. `OpenAi`
    * re-fixed spelling of `Compatible`, because it's a common mistake. :)

  * **Vector Store** - New Vector Store nodes - `Vector Store Add Text`, `Vector Store Query`, and `Griptape Tool: VectorStore` to allow you to work with various Vector Stores

  * **Environment Variables parameters** - all nodes that require environmetn variables & api keys have those environment variables specified on the nodes. This should make it easier to know what environment variables you want to set in `.env`.

  * **Examples** - Example workflows are now available in the `/examples` folder [here](examples/README.md).

* **Breaking Change**
  * There is no longer a need for an `ImageQueryDriver`, so the `image_query_model` input has been removed from the configuration nodes. 
  * Due to how comfyUI handles input removal, the values of non-deleted inputs on some nodes may be broken. Please double-check your values on these Configuration nodes.
  
### July 17, 2024
* Simplified API Keys by removing requirements for `griptape_config.json`. Now all keys are set in `.env`.
* Fixed bug where Griptape wouldn't launch if no `OPENAI_API_KEY` was set.

### July 16, 2024
* Reorganized all the nodes so each class is in it's own file. should make things easier to maintain
* Added `max_attemnpts_on_fail` parameter to all Config nodes to allow the user to determine the number of retries they want when an agent fails. This maps to the `max_attempts` parameter in the Griptape Framework.
* **NewNode**: Audio Driver: Eleven Labs. Uses the ElevenLabs api. Takes a model, a voice, and the ELEVEN_LABS_API_KEY. https://elevenlabs.io/docs/voices/premade-voices#current-premade-voices
* **NewNode**: Griptape Run: Text to Speech task
* **NewNode**: Added AzureOpenAI Config node. To use this, you'll need to set up your Azure endpoint and get API keys. The two environment variables required are `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`. You will also require a [deployment name](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/switching-endpoints). This is available in [Azure OpenAI Studio](https://oai.azure.com/)
* Updated README

### July 12, 2024
* Updated to Griptape v0.28.2
* **New Node** Griptape Config: OpenAI Compatible node. Allows you to connect to services like https://www.ohmygpt.com/ which are compatible with OpenAi's api.
* **New Node** HuggingFace Prompt Driver Config
* Reorganized a few files
* Removed unused DuckDuckGoTool now that Griptape supports drivers.

### July 11, 2024
* The Display Text node no longer clears it's input if you disconnect it - which means you can use it as a way to generate a prompt, and then tweak it later.
* Added Convert Agent to Tool node, allowing you to create agents that have specific skills, and then give them to another agent to use when it feels it's appropriate.

### July 10, 2024

* Updated to work with Griptape v0.28.1
* Image Description node now can handle multiple images at once, and works with Open Source llava.
* Fixed tool, config, ruleset, memory bugs for creating agents based on update to v0.28.0
* **New Nodes** Added WebSearch Drivers: DuckDuckGo and Google Search. To use Google Search, you must have two API keys - GOOGLE_API_KEY and GOOGLE_API_SEARCH_ID. 

### July 9, 2024

* Updated LMStudio and Ollama config nodes to use 127.0.0.1
* Updated `Create Agent` and `Run Agent` nodes to no longer cache their knowledge between runs. Now if the `agent` input isn't connected to anything, it will create a new agent on each run.

### July 2, 2024

* All input nodes updated with dynamic inputs. Demonstration here: https://youtu.be/1fHAzKVPG4M?si=6JHe1NA2_a_nl9rG
* Fixed bug with Text to Combo node
