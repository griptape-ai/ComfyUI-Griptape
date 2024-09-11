import { ComfyWidgets } from "../../../scripts/widgets.js";
import { fitHeight } from "./utils.js";
import { formatAndDisplayJSON } from "./gtUIUtils.js";
export function setupDisplayNodes(nodeType, nodeData, app) {
    if (nodeData.name === "Griptape Display: Artifact") {
      setupArtifactDisplayNode(nodeType, nodeData, app);
    } else if (nodeData.name === "Griptape Display: Text") {
      setupTextDisplayNode(nodeType, nodeData, app);
    } else if (nodeData.name === "Griptape Display: Data as Text") {
      setupDataAsTextDisplayNode(nodeType, nodeData, app);
    }
  }
  
  function setupArtifactDisplayNode(nodeType, nodeData, app) {
    nodeType.prototype.onNodeCreated = function() {
      this.message = ComfyWidgets.STRING(this, 'Output Text', ['STRING', { multiline: true }], app).widget;
      this.message.value = "";
      setupMessageStyle(this.message);
      fitHeight(this, true);
    };
  
    nodeType.prototype.onExecuted = function(message) {
      updateMessageValue(this, message["INPUT"].join(""));
      // this.onResize?.(this.size);
      this?.graph?.setDirtyCanvas(true, true);
    };
  }
  
  function setupTextDisplayNode(nodeType, nodeData, app) {
    nodeType.prototype.onExecuted = function(message) {
      let stringWidget = this.widgets.find(w => w.name === "STRING");
      if (stringWidget && message.hasOwnProperty("INPUT")) {
        let new_val = Array.isArray(message["INPUT"]) ? message["INPUT"].join("") : String(message["INPUT"]);
        if (typeof new_val === 'string' && new_val.trim() !== "") {
          stringWidget.value = new_val;
          // this.size[1] = Math.max(this.size[1], new_val.split("\n").length * 20 + 40);
        }
      }
      this.onResize?.(this.size);
      this.setDirtyCanvas(true, true);
    };
  }
  
  function setupDataAsTextDisplayNode(nodeType, nodeData, app) {
    nodeType.prototype.onNodeCreated = function() {
      this.message = ComfyWidgets.STRING(this, 'Output Text', ['STRING', { multiline: true }], app).widget;
      this.message.value = "";
      setupMessageStyle(this.message);
      fitHeight(this);
    };
  
    nodeType.prototype.onExecuted = function(message) {
      if (this.widgets.find(w => w.type === "customtext")) {
        const new_val = message["INPUT"].join("");
        let formattedJSON = formatAndDisplayJSON(new_val);
        updateMessageValue(this, formattedJSON);
      }
      this.onResize?.(this.size);
      this?.graph?.setDirtyCanvas(true, true);
    };
  }
  
  function setupMessageStyle(message) {
    message.inputEl.style.borderRadius = "8px";
    message.inputEl.style.padding = "8px";
    message.inputEl.style.height = "100%";
    message.inputEl.classList.add("language-python");
  }
  
  function updateMessageValue(node, value) {
    node.message.value = value;
    node.message.inputEl.scrollTop = node.message.inputEl.scrollHeight;
  }