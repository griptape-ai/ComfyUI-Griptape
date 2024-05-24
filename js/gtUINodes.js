import { app } from "../../../scripts/app.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";
import { ComfyDialog } from "../../../scripts/ui/dialog.js";
import { GriptapeConfigDialog } from "./gtUIConfigDialog.js";

class GriptapeNodes extends EventTarget {
  constructor() {
    super();
    this.initializeContextMenu();
    this.injectGriptapeCss();
  }
  async initializeContextMenu() {
    const that = this;
    setTimeout(async () => {
      const getCanvasMenuOptions = LGraphCanvas.prototype.getCanvasMenuOptions;
      LGraphCanvas.prototype.getCanvasMenuOptions = function (...args) {
        const options = getCanvasMenuOptions.apply(this, [...args]);
        options.push(null);
        options.push({
          content: `💬  Griptape`,
          // className: "gtUI-contextmenu-item gtUI-contextmenu-main-item",
          submenu: {
            options: that.getGriptapeContextMenuItems(),
          },
        });

        // Remove consecutive null entries
        let i = 0;
        while (i < options.length) {
          if (options[i] === null && (i === 0 || options[i - 1] === null)) {
            options.splice(i, 1);
          } else {
            i++;
          }
        }
        return options;
      };
    }, 1000);
  }
  getGriptapeContextMenuItems() {
    const that = this;
    return [
      // TODO: Figure out how to pull and set the environment variables
      // {
      //   content: "⚙️ Environment Variables",
      //   callback: (...args) => {
      //     const dialog = new GriptapeConfigDialog();
      //     dialog.show();
      //   },
      // },
      {
        content: "⭐ Star on Github",
        callback: (...args) => {
          window.open(
            "https://github.com/griptape-ai/ComfyUI-Griptape",
            "_blank"
          );
        },
      },
      {
        content: "",
        disabled: true,
      },
      {
        content: "Griptape Home",
        callback: (...args) => {
          window.open("https://griptape.ai", "_blank");
        },
      },
      {
        content: "Griptape Cloud",
        callback: (...args) => {
          window.open("https://cloud.griptape.ai", "_blank");
        },
      },
      {
        content: "Griptape Docs",
        callback: (...args) => {
          window.open("https://docs.griptape.ai", "_blank");
        },
      },
      {
        content: "Griptape Tradeschool",
        callback: (...args) => {
          window.open("https://learn.griptape.ai", "_blank");
        },
      },
    ];
  }

  injectGriptapeCss() {
    let link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = "extensions/ComfyUI-Griptape/gtUI.css";
    document.head.appendChild(link);
  }
}
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
  // nodeCreated(node) {
  //   if (node.category.startsWith("gtUI")) {
  //     node.color = getColor(node.category);
  //   }
  // },
});

export const griptapenodes = new GriptapeNodes();
window.griptapenodes = griptapenodes;
