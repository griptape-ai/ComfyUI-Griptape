# pyright: reportMissingImports=false
import schema
from aiohttp import web
from griptape.drivers import AnthropicPromptDriver, OpenAiChatPromptDriver
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from server import PromptServer

from ..py.griptape_settings import GriptapeSettings
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
            print(f"Data: {data=}")
            message = data.get("user_message", "")
            conversation_history = data.get("conversation_history", "")
            prev_agent_output = data.get("prev_agent_output", "")["value"]
            context = data.get("context", None)

            # print(f"{text_input_sourceNodeId=}, {text_input_outputSlot=}")
            # if (
            #     text_input_sourceNodeId is not None
            #     and text_input_outputSlot is not None
            # ):
            #     print("Executing node")
            #     print()
            #     print()
            #     # Get the current workflow
            #     try:
            #         workflow = PromptServer.instance.get_workflow()
            #         print(f"Workflow: {workflow=}")
            #     except Exception as e:
            #         print(f"Error getting workflow: {e}")
            #     # Try to execute just this node
            #     try:
            #         result = await PromptServer.instance.prompt_queue.execute_node(
            #             text_input_sourceNodeId, workflow
            #         )

            #         # Get the specific output we want
            #         if result:
            #             output_value = result[int(text_input_outputSlot)]
            #             print(f"Node output value: {output_value}")
            #     except Exception as e:
            #         print(f"Error executing node: {e}")
            ruleset = Ruleset(
                name="Prompt Builder",
                rules=[
                    Rule(
                        "You are very good at working with the user to generate unique, concise, and specific prompts"
                    ),
                    Rule("Keep prompts under a paragraph."),
                    Rule(
                        "Iterate together, and when you come up with a good prompt output it with the key 'prompt', otherwise respond with the key 'response'"
                    ),
                    Rule(
                        "You have a conversational and friendly tone. Answer the user's questions, but also try and come up with a prompt they can use."
                    ),
                    Rule(
                        "You are able to receive contextual information from the user - but they need to evaluate incoming nodes first. If they ask something that seems like you should have some, tell them make sure there are incoming nodes and to run the queue at least once."
                    ),
                ],
            )
            settings = GriptapeSettings()
            GROQ_API_KEY = settings.get_settings_key_or_use_env("GROQ_API_KEY")
            ANTHROPIC_API_KEY = settings.get_settings_key_or_use_env(
                "ANTHROPIC_API_KEY"
            )

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
            agent = Agent(
                prompt_driver=groq_prompt_driver,
                output_schema=schema.Schema(
                    {
                        "response": str,
                        "prompt": str,
                    }
                ),
                rulesets=[ruleset],
            )

            result = agent.run(
                [
                    f"Contextual information: {context}",
                    f"Conversation history: {conversation_history}",
                    f"\nYour last pass at the prompt was: {prev_agent_output}",
                    f"\nUser: {message}",
                ]
            )
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
