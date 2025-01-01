import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { nodeFixes } from "./nodeFixes.js";
import { setupConfigurationNodes } from "./ConfigurationNodes.js";
import { setupNodeColors } from "./ColorNodes.js";
import { setupDisplayNodes } from "./DisplayNodes.js";
import { setupCombineNodes } from "./CombineNodes.js";
import { setupExtractionNodes } from "./ExtractionNodes.js";
import { setupTextLoaderModuleNodes } from "./TextLoaderModuleNodes.js";
import { gtUIAddUploadWidget } from "./gtUIUtils.js";
import { setupMenuSeparator } from "./gtUIMenuSeparator.js";
import { keys_organized } from "./griptape_api_keys.js";
import { setupVisibilityToggles } from "./NodesWithVisibilityToggles.js";
import { setupCodeExecutionNode } from "./CodeExecutionNode.js";  
app.registerExtension({
  name: "comfy.gtUI",
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
      // console.log(event.detail.message)
    }
    api.addEventListener("comfy.gtUI.runagent", messageHandler);

    // Create the settings
    app.ui.settings.addSetting({
      id: `Griptape.default_config`,
      category: ["Griptape", "!Griptape", "default_config"],
      name: "default_config",
      type: "dict",
      defaultValue: "",
    });
    app.ui.settings.addSetting({
      id: `Griptape.allow_code_execution`,
      category: ["Griptape", "Griptape", "code_execution"],
      name: "Enable Code Execution Nodes",
      type: "boolean",
      defaultValue: false,
    });
    Object.entries(keys_organized).forEach(([category, keys]) => {
      keys.forEach((key) => {
        app.ui.settings.addSetting({
          id: `Griptape.${key}`,
          category: ["Griptape", category, key],
          name: key,
          type: "text",
          defaultValue: "",
          /* To listen for changes, add an onChange parameter
        onChange: (newVal, oldVal) => { console.log("Setting got changed!") },
        */
        });
      });
    });
  },

  init() {},
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    setupNodeColors(nodeType, nodeData, app);
    setupConfigurationNodes(nodeType, nodeData, app);
    setupDisplayNodes(nodeType, nodeData, app);
    setupCombineNodes(nodeType, nodeData, app);
    setupExtractionNodes(nodeType, nodeData, app);
    setupVisibilityToggles(nodeType, nodeData, app);
    setupCodeExecutionNode(nodeType, nodeData, app);

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
  },
});
