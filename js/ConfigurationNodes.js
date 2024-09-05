import { getOllamaModels, getLMStudioModels, updatePromptModelList } from "./gtUIUtils.js";
import { commentWidget } from "./utils.js";

export function setupConfigurationNodes(nodeType, nodeData, app) {
    if (nodeData.name.includes("Griptape Agent Config") || (nodeData.name.includes("Griptape Embedding Driver")) || (nodeData.name.includes("Griptape Prompt Driver"))) {
        
        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = async function () {
            onNodeCreated?.apply(this, arguments);
            
            // Ensure this.widgets exists before trying to filter it
            if (this.widgets && Array.isArray(this.widgets)) {
              // Find widgets you want to turn into comments
              const commentWidgets = this.widgets.filter(w => w.name.toLowerCase().includes('comment'));
              commentWidgets.forEach(widget => commentWidget(this, widget));
              } else {
                  // If widgets aren't available yet, set up a timeout to check again
                  setTimeout(() => {
                      if (this.widgets && Array.isArray(this.widgets)) {
                          const commentWidgets = this.widgets.filter(w => w.name.toLowerCase().includes('comment'));
                          commentWidgets.forEach(widget => commentWidget(this, widget));
                      } else {
                          // console.warn('Widgets not available for node:', this.title);
                      }
                  }, 100); // Wait 100ms and try again
              }


            let engine = null;
            if (nodeData.name.includes("Ollama")) {
              engine="ollama"
            }
            if (nodeData.name.includes("LM Studio")) {
              engine="lmstudio"
            }
            if (engine) {
              if (this.widgets) {
                const modelWidgets = this.widgets.filter((w) => ["model", "prompt_model", "embedding_model"].includes(w.name));
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
                  
                  const allModels = await fetchModels(engine, baseIp, port);
                  
                  // Update each modelWidget's options and value
                  modelWidgets.forEach(modelWidget => {
                    let filteredModels;
                    if (modelWidget.name.includes("embed")) {
                      filteredModels = allModels.filter(model => model.toLowerCase().includes("embed"));
                    } else {
                      filteredModels = allModels.filter(model => !model.toLowerCase().includes("embed"));
                    }
                    
                    modelWidget.options.values = filteredModels;
                    
                    if (filteredModels.includes(modelWidget.value)) {
                      modelWidget.value = modelWidget.value;
                    } else if (filteredModels.length > 0) {
                      modelWidget.value = filteredModels[0];
                    } else {
                      modelWidget.value = "";
                    }
                  });
                  
                  this.triggerSlot(0);
                };
        
                baseIpWidget.callback = updateModels;
                portWidget.callback = updateModels;
                
                // Initial update
                await updateModels();
                fetchModels(engine, baseIpWidget.value, portWidget.value)
              }
            }
            setFixedRandomization(this);
            // console.log("original size: ", this.size);
            // setTimeout(() =>{
            //   this.onResize?.(this.size);
            //   this.graph.setDirtyCanvas(true, true);

              
            // },100)

          };
          
        
      }
    }
           
      function setFixedRandomization(node) {
        if(node.widgets) {
          const controlWidget = node.widgets.find((w) => w.name === "control_after_generate");
          if (controlWidget) {
        controlWidget.value = "fixed";
    } else {
        // console.warn("Control widget not found for setting fixed randomization");
    }
  }
}
  
  