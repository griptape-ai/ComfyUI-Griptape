import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { nodeFixes } from "./nodeFixes.js";
import { setupConfigurationNodes } from "./ConfigurationNodes.js";
import { setupNodeColors } from "./ColorNodes.js";
import { setupDisplayNodes } from "./DisplayNodes.js";
import { setupCombineNodes } from "./CombineNodes.js";
import { gtUIAddUploadWidget } from "./gtUIUtils.js";

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
    // Add a separator above these items in the RMB Menu
    const sep_above_items = [
      "Text",
      "Agent Configs",
      "Griptape Convert: Agent to Tool",
      "Griptape Replace: Rulesets on Agent",
      "Griptape Run: Agent",
      "Gripatpe Agent Config: Amazon Bedrock",
      "Griptape Combine: Tool List",
      "Griptape Load: Image From URL",
      "Griptape Run: Image Description",
      "Griptape Run: Audio Transcription",
      "Griptape Convert: Text to CLIP Encode",
      "Griptape Combine: Merge Texts",
      "Griptape Save: Text"
    ]
    const originalAddItem = LiteGraph.ContextMenu.prototype.addItem;
    LiteGraph.ContextMenu.prototype.addItem = function (name, value, options) {
      for (let item of sep_above_items) {
        if (name === item) {
          this.addItem("", null)
        }
      }
      return originalAddItem.apply(this, arguments);
    }

    function messageHandler(event) {
      // console.log(event.detail.message)
    }
    api.addEventListener("comfy.gtUI.runagent", messageHandler);

  },


  init() {

  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    setupNodeColors(nodeType, nodeData, app);
    setupConfigurationNodes(nodeType, nodeData, app);
    setupDisplayNodes(nodeType, nodeData, app);
    setupCombineNodes(nodeType, nodeData, app);

    
    // Create Audio Node
    if (nodeData.name === "Griptape Load: Audio") {
      gtUIAddUploadWidget(nodeType, nodeData, "audio", "audio")
    }
  }
});
