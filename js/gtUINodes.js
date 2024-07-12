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
      // // TODO: Figure out how to pull and set the environment variables
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
async function getOllamaModels(baseUrl, port) {
  const url = `${baseUrl}:${port}/api/tags`;

  try {
      const response = await fetch(url);

      if (!response.ok) {
          throw new Error(`Failed to fetch models: ${response.status}`);
      }

      const modelsInfo = await response.json();

      // Extract the model names
      const models = modelsInfo.models.map(model => model.name);

      return models;
  } catch (error) {
      console.error("Error fetching Ollama models:", error);
      return [];
  }
}
async function getLMStudioModels(baseUrl, port) {
  const url = `${baseUrl}:${port}/v1/models`;

  try {
      const response = await fetch(url);

      if (!response.ok) {
          throw new Error(`Failed to fetch models: ${response.status}`);
      }

      const modelsInfo = await response.json();

      // Extract the model names
      const models = modelsInfo.data.map(model => model.id);

      return models;
  } catch (error) {
      console.error("Error fetching LM Studio models:", error);
      return [];
  }
}
async function updatePromptModelList(node, models) {
  const modelWidget = node.widgets.find((w) => w.name === "prompt_model");
  const selectedItem = modelWidget.value;

  modelWidget.options.values = models;
  console.log("Models" + models);
  // if (models.length > 0) {
  //     modelWidget.value = models[0];
  // }
  const warning = "No models returned from server"
  if (models.length == 0){
    modelWidget.value = warning
  }
  if ((selectedItem === "" || selectedItem === null || selectedItem == warning) && models.length > 0 && !models.includes(selectedItem)) {
    modelWidget.value = models[0];
  }
  

}

function gtUIAddUploadWidget(nodeType, nodeData, widgetName, type="audio") {
    chainCallback(nodeType.prototype, "onNodeCreated", function() {
        const pathWidget = this.widgets.find((w) => w.name === widgetName);
        const fileInput = document.createElement("input");
        document.body.append(fileInput);
        let uploadWidget = this.addWidget("button", "choose " + type + " to upload", "image", () => {
            //clear the active click event
            app.canvas.node_widget = null

            fileInput.click();
        });
        uploadWidget.options.serialize = false;

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
                        const filetype = fileInput.files[0].type;
                        pathWidget.options.values.push(filename);
                        pathWidget.value = filename;
                        if (pathWidget.callback) {
                            pathWidget.callback(filename)
                        }
                        // Create a URL for the audio file and set it as the source of the audio element
                        // const audioURL = URL.createObjectURL(filename);
                        // audioWidget.src = audioURL;
                    }
                },
                
            });
            
            this.onDragOver = function( e) {
              if (e.dataTransfer && e.dataTransfer.items) {
                const audio = [...e.dataTransfer.items].find((f) => f.kind === "file" && f.type.startsWith("audio/"));
                // console.log("dragover: " + audio);
                // console.log(audio);
                return !!audio;
              }
              return false;
            }
            this.onDragDrop = function (e) {
              let handled = false;
              for (const file of e.dataTransfer.files) {
                if (file.type.startsWith("audio/")) {
                  handled = true;
                  uploadFile(file, !handled);
                  handled = true;
                  const filename = file.name;
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

    // if (nodeData.name.startsWith("Griptape")) {
    //   const origOnConfigure = nodeType.prototype.onConfigure;
    //   nodeType.prototype.onConfigure = function () {
    //     this.bgcolor=LGraphCanvas.node_colors.yellow.bgcolor;

    //     // this.color = getColor(nodeData.category);
    //   };
    // }

    // Configuration Nodes
    if (nodeData.name.includes("Griptape Agent Config")) {
      const onNodeCreated  = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        
        // Ollama Config Node
        if (nodeData.name.includes("Ollama")) {
          
          // get the base_url
          const base_url = this.widgets.find((w) => w.name === "base_url");
          const port = this.widgets.find((w) => w.name === "port");
          getOllamaModels(base_url.value, port.value).then((models) => {
            const model = this.widgets.find((w) => w.name === "prompt_model");
            model.options.values = models;
            updatePromptModelList(this, models);
          })
        }
        
        // LMStudio Config Node
        if (nodeData.name.includes("LM Studio")) {
          chainCallback(nodeType.prototype, "onNodeUpdated", function() {
          });
          // get the base_url
          const base_url = this.widgets.find((w) => w.name === "base_url");
          const port = this.widgets.find((w) => w.name === "port");
          getLMStudioModels(base_url.value, port.value).then((models) => {
            const model = this.widgets.find((w) => w.name === "prompt_model");
            model.options.values = models;
            updatePromptModelList(this, models);
          })
        }
        
        
        // Set Config node randomization to Fixed
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
      // nodeType.prototype.onNodeCreated = async function () {
      //   const me = onNodeCreated?.apply(this);
      //   this.message = ComfyWidgets.STRING(this, 'Output Text', ['STRING', { multiline: true }], app).widget;
      //   this.message.value = "";
      //   this.message.inputEl.style.borderRadius = "8px";
      //   this.message.inputEl.style.padding  = "8px";
      //   this.message.inputEl.style.height = "100%";
        
      //   fitHeight(this, true);
       
      //   return me;
      // }
     
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        let lineCount = 0;
        let stringWidget = null;
      
        for (const widget of this.widgets) {
          if (widget.name === "INPUT") {
            
            // Check if the widget is connected
            const isConnected = this.isInputConnected(this.findInputSlot(widget.name));
      
            if (isConnected) {
              
              // Check the structure of message["INPUT"]
              if (message.hasOwnProperty("INPUT")) {
                
                let new_val;
                if (Array.isArray(message["INPUT"])) {
                  new_val = message["INPUT"].join("");
                } else if (typeof message["INPUT"] === 'string') {
                  new_val = message["INPUT"];
                } else {
                  new_val = String(message["INPUT"]);
                }
      
                if (typeof new_val === 'string' && new_val.trim() !== "") {
                  // Find the "STRING" widget and update its value
                  stringWidget = this.widgets.find(w => w.name === "STRING");
                  if (stringWidget) {
                    stringWidget.value = new_val;
                  }
                  // Count the number of lines in the text
                  lineCount = new_val.split("\n").length - 1;
                }
              }
            }
          }
        }
        
        // Adjust node size based on line count if needed
        if (lineCount > 0) {
          this.size[1] = Math.max(this.size[1], lineCount * 20 + 40);
        }
        
        // If we updated the STRING widget, we need to notify the node to redraw
        if (stringWidget) {
          this.setDirtyCanvas(true, true);
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

    // Combine: Merge Texts
    if (  nodeData.name === "Griptape Combine: Merge Texts" || 
          nodeData.name === "Griptape Combine: Merge Inputs" || 
          nodeData.name === "Griptape Combine: Rules List" ||
          nodeData.name === "Griptape Combine: Tool List" ||
          nodeData.name === "Griptape Create: Pipeline") {

      // Set the base name of the input node
      var input_name = "input_";

      switch (nodeData.name) {
        case 'Griptape Combine: Rules List':
          input_name = "rules_";
          break;
        case 'Griptape Combine: Tool List':
            input_name = "tool_";
            break;
        case 'Griptape Create: Pipeline':
            input_name = "task_";
            break;
      }

			const onConnectionsChange = nodeType.prototype.onConnectionsChange;
			nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
        if(!link_info)
          return;
        if(type==1) {
          console.log("link_info", link_info);
          console.log("connected", connected);
          console.log("index", index);
          const node = app.graph.getNodeById(link_info.origin_id);
          let origin_type = node.outputs[link_info.origin_slot].type;

          if(origin_type == '*') {
            console.log("origin_type", origin_type);
            this.disconnectInput(link_info.target_slot);
          }

          for(let i in this.inputs) {
            console.log("Working on input", this.inputs[i].name);
            if (this.inputs[i].name.includes(input_name)) {
              console.log("input_name", input_name)
              let input_i = this.inputs[i];
              for(let i in this.inputs) {
                let input_i = this.inputs[i];
                if(input_i.name != 'select' && input_i.name != 'sel_mode')
                  input_i.type = origin_type;

                // console.log("Outputs", this.outputs[i]);
                // this.outputs[i].type = origin_type;
                // this.outputs[i].label = origin_type;
                // this.outputs[i].name = origin_type;
              }

            }
          };
        }

				let select_slot = this.inputs.find(x => x.name == "select");
				let mode_slot = this.inputs.find(x => x.name == "sel_mode");

				let converted_count = 0;
				converted_count += select_slot?1:0;
				converted_count += mode_slot?1:0;

				if (!connected && (this.inputs.length > 1+converted_count)) {
					const stackTrace = new Error().stack;

					if(
						!stackTrace.includes('LGraphNode.prototype.connect') && // for touch device
						!stackTrace.includes('LGraphNode.connect') && // for mouse device
						!stackTrace.includes('loadGraphData') &&
						this.inputs[index].name != 'select') {
						this.removeInput(index);
					}
				}

				let slot_i = 1;
				for (let i = 0; i < this.inputs.length; i++) {
					let input_i = this.inputs[i];
					if(input_i.name != 'select'&& input_i.name != 'sel_mode') {
						input_i.name = `${input_name}${slot_i}`
						slot_i++;
					}
				}

				let last_slot = this.inputs[this.inputs.length - 1];
        // console.log(origin_type);
				if (
					(last_slot.name == 'select' && last_slot.name != 'sel_mode' && this.inputs[this.inputs.length - 2].link != undefined)
					|| (last_slot.name != 'select' && last_slot.name != 'sel_mode' && last_slot.link != undefined)) {
						this.addInput(`${input_name}${slot_i}`, this.origin_type);
				}

        let widgets_to_set = [];

				if(this.widgets) {
          for (let i = 0; i < this.widgets.length; i++) {
            if (this.widgets[i].name.includes(input_name)) {
              console.log(this.widgets[i].name);
              this.widgets[0].options.max = select_slot?this.inputs.length-1:this.inputs.length;
              this.widgets[0].value = Math.min(this.widgets[0].value, this.widgets[0].options.max);
              if(this.widgets[0].options.max > 0 && this.widgets[0].value == 0)
                this.widgets[0].value = 1;
            }
            else {
              // store the widget and value in widgets_to_set array
              widgets_to_set.push({widget: this.widgets[i], value: this.widgets[i].value});
              
            }
          }
				}
        console.log(widgets_to_set);
        for (let i = 0; i < widgets_to_set.length; i++) {
          widgets_to_set[i].widget.value = widgets_to_set[i].value;
        }
      }

    }
  }
});

export const griptapenodes = new GriptapeNodes();
window.griptapenodes = griptapenodes;
