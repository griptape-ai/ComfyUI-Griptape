# ComfyUI Griptape Nodes

This repo creates a series of nodes that enable you to utilize the [Griptape Python Framework](https://github.com/griptape-ai/griptape/) with [ComfyUI](https://github.com/comfyanonymous/ComfyUI), integrating LLMs (Large Language Models) and AI into your workflow.

### Instructions and tutorials

Watch the trailer and all the instructional videos on our [YouTube Playlist](https://www.youtube.com/playlist?list=PLZRzNKLLiEyeK9VN-i53sUU1v5vBLl-nG).

[![Watch the Trailer on YouTube](docs/images/playlist.png)](https://www.youtube.com/playlist?list=PLZRzNKLLiEyeK9VN-i53sUU1v5vBLl-nG)

The repo currently has a subset of Griptape nodes, with more to come soon. Current nodes can:

* Create [Agents](https://docs.griptape.ai/stable/griptape-framework/structures/agents/) that can chat using these models:
    * Local - via **Ollama** and **LM Studio**
        * Llama 3
        * Mistral
        * etc..
    * Via Paid API Keys
        * OpenAI
        * Azure OpenAI
        * Amazon Bedrock 
        * Cohere
        * Google Gemini
        * Anthropic Claude
        * Hugging Face (_Note: Not all models featured on the Hugging Face Hub are supported by this driver. Models that are not supported by Hugging Face serverless inference will not work with this driver. Due to the limitations of Hugging Face serverless inference, only models that are than 10GB are supported._)

* Control agent behavior and personality with access to [Rules and Rulesets](https://docs.griptape.ai/stable/griptape-framework/structures/rulesets/).
* Give Agents access to [Tools](https://docs.griptape.ai/stable/griptape-tools/):
    * [Calculator](https://docs.griptape.ai/stable/griptape-tools/official-tools/calculator/)
    * [DateTime](https://docs.griptape.ai/stable/griptape-tools/official-tools/date-time/)
    * [WebScraper](https://docs.griptape.ai/stable/griptape-tools/official-tools/web-scraper)
    * [FileManager](https://docs.griptape.ai/stable/griptape-tools/official-tools/file-manager)
    * [AudioTranscriptionClient](https://docs.griptape.ai/stable/griptape-tools/official-tools/audio-transcription-client/)
    * [GriptapeCloudKnowledgeBaseClient](https://docs.griptape.ai/stable/reference/griptape/tools/#griptape.tools.GriptapeCloudKnowledgeBaseClient)
    * [GriptapeVectorStoreClient](https://docs.griptape.ai/stable/griptape-tools/official-tools/vector-store-client/)

* Run specific Agent Tasks:
    * [PromptTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#prompt-task)
    * [TextSummaryTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#text-summary-task)
    * [ToolTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#tool-task)
    * [ToolkitTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#toolkit-task)
    * [PromptImageGenerationTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#prompt-image-generation-task)
    * [ImageQueryTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#image-query-task)
    * [VariationImageGenerationTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#variation-image-generation-task) (In Beta)
    * [AudioTranscriptionTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#audio-transcription-task)
    * [TextToSpeechTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#text-to-speech-task)

* [Generate Images](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#image-generation-tasks) using these models:
    * OpenAI
    * Amazon Bedrock Stable Diffusion
    * Amazon Bedrock Titan
    * Leonardo.AI

* Audio
    * Transcribe Audio
    * Text to Voice

## Ultimate Configuration

Use nodes to control every aspect of the Agents behavior, with the following drivers:
* Prompt Driver
* Image Generation Driver
* Embedding Driver
* Vector Store Driver
* Text to Speech Driver
* Audio Transcription Driver

![Workflow to configure an agent](docs/images/Griptape-Agent-Configurations.svg)

## Example

In this example, we're using three `Image Description` nodes to describe the given images. Those descriptions are then `Merged` into a single string which is used as inspiration for creating a new image using the `Create Image from Text` node, driven by an `OpenAI Driver`.

The following image is a workflow you can drag into your ComfyUI Workspace, demonstrating all the options for configuring an Agent.

![Three image descriptions being used to generate a new image](docs/images/image_descriptions_to_image.png)

## More examples

You can previous and download more examples [here](examples/README.md).

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
18. Persistent Display Text: https://youtu.be/9229bN0EKlc?si=Or2eu3Nuh7lxgfEU
19. Convert an Agent to a Tool.. and give it to another Agent: https://youtu.be/CcRot5tVAU8?si=lA0v5kDH51nYWwgG
20. Text-To-Speech Nodes: https://youtu.be/PP1uPkRmvoo?si=QSaWNCRsRaIERrZ4
21. Update to Managing Your API Keys in ComfyUI Griptape Nodes: https://www.youtube.com/watch?v=v80A7rtIjko

## Recent Changelog

Please view recent changes [here](CHANGELOG.md).

## Installation

#### 1. ComfyUI

Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI) using the [instructions](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#installing) for your particular operating system.

#### 2. Use Ollama

If you'd like to run with a local LLM, you can use Ollama and install a model like llama3.

1. Download and install Ollama from their website: https://ollama.com
2. Download a model by running `ollama run <model>`. For example:

   `ollama run llama3`

3. You now have ollama available to you. To use it, follow the instructions in this YouTube video: https://youtu.be/jIq_TL5xmX0?si=0i-myC6tAqG8qbxR

#### 3. Install Griptape-ComfyUI

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


#### 4. Make sure libraries are loaded

Libraries should be installed automatically, but if you're having trouble, hopefully this can help.

There are certain libraries required for Griptape nodes that are called out in the requirements.txt file.

```bash
griptape[all]
python-dotenv
```

These should get installed automatically if you used the ComfyUI Manager installation method. However, if you're running into issues, please install them yourself either using `pip` or `poetry`, depending on your installation method.

* Option A - **pip**

    ```bash
    pip install "griptape[all]" python-dotenv 
    ```

* Option B - **poetry**

    ```bash
    poetry add "griptape[all]" python-dotenv 
    ```

#### 5. Restart ComfyUI

Now if you restart comfyUI, you should see the Griptape menu when you click with the Right Mouse button. 

If you don't see the menu, please come to our [Discord](https://discord.gg/fexDeKxf) and let us know what kind of errors you're getting - we would like to resolve them as soon as possible!

#### 6. Set API Keys

For advanced features, it's recommended to use a more powerful model. These are available from the providers listed bellow, and will require API keys.

1. To set an API key, click on the `Settings` button in the **ComfyUI Sidebar**.
2. Select the `Griptape` option.
3. Scroll down to the API key you'd like to set and enter it.
   
   *Note: If you already have a particular API key set in your environment, it will automatically show up here.*

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
* COHERE_API_KEY: https://dashboard.cohere.com/api-keys
* ELEVEN_LABS_API_KEY: https://elevenlabs.io/app/
    * Click on your username in the lower left
    * Choose **Profile + API Key**
    * Generate and copy the API key
* GRIPTAPE_CLOUD_API_KEY: https://cloud.griptape.ai/configuration/api-keys

---

## Troubleshooting

### Torch issues

Griptape does install the `torch` requirement. Sometimes this may cause problems with ComfyUI where it grabs the wrong version of `torch`, especially if you're on Nvidia. As per the ComfyUI docs, you may need to unintall and re-install `torch`.

```
pip uninstall torch
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
```

### Griptape Not Updating

Sometimes you'll find that the Griptape library didn't get updated properly. This seems to be especially happening when using the ComfyUI Manager. You might see an error like:

```
ImportError: cannot import name 'OllamaPromptDriver' from 'griptape.drivers' (C:\Users\evkou\Documents\Sci_Arc\Sci_Arc_Studio\ComfyUi\ComfyUI_windows_portable\python_embeded\Lib\site-packages\griptape\drivers\__init__.py)

```

To resolve this, you must make sure Griptape is running with the appropriate version. Things to try:

* Update again via the ComfyUI Manager
* Uninstall & Re-install the Griptape nodes via the ComfyUI Manager
* In the terminal, go to your ComfyUI directory and type: `python -m pip install griptape -U`
* Reach out on [Discord](https://discord.gg/fexDeKxf) and ask for help.

### StabilityMatrix

If you are using [StabilityMatrix](https://github.com/LykosAI/StabilityMatrix) to run ComfyUI, you may find that after you install Griptape you get an error like the following:
![Stability Matrix Error](docs/images/stability_matrix_error.png)

To resolve this, you'll need to update your torch installation. Follow these steps:

1. Click on **Packages** to go back to your list of installed Packages.
2. In the **ComfyUI** card, click the vertical `...` menu.
3. Choose **Python Packages** to bring up your list of Python Packages.
4. In the list of Python Packages, search for `torch` to filter the list.
5. Select **torch** and click the `-` button to uninstall `torch`.
6. When prompted, click **Uninstall**
7. Click the `+` button to install a new package.
8. Enter the list of packages: `torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121`
9. Click **OK**.
10. Wait for the install to complete.
11. Click **Close**.
12. Launch ComfyUI again.

---

## Thank you

Massive thank you for help and inspiration from the following people and repos!

* Jovieux from https://github.com/Amorano/Jovimetrix
* rgthree https://github.com/rgthree/rgthree-comfy
* IF_AI_tools https://github.com/if-ai/ComfyUI-IF_AI_tools/tree/main
