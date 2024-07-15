# ComfyUI Griptape Nodes

This repo creates a series of nodes that enable you to utilize the [Griptape Python Framework](https://github.com/griptape-ai/griptape/) with [ComfyUI](https://github.com/comfyanonymous/ComfyUI), integrating LLMs (Large Language Models) and AI into your workflow.

### Instructions and tutorials

Watch the trailer and all the instructional videos on our [YouTube Playlist](https://www.youtube.com/playlist?list=PLZRzNKLLiEyeK9VN-i53sUU1v5vBLl-nG).

[![Watch the Trailer on YouTube](docs/images/playlist.png)](https://www.youtube.com/playlist?list=PLZRzNKLLiEyeK9VN-i53sUU1v5vBLl-nG)

The repo currently has a subset of Griptape nodes, with more to come soon. Current nodes can:

* Create [Agents](https://docs.griptape.ai/stable/griptape-framework/structures/agents/) using these models:
    * Local - via **Ollama** and **LM Studio**
        * Llama 3
        * Mistral
        * etc..
    * Via Paid API Keys
        * OpenAI
        * Amazon Bedrock 
        * Google Gemini
        * Anthropic Claude
        * Hugging Face (_Note: Not all models featured on the Hugging Face Hub are supported by this driver. Models that are not supported by Hugging Face serverless inference will not work with this driver. Due to the limitations of Hugging Face serverless inference, only models that are than 10GB are supported._)

* Control agent behavior with access to [Rules and Rulesets][https://docs.griptape.ai/stable/griptape-framework/structures/rulesets/]
* Give Agents access to [Tools](https://docs.griptape.ai/stable/griptape-tools/):
    * [Calculator](https://docs.griptape.ai/stable/griptape-tools/official-tools/calculator/)
    * [DateTime](https://docs.griptape.ai/stable/griptape-tools/official-tools/date-time/)
    * [WebScraper](https://docs.griptape.ai/stable/griptape-tools/official-tools/web-scraper)
    * [FileManager](https://docs.griptape.ai/stable/griptape-tools/official-tools/file-manager)
    * [AudioTranscriptionClient](https://docs.griptape.ai/stable/griptape-tools/official-tools/audio-transcription-client/)
    * [GriptapeCloudKnowledgeBaseClient](https://docs.griptape.ai/stable/reference/griptape/tools/#griptape.tools.GriptapeCloudKnowledgeBaseClient)

* Run specific Agent Tasks:
    * [PromptTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#prompt-task)
    * [TextSummaryTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#text-summary-task)
    * [ToolTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#tool-task)
    * [ToolkitTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#toolkit-task)
    * [PromptImageGenerationTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#prompt-image-generation-task)
    * [ImageQueryTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#image-query-task)
    * [VariationImageGenerationTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#variation-image-generation-task) (In Beta)

* [Generate Images](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#image-generation-tasks) using these models:
    * OpenAI
    * Amazon Bedrock Stable Diffusion
    * Amazon Bedrock Titan
    * Leonardo.AI

* Transcribe Audio
 
## Example

In this example, we're using three `Image Description` nodes to describe the given images. Those descriptions are then `Merged` into a single string which is used as inspiration for creating a new image using the `Create Image from Text` node, driven by an `OpenAI Driver`.

![Three image descriptions being used to generate a new image](docs/images/image_descriptions_to_image.png)

## Using the nodes - Video Tutorials
1. Installation: https://youtu.be/L4-HnKH4BSI?si=Q7IqP-KnWug7JJ5s
2. Griptape Agents: https://youtu.be/wpQCciNel_A?si=WF_EogiZRGy0cQIm 
3. Controlling which LLM your Agents use: https://youtu.be/JlPuyH5Ot5I?si=KMPjwN3wn4L4rUyg
4. Griptape Tools - Featuring Task Memory and Off-Prompt: https://youtu.be/TvEbv0vTZ5Q
5. Griptape Rulesets, and Image Creation:  https://youtu.be/DK16ouQ_vSs
6. Image Generation with multiple drivers: https://youtu.be/Y4vxJmAZcho
7. Image Description, Parallel Image Description: https://youtu.be/OgYKIluSWWs?si=JUNxhvGohYM0YQaK
8. Audio Transcription: https://youtu.be/P4GVmm122B0?si=24b9c4v1LWk_n80T
9. Using Ollama as a Configuration Driver: https://youtu.be/jIq_TL5xmX0?si=ilfomN6Ka1G4hIEp
10. Combining Rulesets: https://youtu.be/3LDdiLwexp8?si=Oeb6ApEUTqIz6J6O
11. Integrating Text: https://youtu.be/_TVr2zZORnA?si=c6tN4pCEE3Qp0sBI
12. New Nodes & Quality of life improvements: https://youtu.be/M2YBxCfyPVo?si=pj3AFAhl2Tjpd_hw
13. Merge Input Data: https://youtu.be/wQ9lKaGWmZo?si=FgboU5iUg82pXRkC
14. Setting default agent configurations: https://youtu.be/IkioCcldEms?si=4uUu-y9UvIJWVBdE
15. Merge Text with dynamic inputs and custom separator: https://youtu.be/1fHAzKVPG4M?si=6JHe1NA2_a_nl9rG 
16. Multiple Image Descriptions and Local Multi-Modal Models: https://youtu.be/KHz7CMyOk68?si=oQXud6NOtNHrXLez
17. WebSearch Node Now Allows for Driver Functionality in Griptape Nodes: https://youtu.be/4_dkfdVUnRI?si=DA4JvegV0mdHXPDP

## Recent Changelog

### July 16, 2024
* Added `max_subtasks` parameter to Create Agent node and Griptape Run: Toolkit Task node to allow users to decide how many subtasks they want the agent to try. Default is 20.
* Added `max_attemnpts_on_fail` parameter to all Config nodes to allow the user to determine the number of retries they want when an agent fails. This maps to the `max_attempts` parameter in the Griptape Framework.
* **NewNode**: Added AzureOpenAI Config node. To use this, you'll need to set up your Azure endpoint and get API keys. The two environment variables required are `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`. You will also require a [deployment name](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/switching-endpoints). This is available in [Azure OpenAI Studio](https://oai.azure.com/)
* Updated README

### July 12, 2024
* Updated to Griptape v0.28.2
* **New Node** Griptape Config: OpenAI Compatable node. Allows you to connect to services like https://www.ohmygpt.com/ which are compatable with OpenAi's api.
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


## Installation

#### 1. ComfyUI

Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI) using the [instructions](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#installing) for your particular operating system.

#### 2. Use Ollama

If you'd like to run with a local LLM, you can use Ollama and install a model like llama3.

1. Download and install Ollama from their website: https://ollama.com
2. Download a model by running `ollama run <model>`. For example:

   `ollama run llama3`

3. You now have ollama available to you.

#### 3. Add API Keys to your environment

For advanced features, it's recommended to use a more powerful model. These are available from the providers listed bellow, and will require API keys.

It's recommended to add these to a `.env` file in your base comfyUI folder before you start ComfyUI. 

_Note: Most nodes will work fine with just the `OPENAI_API_KEY`, so at least make sure you have that one._

```bash
OPENAI_API_KEY=
GOOGLE_API_KEY=
GOOGLE_API_SEARCH_ID=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
LEONARDO_API_KEY=
ANTHROPIC_API_KEY=
VOYAGE_API_KEY=
GRIPTAPE_API_KEY=
HUGGINGFACE_HUB_ACCESS_TOKEN=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
```

You can get the appropriate API keys from these respective sites:

* OPENAI_API_KEY: https://platform.openai.com/api-keys
* GOOGLE_API_KEY: https://makersuite.google.com/app/apikey
* AWS_ACCESS_KEY_ID & SECURITY_ACCESS_KEY:
    * Open the [AWS Console](https://console.aws.amazon.com/)
    * Click on your username near the top right and select **Security Credentials**
    * Click on **Users** in the sidebar
    * Click on your username
    * Click on the **Security Credentials** tab
    * Click **Create Access Key**
    * Click **Show User Security Credentials**
* LEONARDO_API_KEY: https://docs.leonardo.ai/docs/create-your-api-key
* ANTHROPIC_API_KEY: https://console.anthropic.com/settings/keys
* VOYAGE_API_KEY: https://dash.voyageai.com/
* HUGGINGFACE_HUB_ACCESS_TOKEN: https://huggingface.co/settings/tokens
* AZURE_OPENAI_ENDPOINT & AZURE_OPENAI_API_KEY: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/switching-endpoints

#### 4. Install Griptape-ComfyUI

There are two methods for installing the Griptape-ComfyUI repository. You can either download or git clone this repository inside the `ComfyUI/custom_nodes`, or use the [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager).

* Option A - **ComfyUI Manager** _(Recommended)_

    1. Install ComfyUI Manager by following the [installation instructions](https://github.com/ltdrdata/ComfyUI-Manager#installation).
    2. Click **Manager** in ComfyUI to bring up the ComfyUI Manager
    3. Search for "Griptape"
    4. Find the ComfyUI-Griptape repo.
    5. Click **INSTALL**
    6. Follow the rest of the instructions.

* Option B - **Git Clone**

    1. Open a terminal and input the following commands:

        ```
        cd /path/to/comfyUI
        cd custom_nodes
        git clone https://github.com/griptape-ai/ComfyUI-Griptape
        ```


#### 5. Make sure libraries are loaded

Libraries should be installed automatically, but if you're having trouble, hopefully this can help.

There are certain libraries required for Griptape nodes that are called out in the requirements.txt file.

```bash
griptape[all]
python-dotenv
duckduckgo_search
```

These should get installed automatically if you used the ComfyUI Manager installation method. However, if you're running into issues, please install them yourself either using `pip` or `poetry`, depending on your installation method.

* Option A - **pip**

    ```bash
    pip install "griptape[all]" python-dotenv duckduckgo_search
    ```

* Option B - **poetry**

    ```bash
    poetry add "griptape[all]" python-dotenv duckduckgo_search
    ```

#### 6. Restart ComfyUI

Now if you restart comfyUI, you should see the Griptape menu when you click with the Right Mouse button. 

If you don't see the menu, please come to our [Discord](https://discord.gg/fexDeKxf) and let us know what kind of errors you're getting - we would like to resolve them as soon as possible!

---

## Troubleshooting

### Griptape Not Updating

Sometimes you'll find that the Griptape library didn't get updated properly. This seems to be especially happening when using the ComfyUI Manager. You might see an error like:

```
ImportError: cannot import name 'OllamaPromptDriver' from 'griptape.drivers' (C:\Users\evkou\Documents\Sci_Arc\Sci_Arc_Studio\ComfyUi\ComfyUI_windows_portable\python_embeded\Lib\site-packages\griptape\drivers\__init__.py)

```

To resolve this, you must make sure Griptape is runnig with the appropriate version. Things to try:

* Update again via the ComfyUI Manager
* Uninstall & Re-install the Griptape nodes via the ComfyUI Manager
* In the terminal, go to your ComfyUI directory and type: `python -m pip install griptape -U`
* Reach out on [Discord](https://discord.gg/fexDeKxf) and ask for help.

### API Keys

When you run ComfyUI with the Griptape nodes installed, the installation method will check your environment variables and automatically install the appropriate API keys in a file called: `griptape_config.json`.

If for some reason your environment variables aren't being set properly, you can do this manually by simply copying over the `griptape_config.json.default` file to `griptape_config.json` and add the proper keys there.

If you ever need to change your API keys, go ahead and update that configuration file with the proper key.

---

## Thank you

Massive thank you for help and inspiration from the following people and repos!

* Jovieux from https://github.com/Amorano/Jovimetrix
* rgthree https://github.com/rgthree/rgthree-comfy
