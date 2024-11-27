# Griptape ComfyUI Examples

## Griptape Agent Configuration
This workflow demonstrates all the options for creating an agent based on various configuration drivers.

![Agent Configuration](Griptape-Agent-Config.png)
Download: [Griptape-Agent-Config.json](Griptape-Agent-Config.json)

## Render Log Review
It's handy to be able to review render logs and quickly understand your next actions to resolve any errors. In this example, Griptape uses Anthropic Claude Sonnet-3.5 to review an Autodesk Maya render log and return a summary of errors and recommended next actions.

![Maya Render Log](render_log_review.png)
Download: [render_log_review.png](render_log_review.png)

## PDF to Profile Pic
Uses `Griptape Load: Text` node to import a PDF of a robot resume, then the `Griptape Text: Summary` node to generate a summary of the text. Next, a Griptape Agent creates a prompt to generate a profile picture for the robot described in the text. Finally, an image is generated using `Black Forest Labs flux-pro-1.1`.

![Profile Pic](pdf_to_profile_pic.png)
Download: [pdf_to_profile_pic.png](pdf_to_profile_pic.png)

## Griptape Expert Photographers
Use Agents as experts in their field to help provide feedback that will generate more advanced outputs. Utilizes multiple models - including Ollama running locally. If you don't have Ollama installed, feel free to use another `prompt_driver`.

![Expert Photographer](Photographer-Workflow-Comparison-Example.png)
Download: [Photographer-Workflow-Comparison-Example.json](Photographer-Workflow-Comparison-Example.json)

## Text to Speech
This example includes two workflows - one which is a simple Text To Speech conversion, and a second that uses an Agent with personality rules, and the ability to search the web for inspiration. 

![Text To Speech](Griptape-Text-to-Speech.png)
Download: [Griptape-Text-to-Speech.json](Griptape-Text-to-Speech.json)

## Off Prompt
This example demonstrates how to use a local model (`llama3.1` in this case) to handle all of the results from the `WebScraper` tool. 

![Off Prompt](OffPrompt.png)
Download: [OffPrompt.json](OffPromopt.json)

## RAG (Retrieval Augmented Generation)
Use Retrieval Augmented Generation to have more control over the data your agents can query. Check out this example which demonstrates multiple data sources, reranking results, and controling the responses.

![RAG](retrieval_augmented_generation.png)
Download: [retrieval_augmented_generation.json](retrieval_augmented_generation.json)