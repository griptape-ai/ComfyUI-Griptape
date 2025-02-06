# pyright: reportMissingImports=false
import asyncio

import schema
from aiohttp import web
from griptape.drivers import (
    OpenAiChatPromptDriver,
)
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.utils import Stream
from json_repair import repair_json
from rich.pretty import pprint as pprint
from server import PromptServer

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
            node_id = data.get("node_id", "")
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
            if not agent_dict:
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
                run_items.append(f"Contextual information: {text_context}")
            run_items.append("Conversation history:")
            run_items.append(conversation_history)
            if prev_agent_output.strip() != "":
                run_items.append(
                    f"Your last pass at the prompt was: {prev_agent_output}"
                )
            if message.strip() != "":
                run_items.append(f"User: {message}")

            # Run the async request
            async def stream_response():
                response_data = ""
                for artifact in Stream(agent).run(run_items):
                    response_data += artifact.value
                    await request.app.loop.run_in_executor(
                        None,
                        PromptServer.instance.send_sync,
                        "griptape.stream_chat_node",
                        {
                            "text_context": repair_json(response_data),
                            "id": node_id,
                        },
                    )
                # Now we need to send a complete event.. something like:
                await request.app.loop.run_in_executor(
                    None,
                    PromptServer.instance.send_sync,
                    "griptape.stream_chat_complete",
                    {
                        "text_context": repair_json(str(agent.output.value)),
                        "id": node_id,
                    },
                )

            # Run the streaming in the background
            asyncio.create_task(stream_response())

            # Return an immediate success response
            return web.Response(status=200)

            # Now I need to send the final output and continue the rest of the script.
            print(agent.output.value)
            # Return an empty response to unblock the fetch
            return web.Response()

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
