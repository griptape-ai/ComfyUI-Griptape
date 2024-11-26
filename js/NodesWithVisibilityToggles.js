import { ComfyWidgets } from "../../../scripts/widgets.js";
import { fitHeight } from "./utils.js";
import { formatAndDisplayJSON } from "./gtUIUtils.js";
import { hideWidget, showWidget } from "./utils.js";
import { app } from "../../../scripts/app.js";
export function setupVisibilityToggles(nodeType, nodeData, app) {
  if (nodeData.name.includes("Black Forest Labs Image Generation")) {
    setupBlackForestLabsImageGenerationNode(nodeType, nodeData, app);
  }
}

function setupBlackForestLabsImageGenerationNode(nodeType, nodeData, app) {
  const onNodeCreated = nodeType.prototype.onNodeCreated;
  nodeType.prototype.onNodeCreated = function () {
    const me = onNodeCreated?.apply(this);
    const widget_model = this.widgets.find(
      (w) => w.name === "image_generation_model"
    );

    const width_widget = this.widgets.find((w) => w.name === "width");
    const height_widget = this.widgets.find((w) => w.name === "height");
    const aspect_ratio_width_widget = this.widgets.find(
      (w) => w.name === "aspect_ratio_width"
    );
    const aspect_ratio_height_widget = this.widgets.find(
      (w) => w.name === "aspect_ratio_height"
    );

    const raw_widget = this.widgets.find((w) => w.name === "raw");
    const guidance_widget = this.widgets.find((w) => w.name === "guidance");
    const steps_widget = this.widgets.find((w) => w.name === "steps");
    const interval_widget = this.widgets.find((w) => w.name === "interval");
    const prompt_upsampling_widget = this.widgets.find(
      (w) => w.name === "prompt_upsampling"
    );
    const image_prompt_strength_widget = this.widgets.find((w) => w.name === "image_prompt_strength");

    // Hide both widgets
    widget_model.callback = async () => {
      hideWidget(this, width_widget);
      hideWidget(this, height_widget);
      hideWidget(this, aspect_ratio_width_widget);
      hideWidget(this, aspect_ratio_height_widget);
      hideWidget(this, raw_widget);
      hideWidget(this, guidance_widget);
      hideWidget(this, steps_widget);
      hideWidget(this, interval_widget);
      hideWidget(this, prompt_upsampling_widget);
      hideWidget(this, image_prompt_strength_widget);

      switch (widget_model.value) {
        case "flux-pro-1.1-ultra":
          showWidget(aspect_ratio_height_widget);
          showWidget(aspect_ratio_width_widget);
          showWidget(raw_widget);
          showWidget(image_prompt_strength_widget);
          break;
        case "flux-pro-1.1":
          showWidget(width_widget);
          showWidget(height_widget);
          showWidget(prompt_upsampling_widget);
          break;
        case "flux-pro":
          showWidget(width_widget);
          showWidget(height_widget);
          showWidget(prompt_upsampling_widget);
          showWidget(interval_widget);
          showWidget(guidance_widget);
          showWidget(steps_widget);
          break;
        case "flux-dev":
          showWidget(width_widget);
          showWidget(height_widget);
          showWidget(guidance_widget);
          showWidget(steps_widget);
          showWidget(prompt_upsampling_widget);
          break;
        case "flux-pro-1.0-depth":
        case "flux-pro-1.0-canny":
          showWidget(guidance_widget);
          showWidget(steps_widget);
          showWidget(prompt_upsampling_widget);
          break;

        default:
          break;
      }
      fitHeight(this, true);
    };

    setTimeout(() => {
      widget_model.callback();
    }, 5);
    return me;
  };
}
