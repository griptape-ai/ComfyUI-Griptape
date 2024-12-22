import { ComfyWidgets } from "../../../scripts/widgets.js";
import { fitHeight } from "./utils.js";
import { formatAndDisplayJSON } from "./gtUIUtils.js";
import { hideWidget, showWidget } from "./utils.js";
import { app } from "../../../scripts/app.js";
import { code_execution_templates } from "./CodeExecutionNodeTemplates.js";

// make a list of the keys in the code_execution_templates object
const code_execution_template_keys = Object.keys(code_execution_templates);

export function setupCodeExecutionNode(nodeType, nodeData, app) {
    if (nodeData.name.includes("Code Execution"))
    {
      // Add menu items to examples dropdown
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
          onNodeCreated?.apply(this, arguments);
          const examples_widget = this.widgets.find(w => w.name === 'examples');
          
          examples_widget.options.values = code_execution_template_keys;
          examples_widget.callback = async() => {
    
            const code_widget = this.widgets.find(w => w.name === 'code');
            code_widget.value = code_execution_templates[examples_widget.value];

          }
    
        }
      const original_getExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;
      nodeType.prototype.getExtraMenuOptions = function(_, options) {
          original_getExtraMenuOptions?.apply(this, arguments);
          options.push({
              content: "Griptape Code Execution Templates",
              has_submenu: true,
              callback: make_code_execution_templates_submenu
              
              }
          )
      }   
    }
  
  }

function make_code_execution_templates_submenu(value, options, e, menu, node) {
  const submenu = new LiteGraph.ContextMenu(
    code_execution_template_keys,
    { 
        event: e, 
        callback: function (v) { 
          const code_widget = node.widgets.find(w => w.name === 'code');
          code_widget.value = code_execution_templates[v];
          console.log(v, code_widget.value);
            // do something with v (=="option x")
        }, 
        parentMenu: menu, 
        node:node
    }
)

}
  
