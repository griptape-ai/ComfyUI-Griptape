# pyright: reportMissingImports=false
import schema
from aiohttp import web
from griptape.drivers import (
    AnthropicPromptDriver,
    OpenAiChatPromptDriver,
)
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from rich.pretty import pprint as print
from server import PromptServer

from ..py.griptape_settings import GriptapeSettings
from .agent.gtComfyAgent import gtComfyAgent
from .get_version import get_version

# Import your route handlers here
from .utilities import get_models


def setup_routes():
    @PromptServer.instance.routes.post("/Griptape/get_models")
    async def get_models_endpoint(request):
        data = await request.json()
        engine = data.get("engine")
        base_ip = data.get("base_ip")
        port = data.get("port")
        models = get_models(engine, base_ip, port)
        return web.json_response(models)

    @PromptServer.instance.routes.get("/Griptape/get_version")
    async def get_version_endpoint(request):
        try:
            version = get_version()
            return web.json_response({"version": version})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    @PromptServer.instance.routes.post("/Griptape/prompt_chat")
    async def prompt_chat(request):
        try:
            # Get the JSON data from the request
            data = await request.json()
            message = data.get("user_message", "")
            conversation_history = data.get("conversation_history", "")
            prev_agent_output = data.get("prev_agent_output", "")["value"]
            context = data.get("context", None)
            agent_dict = data.get("agent", None)
            text_context = context.get("text_context", None)

            ruleset = Ruleset(
                name="Prompt Builder",
                rules=[
                    Rule(
                        "You are very good at working with the user to generate unique, concise, and specific prompts"
                    ),
                    Rule("Keep prompts under a paragraph."),
                    Rule(
                        "Iterate together, and when you come up with a good prompt output it with the key 'prompt', otherwise respond with the key 'response'. If you have a suggestion, use it, don't ask the user if you _should_ use it. Be proactive."
                    ),
                    Rule(
                        "You have a conversational and friendly tone. Answer the user's questions, but also try and come up with a prompt they can use."
                    ),
                    Rule(
                        "You are able to receive contextual information from the user - but they need to evaluate incoming nodes first. If they ask something that seems like you should have some, tell them make sure there are incoming nodes and to run the queue at least once."
                    ),
                ],
            )
            rulesets = [ruleset]
            settings = GriptapeSettings()
            GROQ_API_KEY = settings.get_settings_key_or_use_env("GROQ_API_KEY")
            ANTHROPIC_API_KEY = settings.get_settings_key_or_use_env(
                "ANTHROPIC_API_KEY"
            )
            if not agent_dict:
                groq_prompt_driver = OpenAiChatPromptDriver(
                    api_key=GROQ_API_KEY,
                    base_url="https://api.groq.com/openai/v1",
                    model="llama-3.3-70b-versatile",
                    # stream=True,
                    structured_output_strategy="tool",
                )
                anthropic_prompt_driver = AnthropicPromptDriver(
                    model="claude-3-5-sonnet-latest",
                    api_key=ANTHROPIC_API_KEY,
                    structured_output_strategy="tool",
                )
                prompt_driver = OpenAiChatPromptDriver(model="gpt-4o", stream=True)

            else:
                print("Creating agent from dict\n....")
                new_agent = gtComfyAgent.from_dict(agent_dict)
                prompt_driver = new_agent.prompt_driver
                rulesets = [ruleset]

            agent = Agent(
                prompt_driver=prompt_driver,
                output_schema=schema.Schema(
                    {
                        "response": str,
                        "prompt": str,
                    }
                ),
                rulesets=rulesets,
            )

            run_items = []
            if text_context.strip() != "":
                run_items.append("Contextual information:")
                run_items.append(text_context)
            run_items.append("Conversation history:")
            run_items.append(conversation_history)
            if prev_agent_output.strip() != "":
                run_items.append("Your last pass at the prompt was:")
                run_items.append(prev_agent_output)
            if message.strip() != "":
                run_items.append("User:")
                run_items.append(message)

            # Run the agent
            result = agent.run(run_items)

            # Create your response - for now just a test response
            # print(result.output.value)
            response_data = result.output.value

            # Return JSON response
            return web.json_response(response_data)

        except Exception as e:
            print(f"Error in prompt_chat: {e}")
            return web.json_response({"error": str(e)}, status=500)


# Call this function to set up all routes
def init_routes():
    try:
        setup_routes()
    except Exception as e:
        print(f"Failed to initialize custom routes: {e}")
    print("   \033[34m- Custom routes initialized.\033[0m")
