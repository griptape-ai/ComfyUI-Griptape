import { getOllamaModels, getLMStudioModels, updatePromptModelList } from "./gtUIUtils.js";

export function setupConfigurationNodes(nodeType, nodeData, app) {
    if (nodeData.name.includes("Griptape Agent Config") || (nodeData.name.includes("Griptape Embedding Driver")) || (nodeData.name.includes("Griptape Prompt Driver"))) {
        
        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = async function () {
            onNodeCreated?.apply(this, arguments);

            if (nodeData.name.includes("Ollama")) {
                setupOllamaConfig(this);
            } else if (nodeData.name.includes("LM Studio")) {
                setupLMStudioConfig(this);
            }
            
            setFixedRandomization(this);
        };
    }
}


function setupOllamaConfig(node) {
    const base_url = node.widgets.find((w) => w.name === "base_url");
    const port = node.widgets.find((w) => w.name === "port");

    if (base_url && port) {
        getOllamaModels(base_url.value, port.value)
        .then((models) => updatePromptModelList(node, models))
        .catch((error) => console.error("Error fetching Ollama models:", error));
    } else {
        console.warn("Ollama config: base_url or port widget not found");
    }
}
  
function setupLMStudioConfig(node) {
    const base_url = node.widgets.find((w) => w.name === "base_url");
    const port = node.widgets.find((w) => w.name === "port");
    
    if (base_url && port) {
        getLMStudioModels(base_url.value, port.value)
        .then((models) => updatePromptModelList(node, models))
        .catch((error) => console.error("Error fetching LM Studio models:", error));
    } else {
        console.warn("LM Studio config: base_url or port widget not found");
    }
}
  
function setFixedRandomization(node) {
    if(node.widgets) {
        const controlWidget = node.widgets.find((w) => w.name === "control_after_generate");
        if (controlWidget) {
            controlWidget.value = "fixed";
        } else {
            console.warn("Control widget not found for setting fixed randomization");
        }
    }
}
  
  