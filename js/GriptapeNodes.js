import { griptapeMenuItems } from "./gtUIContextMenu.js";

export class GriptapeNodes extends EventTarget {
  constructor() {
    super();
    this.initializeContextMenu();
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
    return griptapeMenuItems;
  }

  injectGriptapeCss() {
    let link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = "extensions/ComfyUI-Griptape/gtUI.css";
    document.head.appendChild(link);
  }
}

// Instantiate and export GriptapeNodes
export const griptapeNodes = new GriptapeNodes();

// Make it available globally if needed
if (typeof window !== 'undefined') {
  window.griptapeNodes = griptapeNodes;
}

