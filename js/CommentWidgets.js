import { commentWidget } from "./utils.js";

export function setupCommentWidgets(nodeType, nodeData, app) {
    if ((nodeData.name.includes("Griptape Agent Config")) || 
      (nodeData.name.includes("Bria")) ) {
        
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

          };
          
        
      }
    }

  
  