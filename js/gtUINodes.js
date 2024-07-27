import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { nodeFixes } from "./nodeFixes.js";
import { setupConfigurationNodes } from "./ConfigurationNodes.js";
import { setupNodeColors } from "./ColorNodes.js";
import { setupDisplayNodes } from "./DisplayNodes.js";
import { setupCombineNodes } from "./CombineNodes.js";
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
