import { commentWidget, bodyWidget } from "./utils.js";

export function setupChatNode(nodeType, nodeData, app) {
  if (nodeData.name.includes("Griptape Chat")) {
    console.log("Setting up Griptape Chat node");

    // nodeData.input = {
    //   required: {
    //     message: ["STRING", { multiline: true }],
    //     chat_history: ["MARKDOWN", { multiline: true }],
    //   },
    // };

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = async function () {
      onNodeCreated?.apply(this, arguments);
      // Find widgets you want to turn into comments
      const commentWidgets = this.widgets.filter((w) =>
        w.name.toLowerCase().includes("comment")
      );
      commentWidgets.forEach((widget) => commentWidget(this, widget));
      // Find widgets you want to turn into body
      const bodyWidgets = this.widgets.filter((w) =>
        w.name.toLowerCase().includes("body")
      );
      bodyWidgets.forEach((widget) => bodyWidget(this, widget));

      const historyWidget = this.widgets.find(
        (w) => w.name === "agent_response"
      );
      const messageWidget = this.widgets.find((w) => w.name === "user_message");

      // messageWidget.name = "prompt";
      // historyWidget.name = "output";
      historyWidget.disabled = true;

      // Function to handle sending message
      const sendMessage = () => {
        console.log("Sending message...");
        if (messageWidget && messageWidget.value?.trim()) {
          let response = `## 🤖 Assistant`;
          response += `\n${messageWidget.value}`;
          response += `\n\n## 🧠 Response`;
          response += `\nThis is where the LLM response will go...`;
          historyWidget.value = response;
          setTimeout(() => {
            const textareas = document.querySelectorAll("textarea");
            for (let textarea of textareas) {
              if (textarea.value === messageWidget.value) {
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
            if (textarea.value === messageWidget.value) {
              if (e.key === "Enter" && e.shiftKey) {
                e.preventDefault(); // Prevent new line
                sendMessage();
              }
            }
          });
        }
      }, 100);

      // Add send button (still keeping this as an alternative)
      this.addWidget("button", "Send", null, sendMessage);
    };
    nodeType.prototype.computeSize = function () {
      return [400, 500];
    };
  }
}
