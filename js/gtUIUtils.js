import { api } from "../../../scripts/api.js";

export function get_position_style(ctx, widget_width, y, node_height) {
  const MARGIN = 4;
  const elRect = ctx.canvas.getBoundingClientRect();
  const transform = new DOMMatrix()
    .scaleSelf(
      elRect.width / ctx.canvas.width,
      elRect.height / ctx.canvas.height
    )
    .multiplySelf(ctx.getTransform())
    .translateSelf(MARGIN, MARGIN + y);

  return {
    transformOrigin: "0 0",
    transform: transform,
    left: `0px`,
    top: `0px`,
    position: "absolute",
    maxWidth: `${widget_width - MARGIN * 2}px`,
    maxHeight: `${node_height - MARGIN * 2}px`,
    width: `auto`,
    height: `auto`,
  };
}

export function formatAndDisplayJSON(text) {
  console.log("Input text:", text); // Debug: Log the input

  if (typeof text !== "string") {
    console.log("Input is not a string:", typeof text);
    return "Error: Input is not a string";
  }

  try {
    // Try to parse as JSON
    const jsonObject = JSON.parse(text);
    const formattedJSON = JSON.stringify(jsonObject, null, 2);
    console.log("Formatted JSON:", formattedJSON); // Debug: Log the result
    return formattedJSON;
  } catch (jsonError) {
    console.log("JSON parse error:", jsonError.message); // Debug: Log the error

    // Check if it's a Python-like object
    if (text.trim().startsWith("{") || text.trim().startsWith("[")) {
      try {
        const formattedPython = formatPythonLikeObject(text);
        console.log("Formatted Python-like object:", formattedPython); // Debug: Log the result
        return formattedPython || text; // Return original text if formatPythonLikeObject returns empty
      } catch (pythonError) {
        console.log(
          "Python-like object formatting error:",
          pythonError.message
        ); // Debug: Log the error
      }
    }

    // If it's not JSON or a Python-like object, return the original text
    console.log("Returning original text");
    return text;
  }
}

export function formatPythonLikeObject(text) {
  let indent = 0;
  let inString = false;
  const formatted = [];
  for (let i = 0; i < text.length; i++) {
    // ... (rest of the function remains the same)
  }
  return formatted.join("");
}

export function chainCallback(object, property, callback) {
  if (object == undefined) {
    console.error("Tried to add callback to non-existent object");
    return;
  }
  if (property in object) {
    const callback_orig = object[property];
    object[property] = function () {
      const r = callback_orig.apply(this, arguments);
      callback.apply(this, arguments);
      return r;
    };
  } else {
    object[property] = callback;
  }
}

export async function uploadFile(file) {
  try {
    const body = new FormData();
    const i = file.webkitRelativePath.lastIndexOf("/");
    const subfolder = file.webkitRelativePath.slice(0, i + 1);
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
      return resp.status;
    } else {
      alert(resp.status + " - " + resp.statusText);
    }
  } catch (error) {
    alert(error);
  }
}
const createUrlCallback = function (baseurl) {
  return function () {
    window.open(baseurl, "_blank");
  };
};
const createUrlCallbackWithWidget = function (baseurl, widgetName, node) {
  return function () {
    // Find the widget by its name when the button is clicked
    const pathWidget = node.widgets.find((w) => w.name === widgetName);
    console.log(pathWidget);
    if (pathWidget) {
      let value = pathWidget.value; // Get the current value of the widget
      const url = baseurl + "/" + value; // Construct the URL
      window.open(url, "_blank"); // Open the URL in a new tab
    } else {
      console.error(`Widget with name ${widgetName} not found`);
    }
  };
};
export function gtUIAddUrlButtonWidget(
  nodeType,
  buttonText,
  baseurl,
  widgetName
) {
  chainCallback(nodeType.prototype, "onNodeCreated", function () {
    const buttonCallback = createUrlCallback(baseurl);
    if (widgetName != "") {
      buttonCallback = createUrlCallbackWithWidget(baseurl, widgetName, this);
    }
    let buttonWidget = this.addWidget(
      "button",
      buttonText,
      null,
      buttonCallback
    );
  });
}
export function gtUIAddButtonWidget(nodeType, buttonText, buttonCallback) {
  chainCallback(nodeType.prototype, "onNodeCreated", function () {
    let buttonWidget = this.addWidget(
      "button",
      buttonText,
      null,
      buttonCallback
    );
  });
}

export function gtUIAddUploadWidget(
  nodeType,
  nodeData,
  widgetName,
  type = "audio"
) {
  chainCallback(nodeType.prototype, "onNodeCreated", function () {
    const pathWidget = this.widgets.find((w) => w.name === widgetName);
    const fileInput = document.createElement("input");
    document.body.append(fileInput);
    let uploadWidget = this.addWidget(
      "button",
      "choose " + type + " to upload",
      "image",
      () => {
        //clear the active click event
        app.canvas.node_widget = null;

        fileInput.click();
      }
    );
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
          const i = directory.lastIndexOf("/");
          if (i <= 0) {
            throw "No directory found";
          }
          const path = directory.slice(0, directory.lastIndexOf("/"));
          if (pathWidget.options.values.includes(path)) {
            alert("A folder of the same name already exists");
            return;
          }
          let successes = 0;
          for (const file of fileInput.files) {
            if ((await uploadFile(file)) == 200) {
              successes++;
            } else {
              //Upload failed, but some prior uploads may have succeeded
              //Stop future uploads to prevent cascading failures
              //and only add to list if an upload has succeeded
              if (successes > 0) {
                break;
              } else {
                return;
              }
            }
          }
          pathWidget.options.values.push(path);
          pathWidget.value = path;
          if (pathWidget.callback) {
            pathWidget.callback(path);
          }
        },
      });
    } else if (type == "text") {
      console.log("text here");
      Object.assign(fileInput, {
        type: "file",
        accept:
          "text/plain,text/markdown,text/html,text/csv,text/xml,text/yaml,text/json,application/json,application/pdf,application/x-yaml,application/vnd.ms-excel,application/csv,application/tsv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/tab-separated-values,text/info",
        style: "display: none",
        onchange: async () => {
          if (fileInput.files.length) {
            if ((await uploadFile(fileInput.files[0])) != 200) {
              //upload failed and file can not be added to options
              return;
            }
            const filename = fileInput.files[0].name;
            pathWidget.options.values.push(filename);
            pathWidget.value = filename;
            if (pathWidget.callback) {
              pathWidget.callback(filename);
            }
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
            if ((await uploadFile(fileInput.files[0])) != 200) {
              //upload failed and file can not be added to options
              return;
            }
            const filename = fileInput.files[0].name;
            pathWidget.options.values.push(filename);
            pathWidget.value = filename;
            if (pathWidget.callback) {
              pathWidget.callback(filename);
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
            if ((await uploadFile(fileInput.files[0])) != 200) {
              //upload failed and file can not be added to options
              return;
            }
            const filename = fileInput.files[0].name;
            const filetype = fileInput.files[0].type;
            pathWidget.options.values.push(filename);
            pathWidget.value = filename;
            if (pathWidget.callback) {
              pathWidget.callback(filename);
            }
            // Create a URL for the audio file and set it as the source of the audio element
            // const audioURL = URL.createObjectURL(filename);
            // audioWidget.src = audioURL;
          }
        },
      });

      this.onDragOver = function (e) {
        if (e.dataTransfer && e.dataTransfer.items) {
          const audio = [...e.dataTransfer.items].find(
            (f) => f.kind === "file" && f.type.startsWith("audio/")
          );
          // console.log("dragover: " + audio);
          // console.log(audio);
          return !!audio;
        }
        return false;
      };
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
              pathWidget.callback(filename);
            }
          }
        }
        return handled;
      };
    } else {
      throw "Unknown upload type";
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
    const models = modelsInfo.data.map((model) => model.id);

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
    const models = modelsInfo.models.map((model) => model.name);

    return models;
  } catch (error) {
    console.error("Error fetching Ollama models:", error);
    return [];
  }
}
export async function updatePromptModelList(node, models) {
  const modelWidget = node.widgets.find(
    (w) => w.name === "model" || w.name === "prompt_model"
  );
  if (modelWidget) {
    const selectedItem = modelWidget.value;

    modelWidget.options.values = models;
    // if (models.length > 0) {
    //     modelWidget.value = models[0];
    // }
    const warning = "No models returned from server";
    if (models.length == 0) {
      modelWidget.value = warning;
    }
    if (
      (selectedItem === "" ||
        selectedItem === null ||
        selectedItem == warning) &&
      models.length > 0 &&
      !models.includes(selectedItem)
    ) {
      modelWidget.value = models[0];
    }
  }
}
