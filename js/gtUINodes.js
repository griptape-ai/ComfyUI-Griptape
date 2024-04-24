import { app } from "../../../scripts/app.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

function getColor(category) {
  switch (category) {
    case "Griptape/Tasks":
      return "#315459";
    case "Griptape/Tools":
      return "#3f2e52";
    case "Griptape/Agent":
      return "#573159";
    case "Griptape/Config":
      return "#3b3429";
    case "Griptape/Output":
      return "#262e2e";
    default:
      return "#171717";
  }
}
app.registerExtension({
  name: "comfy.gtUI",

  init() {},
  beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.category.startsWith("Griptape")) {
      const origOnConfigure = nodeType.prototype.onConfigure;
      nodeType.prototype.onConfigure = function () {
        this.bgcolor = "#171717";
        this.color = getColor(nodeData.category);
      };

      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated?.apply(this, arguments);
        this.bgcolor = "#171717";
        this.color = getColor(nodeData.category);
        this.onResize?.(this.size);
        return r;
      };
    }
    if (nodeData.name === "gtUIOutputStringNode") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated?.apply(this, arguments);
        // Custom Text
        const w = ComfyWidgets["STRING"](
          this,
          "Output Text",
          ["STRING", { multiline: true }],
          app
        ).widget;
        w.inputEl.readOnly = true;
        w.inputEl.style.borderRadius = "8px";
        w.inputEl.style.padding = "8px";
        w.inputEl.style.lineHeight = "1.5";
        w.inputEl.style.backgroundColor = "#070707";

        return r;
      };

      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        for (const widget of this.widgets) {
          if (widget.type === "customtext") {
            widget.value = message["INPUT"].join("");
          }
        }

        this.onResize?.(this.size);
      };
    }
  },
  nodeCreated(node) {
    if (node.category.startsWith("Griptape")) {
      node.color = getColor(node.category);
    }
  },
});
