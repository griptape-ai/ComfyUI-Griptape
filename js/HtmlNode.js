import { app } from "../../../scripts/app.js";
import { $el } from "../../../scripts/ui.js";

/* 
A method that returns the required style for the html 
*/
function get_position_style(ctx, widget_width, y, node_height) {
  const MARGIN = 4; // the margin around the html element

  /* Create a transform that deals with all the scrolling and zooming */
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
    maxHeight: `${node_height - MARGIN * 2}px`, // we're assuming we have the whole height of the node
    width: `auto`,
    height: `auto`,
  };
}

app.registerExtension({
  name: "the.unique,name",

  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeType.comfyClass == "HtmlNode") {
      /* 
            Hijack the onNodeCreated call to add our widget
            */
      const orig_nodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        orig_nodeCreated?.apply(this, arguments);

        const widget = {
          type: "HTML", // whatever
          name: "flying", // whatever
          draw(ctx, node, widget_width, y, widget_height) {
            Object.assign(
              this.inputEl.style,
              get_position_style(ctx, widget_width, y, node.size[1])
            ); // assign the required style when we are drawn
          },
        };

        /*
                Create an html element and add it to the document.  
                Look at $el in ui.js for all the options here
                */
        widget.inputEl = $el("img", {
          src: "https://assets-global.website-files.com/65d658559223871198e78bca/65e4fd64fb258c6d9bd8c276_griptape-Chunck_beige.svg",
        });
        document.body.appendChild(widget.inputEl);

        /*
                Add the widget, make sure we clean up nicely, and we do not want to be serialized!
                */
        this.addCustomWidget(widget);
        this.onRemoved = function () {
          widget.inputEl.remove();
        };
        this.serialize_widgets = false;
      };
    }
  },
});
