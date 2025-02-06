import { app } from "../../../scripts/app.js";
import { ComfyButtonGroup } from "../../scripts/ui/components/buttonGroup.js";
import { ComfyButton } from "../../scripts/ui/components/button.js";

import { api } from "../../../scripts/api.js";
import { nodeFixes } from "./nodeFixes.js";
import { setupConfigurationNodes } from "./ConfigurationNodes.js";
import { setupNodeColors } from "./ColorNodes.js";
import { setupDisplayNodes } from "./DisplayNodes.js";
import { setupCombineNodes } from "./CombineNodes.js";
import { setupExtractionNodes } from "./ExtractionNodes.js";
import { setupTextLoaderModuleNodes } from "./TextLoaderModuleNodes.js";
import { setupChatNode } from "./gtUIChat.js";
import {
  gtUIAddUploadWidget,
  gtUIAddUrlButtonWidget,
  gtUIAddButtonWidget,
} from "./gtUIUtils.js";
import { setupMenuSeparator } from "./gtUIMenuSeparator.js";
import { keys_organized } from "./griptape_api_keys.js";
import { setupVisibilityToggles } from "./NodesWithVisibilityToggles.js";
import { setupCodeExecutionNode } from "./CodeExecutionNode.js";
import { setupApiKeyButtons } from "./apiKeyButtons.js";
import { createSettings } from "./settings.js";
const createUrlCallback = function (url) {
  return function () {
    window.open(url, "_blank"); // Opens the provided URL in a new tab
  };
};

// function addGriptapeTopBarButtons() {
//   const buttons = [];
//   const griptapeButton = new ComfyButton({
//     tooltip: "Griptape",
//     app,
//     enabled: true,
//     classList: "comfyui-button comfyui-menu-mobile-collapse primary",
//   });
//   console.log(griptapeButton);
// }
app.registerExtension({
  name: "comfy.gtUI",
  // addGriptapeTopBarButtons,
  beforeConfigureGraph: (graphData, missingNodeTypes) => {
    for (let node of graphData.nodes) {
      if (nodeFixes.fixes[node.type]) {
        node.type = nodeFixes.fixes[node.type];
      }
    }
  },
  setup: (app) => {
    setupMenuSeparator();
    function messageHandler(event) {
      console.log(event.detail.message);
    }
    function runStreamMessageHandler(event) {
      const { id, text_context, widget } = event.detail;
      const node = app.graph._nodes_by_id[id];
      const output_widget = node.widgets.find((w) => w.name === widget);
      if (!output_widget) {
        return;
      }
      output_widget.value = text_context;
      node.setDirtyCanvas(false);
      // output_widget.value = text_context;
    }
    api.addEventListener("comfy.gtUI.runagent", messageHandler);
    api.addEventListener("griptape.stream_agent_run", runStreamMessageHandler);

    createSettings(app);
  },

  init() {},
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    setupChatNode(nodeType, nodeData, app);
    setupNodeColors(nodeType, nodeData, app);
    setupConfigurationNodes(nodeType, nodeData, app);
    setupDisplayNodes(nodeType, nodeData, app);
    setupCombineNodes(nodeType, nodeData, app);
    setupExtractionNodes(nodeType, nodeData, app);
    setupVisibilityToggles(nodeType, nodeData, app);
    setupCodeExecutionNode(nodeType, nodeData, app);
    setupApiKeyButtons(nodeType, nodeData, app);
    // Create Audio Node
    if (nodeData.name === "Griptape Load: Audio") {
      gtUIAddUploadWidget(nodeType, nodeData, "audio", "audio");
    }
    // Load Text Node
    if (nodeData.name === "Griptape Load: Text") {
      gtUIAddUploadWidget(nodeType, nodeData, "text", "text");
    }
    if (nodeData.name === "Griptape RAG Retrieve: Text Loader Module") {
      gtUIAddUploadWidget(nodeType, nodeData, "file_path", "text");
    }
    setupTextLoaderModuleNodes(nodeType, nodeData, app);

    if (nodeData.name === "Griptape Code: Run Griptape Cloud Structure") {
      gtUIAddUrlButtonWidget(
        nodeType,
        "Open Griptape Cloud Structure Dashboard",
        "https://cloud.griptape.ai/structures",
        "structure_id"
      );
    }
    if (nodeData.name === "Griptape Run: Cloud Assistant") {
      gtUIAddUrlButtonWidget(
        nodeType,
        "Open Griptape Cloud Assistant Dashboard",
        "https://cloud.griptape.ai/assistants",
        "assistant_id"
      );
    }
    if (nodeData.name === "Griptape Retrieve: Cloud Ruleset") {
      gtUIAddUrlButtonWidget(
        nodeType,
        "Open Griptape Cloud Ruleset Dashboard",
        "https://cloud.griptape.ai/rulesets",
        "ruleset_id"
      );
    }
  },
});
