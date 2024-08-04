import { getOllamaModels, getLMStudioModels, updatePromptModelList } from "./gtUIUtils.js";

export function setupConfigurationNodes(nodeType, nodeData, app) {
    if (nodeData.name.includes("Griptape Agent Config") || (nodeData.name.includes("Griptape Embedding Driver")) || (nodeData.name.includes("Griptape Prompt Driver"))) {
        
        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = async function () {
            onNodeCreated?.apply(this, arguments);
            
            let engine = "ollama"
            if (nodeData.name.includes("LM Studio")) {
                engine="lmstudio"
            }
            if (this.widgets) {
              const modelWidget = this.widgets.find((w) => w.name === "model" || w.name === "prompt_model");
              const baseIpWidget = this.widgets.find((w) => w.name === "base_url");
              const portWidget = this.widgets.find((w) => w.name === "port");
              const fetchModels = async (engine, baseIp, port) => {
                try {
                  const response = await fetch("/Griptape/get_models", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                      engine: engine,
                      base_ip: baseIp,
                      port: port,
                    }),
                  });
      
                  if (response.ok) {
                    const models = await response.json();
                    return models;
                  } else {
                    console.error(`Failed to fetch models: ${response.status}`);
                    return [];
                  }
                } catch (error) {
                  console.error(`Error fetching models for engine ${engine}:`, error);
                  return [];
                }
              };
              const updateModels = async () => {
                let engine = "ollama"
                if (nodeData.name.includes("LM Studio")) {
                    engine="lmstudio"
                }
    
                const baseIp = baseIpWidget.value;
                const port = portWidget.value;
          
                const models = await fetchModels(engine, baseIp, port);
      
                // Update modelWidget options and value
                modelWidget.options.values = models;
      
                if (models.includes(modelWidget.value)) {
                  modelWidget.value = modelWidget.value;
                } else if (models.length > 0) {
                  modelWidget.value = models[0];
                } else {
                  modelWidget.value = "";
                }
      
                this.triggerSlot(0);
      
              };
      
              baseIpWidget.callback = updateModels;
              portWidget.callback = updateModels;
      
              // Initial update
              await updateModels();
              fetchModels(engine, baseIpWidget.value, portWidget.value)

              setFixedRandomization(this);
            }
        };

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
  
  