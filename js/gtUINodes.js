import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";
import { ComfyDialog } from "../../../scripts/ui/dialog.js";
import { GriptapeConfigDialog } from "./gtUIConfigDialog.js";

function chainCallback(object, property, callback) {
    if (object == undefined) {
        //This should not happen.
        console.error("Tried to add callback to non-existant object")
        return;
    }
    if (property in object) {
        const callback_orig = object[property]
        object[property] = function () {
            const r = callback_orig.apply(this, arguments);
            callback.apply(this, arguments);
            return r
        };
    } else {
        object[property] = callback;
    }
}

async function uploadFile(file) {
    //TODO: Add uploaded file to cache with Cache.put()?
    try {
        // Wrap file in formdata so it includes filename
        const body = new FormData();
        const i = file.webkitRelativePath.lastIndexOf('/');
        const subfolder = file.webkitRelativePath.slice(0,i+1)
        const new_file = new File([file], file.name, {
            type: file.type,
            lastModified: file.lastModified,
        });
        body.append("image", new_file);
        if (i > 0) {
            body.append("subfolder", subfolder);
        }
        const resp = await api.fetchApi("/upload/image", {
            method: "POST",
            body,
        });

        if (resp.status === 200) {
            return resp.status
        } else {
            alert(resp.status + " - " + resp.statusText);
        }
    } catch (error) {
        alert(error);
    }
}

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
      {
        content: "Griptape Discord",
        callback: (...args) => {
          window.open("https://discord.gg/gnWRz88eym", "_blank");
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
function gtUIAddUploadWidget(nodeType, nodeData, widgetName, type="audio") {
    chainCallback(nodeType.prototype, "onNodeCreated", function() {
        const pathWidget = this.widgets.find((w) => w.name === widgetName);
        const fileInput = document.createElement("input");
        chainCallback(this, "onRemoved", () => {
            fileInput?.remove();
        });
        if (type == "folder") {
            Object.assign(fileInput, {
                type: "file",
                style: "display: none",
                webkitdirectory: true,
                onchange: async () => {
                    const directory = fileInput.files[0].webkitRelativePath;
                    const i = directory.lastIndexOf('/');
                    if (i <= 0) {
                        throw "No directory found";
                    }
                    const path = directory.slice(0,directory.lastIndexOf('/'))
                    if (pathWidget.options.values.includes(path)) {
                        alert("A folder of the same name already exists");
                        return;
                    }
                    let successes = 0;
                    for(const file of fileInput.files) {
                        if (await uploadFile(file) == 200) {
                            successes++;
                        } else {
                            //Upload failed, but some prior uploads may have succeeded
                            //Stop future uploads to prevent cascading failures
                            //and only add to list if an upload has succeeded
                            if (successes > 0) {
                                break
                            } else {
                                return;
                            }
                        }
                    }
                    pathWidget.options.values.push(path);
                    pathWidget.value = path;
                    if (pathWidget.callback) {
                        pathWidget.callback(path)
                    }
                },
            });
        } else if (type == "video") {
            Object.assign(fileInput, {
                type: "file",
                accept: "video/webm,video/mp4,video/mkv,image/gif",
                style: "display: none",
                onchange: async () => {
                    if (fileInput.files.length) {
                        if (await uploadFile(fileInput.files[0]) != 200) {
                            //upload failed and file can not be added to options
                            return;
                        }
                        const filename = fileInput.files[0].name;
                        pathWidget.options.values.push(filename);
                        pathWidget.value = filename;
                        if (pathWidget.callback) {
                            pathWidget.callback(filename)
                        }
                    }
                },
            });
        } else if (type == "audio") {
            Object.assign(fileInput, {
                type: "file",
                accept: "audio/mpeg,audio/wav,audio/x-wav,audio/ogg",
                style: "display: none",
                onchange: async () => {
                    if (fileInput.files.length) {
                        if (await uploadFile(fileInput.files[0]) != 200) {
                            //upload failed and file can not be added to options
                            return;
                        }
                        const filename = fileInput.files[0].name;
                        pathWidget.options.values.push(filename);
                        pathWidget.value = filename;
                        if (pathWidget.callback) {
                            pathWidget.callback(filename)
                        }
                    }
                },
            });
        }else {
            throw "Unknown upload type"
        }
        document.body.append(fileInput);
        let uploadWidget = this.addWidget("button", "choose " + type + " to upload", "image", () => {
            //clear the active click event
            app.canvas.node_widget = null

            fileInput.click();
        });
        uploadWidget.options.serialize = false;
    });
}
app.registerExtension({
  name: "comfy.gtUI",

  init() {},
  beforeRegisterNodeDef(nodeType, nodeData, app) {
    // if (nodeData.category.startsWith("Griptape")) {
    //   const origOnConfigure = nodeType.prototype.onConfigure;
    //   nodeType.prototype.onConfigure = function () {
    //     this.bgcolor = "#171717";
    //     this.color = getColor(nodeData.category);
    //   };

    //   const onNodeCreated = nodeType.prototype.onNodeCreated;
    //   nodeType.prototype.onNodeCreated = function () {
    //     const r = onNodeCreated?.apply(this, arguments);
    //     this.bgcolor = "#171717";
    //     this.color = getColor(nodeData.category);
    //     this.onResize?.(this.size);
    //     return r;
    //   };
    // }
    if (nodeData.name === "gtUILoadAudio") {
      gtUIAddUploadWidget(nodeType, nodeData, "audio", "audio")
      console.log("I found it!")
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
        // w.inputEl.style.backgroundColor = "#070707";

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
});

export const griptapenodes = new GriptapeNodes();
window.griptapenodes = griptapenodes;
