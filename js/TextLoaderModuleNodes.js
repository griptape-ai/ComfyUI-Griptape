import { hideWidget, showWidget } from "./utils.js";
export function setupTextLoaderModuleNodes(nodeType, nodeData, app) {
    if (nodeData.name === "Griptape RAG Retrieve: Text Loader Module") {
      setupLoaderAttr(nodeType, nodeData, app);
    }
  }
  
  function setupLoaderAttr(nodeType, nodeData, app) {
    const onNodeCreated = nodeType.prototype.onNodeCreated
    nodeType.prototype.onNodeCreated = function() {
      const me = onNodeCreated?.apply(this);
      const widget_loader_type = this.widgets.find(w => w.name === 'loader');
      const widget_text = this.widgets.find(w=> w.name === 'text');
      const widget_url = this.widgets.find(w=> w.name === 'url');

      // Hide both widgets
      widget_loader_type.callback = async() => {
        hideWidget(this, widget_url);

        switch (widget_loader_type.value) {
          case "WebLoader":
            showWidget(widget_url);
            break;
        }
      }

      setTimeout(() => { widget_loader_type.callback() }, 5);
      return me;
      // setupMessageStyle(this.message);
    };
  
  }
  
