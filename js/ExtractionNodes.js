import { ComfyWidgets } from "../../../scripts/widgets.js";
import { fitHeight } from "./utils.js";
import { formatAndDisplayJSON } from "./gtUIUtils.js";
import { hideWidget, showWidget } from "./utils.js";
import { app } from "../../../scripts/app.js";
export function setupExtractionNodes(nodeType, nodeData, app) {
    if (nodeData.name === "Griptape Tool: Extraction") {
      setupExtractionTypeAttrr(nodeType, nodeData, app);
    }
  }
  
  function setupExtractionTypeAttrr(nodeType, nodeData, app) {
    const onNodeCreated = nodeType.prototype.onNodeCreated
    nodeType.prototype.onNodeCreated = function() {
      const me = onNodeCreated?.apply(this);
      const widget_extraction_type = this.widgets.find(w => w.name === 'extraction_type');
      const widget_column_names = this.widgets.find(w=> w.name === 'column_names');
      const widget_template_schema = this.widgets.find(w=> w.name === 'template_schema');

      // Hide both widgets
      widget_extraction_type.callback = async() => {
        hideWidget(this, widget_column_names);
        hideWidget(this, widget_template_schema);

        switch (widget_extraction_type.value) {
          case "csv":
            showWidget(widget_column_names);
            // fitHeight(this, true);
            break;
          case "json":
            showWidget(widget_template_schema);
            // fitHeight(this, true);
            break;
          default:
            // fitHeight(this, true);
            break;
        }
      }

      setTimeout(() => { widget_extraction_type.callback() }, 5);
      return me;
      // setupMessageStyle(this.message);
    };
  
  }
  
