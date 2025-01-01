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
import { gtUIAddUploadWidget } from "./gtUIUtils.js";
import { setupMenuSeparator } from "./gtUIMenuSeparator.js";
import { keys_organized } from "./griptape_api_keys.js";
import { setupVisibilityToggles } from "./NodesWithVisibilityToggles.js";
import { setupCodeExecutionNode } from "./CodeExecutionNode.js";  
import { gtUIAddButtonWidget } from "./gtUIUtils.js";
function addGriptapeTopBarButtons() {
  const buttons = [];
  const griptapeButton = new ComfyButton({
    tooltip: "Griptape",
    app,
    enabled: true,
    classList: "comfyui-button comfyui-menu-mobile-collapse primary",
});
  console.log(griptapeButton);
}
app.registerExtension({
  name: "comfy.gtUI",
  addGriptapeTopBarButtons,
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
      tooltip: "To set this, use the Griptape: Set Default Agent node.",
    });
    app.ui.settings.addSetting({
      id: `Griptape.allow_code_execution_dangerous`,
      category: ["Griptape", "!Griptape", "code_execution_dangerous"],
      name: "Enable Insecure Griptape Code: Run Python [DANGER]",
      type: "boolean",
      tooltip: "When enabled, the Griptape Code: Run Python node will not check for dangerous code.\n\n[WARNING] This setting is dangerous and should only be enabled if you know what you are doing.",
      defaultValue: false,
      onChange: (newVal, oldVal) => { if (newVal == true) { console.warn("Griptape Code: Dangerous Code Execution enabled: ", newVal)} },
    });
    app.ui.settings.addSetting({
      id: `Griptape.allow_code_execution`,
      category: ["Griptape", "!Griptape", "code_execution"],
      name: "Enable Griptape Code: Run Python Nodes",
      type: "boolean",
      tooltip: "When enabled, the `Griptape Code: Run Python` node will be available for use.",
      defaultValue: false,
      // onChange: (newVal, oldVal) => { console.log("Setting got changed!", newVal) },
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
    // Run Griptape Structure Nodes
    if (nodeData.name === "Griptape Code: Run Griptape Structure") {
      gtUIAddButtonWidget(nodeType, "Open Griptape Structure Dashboard", createUrlCallback("https://cloud.griptape.ai/structures"))
    }
    // Add Conductor Dashboard Widgets
    // add a button that will open a url in a new tab
    
    // if (nodeData.name === "Griptape LoRA: Train using Conductor") {
    //   gtUIAddButtonWidget(nodeType, "Open Conductor Dashboard", createUrlCallback("https://dashboard.conductortech.com/"))
    // }
    // if (nodeData.name === "Griptape LoRA: Download Job") {
    //   gtUIAddUrlButtonWidget(nodeType, "Open Conductor Job Dashboard", "https://dashboard.conductortech.com/job", "job_id")
    // }

  },
});
