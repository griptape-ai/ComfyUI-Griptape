import { getOllamaModels, getLMStudioModels, updatePromptModelList } from "./gtUIUtils.js";
import { getStorageValue, setStorageValue } from "../../scripts/utils.js";

function applyColor(node, color) {
    node.color = color.color;
    node.bgcolor = color.bgcolor;
    node.groupcolor = color.groupcolor;
}
export function setupNodeColors(nodeType, nodeData) {
    const setColor = getStorageValue("Comfy.Griptape.ColorNodes", true);
    if (setColor) {
        if (nodeData.name.includes("Griptape")) {
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = async function () {
                onNodeCreated?.apply(this, arguments);
                const nodeColors = LGraphCanvas.node_colors;
                if (nodeData.name.includes("Griptape Prompt Driver") ||
                    nodeData.name.includes("Griptape Embedding Driver") ||
                    nodeData.name.includes("Griptape Driver") ||
                    nodeData.name.includes("Griptape Vector Store Driver") ||
                    nodeData.name.includes("Griptape Text To Speech Driver") ||
                    nodeData.name.includes("Griptape Audio Transcription Driver") ||
                    nodeData.name.includes("Griptape WebSearch Driver") 
                ) {
                    applyColor(this, nodeColors.cyan);
                }
                if (nodeData.name.includes("Griptape Agent Config:") ||
                    nodeData.name === "Griptape Set: Default Agent")
                {
                    applyColor(this, nodeColors.pale_blue);
                }
                if (nodeData.name === "Griptape Create: Agent" ||
                    nodeData.name === "Griptape Create: Agent from Config" ) {
                    applyColor(this, nodeColors.purple);
                }
                if (nodeData.name === "Griptape Create: Rules" ||
                    nodeData.name.includes("Griptape Replace: Rulesets")) {
                    applyColor(this, nodeColors.cyan);
                }
                if (nodeData.name.includes("Griptape Tool:") || 
                    nodeData.name.includes("Griptape Replace: Tools") ||
                    nodeData.name === ("Griptape Convert: Agent to Tool")) {
                    applyColor(this, nodeColors.cyan);
                }
                // if (nodeData.name.includes("Griptape Combine:") ||
                //     nodeData.name.includes("Griptape Expand:")) {
                //     applyColor(this, nodeColors.none);
                // }
                if (nodeData.name.includes("Griptape Display:")){
                    applyColor(this, nodeColors.black);
                }
                // if (nodeData.name.includes("Griptape Create: Text") ||
                //     nodeData.name.includes("Griptape Create: CLIP") ||
                //     nodeData.name.includes("Griptape Convert: Text to CLIP") ||
                //     nodeData.name.includes("Griptape Load")){
                //     applyColor(this, nodeColors.green);
                // }
                if (nodeData.name.includes("Griptape Create: Image") ||
                    nodeData.name.includes("Griptape Run:") ||
                    nodeData.name.includes("Griptape Vector Store: Add Text") ||
                    nodeData.name.includes("Griptape Vector Store: Query")){
                    applyColor(this, nodeColors.red);
                }

                if (nodeData.name.includes("[DEPRECATED]")){
                    applyColor(this, nodeColors.yellow)

                }
                const size = this.size;
                this.onResize?.(this.size);
                this?.graph?.setDirtyCanvas(true, true);
          
                
            };
        }
    }
}
