export function get_position_style(ctx, widget_width, y, node_height) {
    const MARGIN = 4;
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
        maxHeight: `${node_height - MARGIN*2}px`,
        width: `auto`,
        height: `auto`,
    }
}

export function formatAndDisplayJSON(text) {
    try {
        const jsonObject = JSON.parse(text);
        return JSON.stringify(jsonObject, null, 2);
    } catch (jsonError) {
        return formatPythonLikeObject(text);
    }
}

export function formatPythonLikeObject(text) {
    let indent = 0;
    let inString = false;
    const formatted = [];
    for (let i = 0; i < text.length; i++) {
        // ... (rest of the function remains the same)
    }
    return formatted.join('');
}

export function chainCallback(object, property, callback) {
    if (object == undefined) {
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

export async function uploadFile(file) {
    try {
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

export function gtUIAddUploadWidget(nodeType, nodeData, widgetName, type="audio") {
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

export async function getLMStudioModels(baseUrl, port) {
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
  
export async function getOllamaModels(baseUrl, port) {
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
  export async function updatePromptModelList(node, models) {

    const modelWidget = node.widgets.find((w) => w.name === "model" || w.name === "prompt_model");
    if (modelWidget){
        const selectedItem = modelWidget.value;
    
        modelWidget.options.values = models;
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
  
  }