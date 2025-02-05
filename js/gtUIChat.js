import { commentWidget, bodyWidget } from "./utils.js";
import { api } from "../../../scripts/api.js";
import { app } from "../../../scripts/app.js";
// Global store for incoming messages per node
const incoming_data = {};
const messagePromises = {};
const agents = {};
const agent_response_widgets = {};

// Using a promise to be able to wait for messages
function messageHandler(event) {
  console.log("Event detail: ", event.detail);
  const { text_context, agent, id } = event.detail;
  agents[id] = agent;
  incoming_data[id] = { text_context };
  // If there's a pending promise for this ID, resolve it
  if (messagePromises[id]) {
    messagePromises[id].resolve(incoming_data[id]);
    delete messagePromises[id];
  }
}

// TO FIX: This is not streaming as expected
function streamChatMessageHandler(event) {
  const { text_context, id } = event.detail;
  // console.log("Stream handler called with id:", id);
  const node = app.graph._nodes_by_id[id];
  const agent_response_widget = node.widgets.find(
    (w) => w.name === "agent_response"
  );
  const agent_output_widget = node.widgets.find(
    (w) => w.name === "agent_output"
  );

  // the text_context should be json, split it into the response and prompt
  const { response, prompt } = JSON.parse(text_context);
  agent_response_widget.value = response;
  agent_output_widget.value = prompt;
  // Try both node and graph dirty canvas
  node.setDirtyCanvas(true);
  if (node.graph) {
    node.graph.setDirtyCanvas(true);
  }

  // console.log(agent_response_widget);
}

function waitForMessage(id, timeout = 20000) {
  return new Promise((resolve, reject) => {
    // If we already have the data, return it immediately
    if (incoming_data[id]) {
      return resolve(incoming_data[id]);
    }

    // Otherwise, store the promise resolvers
    messagePromises[id] = { resolve, reject };

    // Add timeout
    setTimeout(() => {
      if (messagePromises[id]) {
        delete messagePromises[id];
        reject(new Error(`Timeout waiting for message for node ${id}`));
      }
    }, timeout);
  });
}

// create a listner for the chat node event
api.addEventListener("griptape.chat_node", messageHandler);
api.addEventListener("griptape.stream_chat_node", streamChatMessageHandler);

// Setup the Chat Node itself
export function setupChatNode(nodeType, nodeData, app) {
  if (nodeData.name.includes("Griptape Chat")) {
    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = async function () {
      onNodeCreated?.apply(this, arguments);

      // ----------------------------------------------------------
      // Grab Widgets and Inputs

      // Headers and Body Widgets
      const commentWidgets = this.widgets.filter((w) =>
        w.name.toLowerCase().includes("comment")
      );
      commentWidgets.forEach((widget) => commentWidget(this, widget));
      const bodyWidgets = this.widgets.filter((w) =>
        w.name.toLowerCase().includes("body")
      );
      bodyWidgets.forEach((widget) => bodyWidget(this, widget));

      // Inputs
      const agent = this.inputs.find((i) => i.name === "agent");
      const text_context_input = this.inputs.find(
        (i) => i.name === "text_context"
      );

      // Message Widgets
      const user_message_widget = this.widgets.find(
        (w) => w.name === "user_message"
      );
      const agent_response_widget = this.widgets.find(
        (w) => w.name === "agent_response"
      );
      agent_response_widgets[this.id] = agent_response_widget;
      console.log("Setting widget for id:", this.id, agent_response_widget);

      const agent_output_widget = this.widgets.find(
        (w) => w.name === "agent_output"
      );

      // Get the output_selector input
      const output_selector_widget = this.widgets.find(
        (w) => w.name === "output_selector"
      );

      // ----------------------------------------------------------
      // Initialize conversation history
      this.conversationHistory = [];
      this.output_history = [];

      // Add callback to output_selector
      output_selector_widget.callback = (value) => {
        const index = parseInt(value);
        if (index >= 0 && index < this.output_history.length) {
          agent_output_widget.value = this.output_history[index];
        }
      };

      // Function to handle clearing chat
      const clearChat = () => {
        this.conversationHistory = [];
        this.output_history = [];
        user_message_widget.value = "";
        agent_response_widget.value = "";
        agent_output_widget.value = "";
        output_selector_widget.value = 0;
        output_selector_widget.callback?.(0);
      };

      // Function to refresh context
      const refreshContext = async () => {
        app.queueNodeIds = [this.id];
        await app.queuePrompt();

        try {
          const messageData = await waitForMessage(this.id);
        } catch (error) {
          console.error("Failed to get message:", error);
          incoming_data[this.id] = null;
        }

        app.queueNodeIds = null;
      };

      // ----------------------------------------------------------
      // Function to handle sending message
      const sendMessage = async () => {
        if (user_message_widget && user_message_widget.value?.trim()) {
          try {
            const userMessage = user_message_widget.value;
            const text_context_input = this.inputs.find(
              (i) => i.name === "text_context"
            );
            // console.log("context: ", text_context_input);
            this.conversationHistory.push({
              role: "User",
              message: userMessage,
            });
            let context = null;
            if (text_context_input.link) {
              // Text_context_input has a link
              // Checking to see if there's any already stored data.
              context = incoming_data[this.id];
              if (!context) {
                // There was no stored data, so we need to refresh the context
                const msg = await refreshContext();
                context = incoming_data[this.id];
              }
            } else {
              // There's no link, so let's make sure we don't pass any context.
              context = {
                text_context: "NO CONTEXT",
              };
            }

            // Show loading state
            agent_response_widget.value = "🤔 Thinking...";

            // Make API call
            const response = await fetch("/Griptape/prompt_chat", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                user_message: userMessage,
                conversation_history: this.conversationHistory,
                context: context,
                prev_agent_output: agent_output_widget,
                node_id: this.id,
                agent: agents[this.id],
              }),
            });

            response.body.cancel(); // Cancel the body since we're sending events
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }

            // TEMPORRILY REMOVE GETTING THE RESPONSE
            // // Get response data
            // const data = await response.json();
            // // Update agent response
            // let responseText = data.response || "No response received";
            // agent_response_widget.value = responseText;
            // // Add assistant response to history
            // this.conversationHistory.push({
            //   role: "Assistant",
            //   message: data.response || "No response received",
            // });

            // // Update prompt output if provided
            // if (data.prompt) {
            //   // check and see if the prompt is the same as the most recent prompt in the history
            //   // if it is, then don't add it to the history
            //   if (
            //     this.output_history.length === 0 ||
            //     this.output_history[this.output_history.length - 1] !==
            //       data.prompt
            //   ) {
            //     this.output_history.push(data.prompt);
            //   }
            //   agent_output_widget.value = data.prompt;
            //   let current_index = this.output_history.length - 1;
            //   output_selector_widget.value = this.output_history.length - 1;
            //   // Tell ComfyUI these widgets need redrawing
            //   output_selector_widget.callback?.(output_selector_widget.value);
            //   this.setDirtyCanvas(true);
            // }
          } catch (error) {
            console.error("Error:", error);
            agent_response_widget.value =
              "## Error\nFailed to get response from agent";
            agent_output_widget.value =
              "Error occurred while generating prompt";
          }

          // Select the message text for easy replacement
          setTimeout(() => {
            const textareas = document.querySelectorAll("textarea");
            for (let textarea of textareas) {
              if (textarea.value === user_message_widget.value) {
                textarea.focus();
                textarea.select();
                break;
              }
            }
          }, 100);
        }
      };

      // Add enter key handler to the textarea
      setTimeout(() => {
        const textareas = document.querySelectorAll("textarea");
        for (let textarea of textareas) {
          textarea.addEventListener("keydown", (e) => {
            // Check if it's the prompt textarea
            if (textarea.value === user_message_widget.value) {
              if (e.key === "Enter" && e.shiftKey) {
                e.preventDefault(); // Prevent new line
                sendMessage();
              }
            }
          });
        }
      }, 100);

      // Add RefreshButton
      this.addWidget("button", "Refresh Context", null, refreshContext);
      // Add clear button
      this.addWidget("button", "Clear Chat", null, clearChat);
    };
    setTimeout(() => {
      nodeType.prototype.computeSize = function () {
        return [400, 500];
      };
    }, 100);
  }
}
