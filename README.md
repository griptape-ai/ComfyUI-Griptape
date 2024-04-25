# ComfyUI Griptape Nodes

This repo creates a series of nodes that enable you to utilize the Griptape Python Framework with ComfyUI, integrating AI into your workflow.

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

### Installation notes

* There are required libraries for the ComfyUI-Griptape nodes. They're called out in the requirements.txt file:
    * `griptape[all]`
    * `python-dotenv`

* Certain API keys are required for various nodes to work. It's recommended to add these to a `.env` file before you run comfyUI in your base comfyUI folder.

```
OPENAI_API_KEY=
GOOGLE_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
LEONARDO_API_KEY=
GROQ_API_KEY=
```

* Alternatively, copy the file `griptape_config.json.default` to `griptape.config.json` and add the environment variables there.

* The WebScraper tool uses [ Markdownify ](https://docs.griptape.ai/stable/reference/griptape/drivers/web_scraper/markdownify_web_scraper_driver/). You may need to install the `playwright` browser to get this to work. 

    ```bash
    playwright install
    ```
