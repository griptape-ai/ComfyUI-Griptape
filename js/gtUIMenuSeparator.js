// Menu items that should have a separator above them
const sep_above_items = [
    // Main Menu Items
    "Agent Configs",
    "Display",
    "Audio",
    // Sub Menu Items - Agent
    "Griptape Run: Agent",
    "Griptape Expand: Agent Nodes",
    "Griptape Convert: Agent to Tool",
    // Sub Menu Item - Agent Configs
    "Griptape Agent Config: Amazon Bedrock",
    // Sub Menu Item - Agent Tools
    "Griptape Tool: Audio Transcription",
    // Sub Menu Item -  Audio
    "Griptape Load: Audio",
    // Sub Menu Items - Image
    "Griptape Load: Image From URL",
    "Griptape Run: Image Description",
    // Sub Menu Items - Text
    "Griptape Convert: Text to CLIP Encode",
    "Griptape Combine: Merge Texts",
    "Griptape Save: Text",
    "Griptape Vector Store: Add Text"
]
export function setupMenuSeparator() {
    const originalAddItem = LiteGraph.ContextMenu.prototype.addItem;
    LiteGraph.ContextMenu.prototype.addItem = function (name, value, options) {
      for (let item of sep_above_items) {
        if (name === item) {
          this.addItem("", null)
        }
      }
      return originalAddItem.apply(this, arguments);
    }
}