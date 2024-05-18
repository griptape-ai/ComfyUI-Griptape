# ComfyUI Griptape Nodes

This repo creates a series of nodes that enable you to utilize the [Griptape Python Framework](https://github.com/griptape-ai/griptape/) with [ComfyUI](https://github.com/comfyanonymous/ComfyUI), integrating AI into your workflow.

It has a subset of Griptape nodes, including nodes for:

* Creating [Agents](https://docs.griptape.ai/stable/griptape-framework/structures/agents/)
    * OpenAI
    * Amazon Bedrock 
    * Google Gemini
    * Anthropic Claude
* [Image Generation](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#image-generation-tasks)
    * OpenAI
    * Amazon Bedrock Stable Diffusion
    * Amazon Bedrock Titan
    * Leonardo.AI
* [Image Querying](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#image-query-task)
* Image Variation (in beta)
* Tools
    * [Calculator](https://docs.griptape.ai/stable/griptape-tools/official-tools/calculator/)
    * [DateTime](https://docs.griptape.ai/stable/griptape-tools/official-tools/date-time/)
    * [WebScraper](https://docs.griptape.ai/stable/griptape-tools/official-tools/web-scraper)
    * [ FileManager ](https://docs.griptape.ai/stable/griptape-tools/official-tools/web-scraper)

## Installation

#### 1. ComfyUI

Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI) using the [instructions](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#installing) for your particular operating system.

#### 2. Install Griptape-ComfyUI

There are two methods for installing the Griptape-ComfyUI repository. You can either download or git clone this repository inside the `ComfyUI/custom_nodes`, or use the [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager).

* Option A - **ComfyUI Manager** _(Recommended)_

    1. Install ComfyUI Manager by following the [installation instructions](https://github.com/ltdrdata/ComfyUI-Manager#installation).
    2. Click **Manager** in ComfyUI to bring up the ComfyUI Manager
    3. Click **Install via Git URL**
    4. Enter the URL for ComfyUI-Griptape: https://github.com/griptape-ai/ComfyUI-Griptape
    5. Click **OK**
    6. Follow the rest of the instructions.

* Option B - **Git Clone**

    1. Open a terminal and input the following commands:

        ```
        cd /path/to/comfyUI
        cd custom_nodes
        git clone https://github.com/griptape-ai/ComfyUI-Griptape
        ```

#### 3. Make sure libraries are loaded

There are required libraries for the ComfyUI-Griptape nodes. They're called out in the requirements.txt file:

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


#### 4. Add API keys to your Environment

Certain API keys are required for various nodes to work. It's recommended to add these to a `.env` file in your base comfyUI folder before you start ComfyUI. 

_Note: Most nodes will work fine with just the `OPENAI_API_KEY`, so at least make sure you have that one._

```bash
OPENAI_API_KEY=
GOOGLE_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
LEONARDO_API_KEY=
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

## Troubleshooting

#### API Keys

When you run ComfyUI with the Griptape nodes installed, the installation method will check your environment variables and automatically install the appropriate API keys in a file called: `griptape.config.json`.

If for some reason your environment variables aren't being set properly, you can do this manually by simply copying over the `griptape.config.json.default` file to `griptape.config.json` and add the proper keys there.

If you ever need to change your API keys, go ahead and update that configuration file with the proper key.

#### Webscraper

The WebScraper tool uses [ Markdownify ](https://docs.griptape.ai/stable/reference/griptape/drivers/web_scraper/markdownify_web_scraper_driver/). 

The `playwright` browser should get installed automatically when you install the Griptape Nodes, but if it doesn't you may need to install this manually to get it to work.

In your terminal, execute the following code:

    ```bash
    playwright install
    ```
