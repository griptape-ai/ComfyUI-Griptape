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
import {  setupMenuSeparator } from "./gtUIMenuSeparator.js";
// app.extensionManager.registerSidebarTab({
//   id: "search",
//   icon: "pi pi-search",
//   title: "search",
//   tooltip: "search",
//   type: "custom",
//   render: (el: HTMLElement) => {
//     el.innerHTML = "<div>Custom search tab</div>";
//   },
// });

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
    
    // app.ui.settings.addSetting({
    //   id: "griptape.env",
    //   name: "Griptape environment variables",
    //   type: "textbox", // "text" is another simple option

    //   defaultValue: "OPENAI_API_KEY=12345",
    //   /* To listen for changes, add an onChange parameter
    //   onChange: (newVal, oldVal) => { console.log("Setting got changed!") },
    //   */
  // });

  },


  init() {

  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    setupNodeColors(nodeType, nodeData, app);
    setupConfigurationNodes(nodeType, nodeData, app);
    setupDisplayNodes(nodeType, nodeData, app);
    setupCombineNodes(nodeType, nodeData, app);
    setupExtractionNodes(nodeType, nodeData, app);
    setupTextLoaderModuleNodes(nodeType, nodeData, app);

    
    // Create Audio Node
    if (nodeData.name === "Griptape Load: Audio") {
      gtUIAddUploadWidget(nodeType, nodeData, "audio", "audio")
    }
    // Load Text Node
    if (nodeData.name === "Griptape Load: Text") {
      gtUIAddUploadWidget(nodeType, nodeData, "text", "text")
    }
  }
});
