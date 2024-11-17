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
      const file_path = this.widgets.find(w=> w.name === 'file_path');
      const widget_url = this.widgets.find(w=> w.name === 'url');
      const upload_button = this.widgets.find(w=> w.name === 'choose text to upload');
      const input_source = this.widgets.find(w=> w.name === 'input_source');

      // Hide widgets
      widget_loader_type.callback = async() => {
        hideWidget(this, widget_url);
        hideWidget(this, input_source);
        switch (widget_loader_type.value) {
          case "WebLoader":
            showWidget(widget_url);
            break;
          case "TextLoader":
            showWidget(input_source);
            break;
          case "CsvLoader":
            showWidget(input_source);
            break;
          case "PdfLoader":
            input_source.value = "File Path";
            showWidget(input_source);
            showWidget(file_path);
            showWidget(upload_button);
            break;
        }
      }
      input_source.callback = async() => {
        hideWidget(this, file_path);
        hideWidget(this, upload_button);
        if (input_source.value == "File Path") {
          showWidget(file_path);
          showWidget(upload_button);
        }
        else {
          hideWidget(this, file_path);
          hideWidget(this, upload_button);
        }

      }

      setTimeout(() => { 
        input_source.callback(); 
      }, 5);
      setTimeout(() => { 
        widget_loader_type.callback(); 
      }, 5);
      return me;
      // setupMessageStyle(this.message);
    };
  
  }
  
