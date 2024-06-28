import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";
import { fitHeight } from "./utils.js";
import { ComfyDialog } from "../../../scripts/ui/dialog.js";
import { GriptapeConfigDialog } from "./gtUIConfigDialog.js";
import { nodeFixes } from "./nodeFixes.js";

/* 
A method that returns the required style for the html 
*/
function get_position_style(ctx, widget_width, y, node_height) {
    const MARGIN = 4;  // the margin around the html element

/* Create a transform that deals with all the scrolling and zooming */
    const elRect = ctx.canvas.getBoundingClientRect();
    const transform = new DOMMatrix()
        .scaleSelf(elRect.width / ctx.canvas.width, elRect.height / ctx.canvas.height)
        .multiplySelf(ctx.getTransform())
        .translateSelf(MARGIN, MARGIN + y);

    return {
        transformOrigin: '0 0',
        transform: transform,
        left: `0px`, 
        top: `0px`,
        position: "absolute",
        maxWidth: `${widget_width - MARGIN*2}px`,
        maxHeight: `${node_height - MARGIN*2}px`,    // we're assuming we have the whole height of the node
        width: `auto`,
        height: `auto`,
    }
}

const tabs=2
// Function to format JSON and display it in the textarea
function formatAndDisplayJSON(text) {
  try {
    // parse the JSON string
    const jsonObject = JSON.parse(text);
    const formattedJSON = JSON.stringify(jsonObject, null, tabs);
  
    return(formattedJSON);
  }
  catch (jsonError) {
    return formatPythonLikeObject(text);
  }
}
function formatPythonLikeObject(text) {
  let indent = 0;
  let inString = false;
  const formatted = [];
  for (let i = 0; i < text.length; i++) {
      const char = text[i];
      if (char === '\'' || char === '"') {
          inString = !inString;
          formatted.push(char);
      } else if (!inString && (char === '{' || char === '[' || char === '(')) {
          formatted.push(char);
          formatted.push('\n');
          indent++;
          formatted.push(' '.repeat(indent * tabs));
      } else if (!inString && (char === '}' || char === ']' || char === ')')) {
          formatted.push('\n');
          indent--;
          formatted.push(' '.repeat(indent * tabs));
          formatted.push(char);
      } else if (!inString && char === ',') {
          formatted.push(char);
          formatted.push('\n');
          formatted.push(' '.repeat(indent * tabs));
      } else {
          formatted.push(char);
      }
  }
  return formatted.join('');
}

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
    // this.injectGriptapeCss();
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
        callback: (...args) => 
          {
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
            this.onDragOver = function( e) {
              if (e.dataTransfer && e.dataTransfer.items) {
                const audio = [...e.dataTransfer.items].find((f) => f.kind === "file" && f.type.startsWith("audio/"));
                console.log("dragover: " + audio);;
                return !!audio;
              }
              return false;
            }
            this.onDragDrop = function (e) {
              console.log("onDragDrop called");
              let handled = false;
              for (const file of e.dataTransfer.files) {
                if (file.type.startsWith("audio/")) {
                  handled = true;
                  uploadFile(file, !handled);
                  handled = true;
                  const filename = file.name;
                  console.log(filename);
                  pathWidget.options.values.push(filename);
                  pathWidget.value = filename;
                  if (pathWidget.callback) {
                      pathWidget.callback(filename)
                  }

                }
              }
              return handled;
              
            }
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
  beforeConfigureGraph: (graphData, missingNodeTypes) => {
    for (let node of graphData.nodes) {
      if (nodeFixes.fixes[node.type]) {
        node.type = nodeFixes.fixes[node.type];
      }
    }
  },


  init() {

  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {

    // if (nodeData.category.startsWith("Griptape")) {
    //   const origOnConfigure = nodeType.prototype.onConfigure;
    //   nodeType.prototype.onConfigure = function () {
    //     this.bgcolor = "#171717";
    //     this.color = getColor(nodeData.category);
    //   };

    // Set Config node randomization to Fixed
    if (nodeData.name.includes("Griptape Agent Config")) {
      const onNodeCreated  = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        for (const widget of this.widgets) {
          if (widget.name === "control_after_generate") {
            widget.value = "fixed";
          }
          }
        }
    }

    // Create Audio Node
    if (nodeData.name === "Griptape Load: Audio") {
      gtUIAddUploadWidget(nodeType, nodeData, "audio", "audio")
    }

    // Display Artifact Node
    if (nodeData.name === "Griptape Display: Artifact") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        const me = onNodeCreated?.apply(this);
        this.message = ComfyWidgets.STRING(this, 'Output Text', ['STRING', { multiline: true }], app).widget;
        this.message.value = "";
        this.message.inputEl.style.borderRadius = "8px";
        this.message.inputEl.style.padding  = "8px";
        this.message.inputEl.style.height = "100%";
        this.message.inputEl.classList.add("language-python");

        fitHeight(this, true);
        return me;
      }
     
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        let lineCount = 0;
        for (const widget of this.widgets) {
          if (widget.type === "customtext") {
            const new_val = message["INPUT"].join("");
            widget.value = new_val;

            // Count the number of lines in the text
            for (let char of new_val) {
              if (char === "\n") {
                lineCount++;
              }
            }
          }
        }
        this.onResize?.(this.size);
        this?.graph?.setDirtyCanvas(true, true);

      };
    }
    
    // Display Text Node
    if (nodeData.name === "Griptape Display: Text") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        const me = onNodeCreated?.apply(this);
        this.message = ComfyWidgets.STRING(this, 'Output Text', ['STRING', { multiline: true }], app).widget;
        this.message.value = "";
        this.message.inputEl.style.borderRadius = "8px";
        this.message.inputEl.style.padding  = "8px";
        this.message.inputEl.style.height = "100%";
        fitHeight(this, true);
        return me;
      }
     
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        let lineCount = 0;
        for (const widget of this.widgets) {
          if (widget.type === "customtext") {
            const new_val = message["INPUT"].join("");
            widget.value = new_val;

            // Count the number of lines in the text
            for (let char of new_val) {
              if (char === "\n") {
                lineCount++;
              }
            }
          }
        }
        this.onResize?.(this.size);
        this?.graph?.setDirtyCanvas(true, true);
      };
    };

    // Display Data as Text node
    if ( nodeData.name === "Griptape Display: Data as Text") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        const me = onNodeCreated?.apply(this);
        this.message = ComfyWidgets.STRING(this, 'Output Text', ['STRING', { multiline: true }], app).widget;
        this.message.value = "";
        this.message.inputEl.style.borderRadius = "8px";
        this.message.inputEl.style.padding  = "8px";
        this.message.inputEl.style.height = "100%";
        fitHeight(this, true);
        return me;
      }
     
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        let lineCount = 0;
        for (const widget of this.widgets) {
          if (widget.type === "customtext") {
            const new_val = message["INPUT"].join("");
            let formattedJSON = formatAndDisplayJSON(new_val);
            widget.value = formattedJSON;

            // Count the number of lines in the text
            for (let char of formattedJSON) {
              if (char === "\n") {
                lineCount++;
              }
            }
          }
        }
        this.onResize?.(this.size);
        this?.graph?.setDirtyCanvas(true, true);
      };
    };
  }
});

export const griptapenodes = new GriptapeNodes();
window.griptapenodes = griptapenodes;
