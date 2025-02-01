// Menu items that should have a separator above them
const sep_above_items = [
  // Main Menu Items
  "Agent Configs",
  "Display",
  "Audio",
  // Sub Menu Items - Agent
  "Griptape Run: Agent",
  "Griptape Run: Cloud Assistant",
  "Griptape Expand: Agent Nodes",
  "Griptape Convert: Agent to Tool",
  // Sub Menu Item - Agent Configs
  "Griptape Agent Config: Amazon Bedrock Drivers",
  // Sub Menu Item - Agent Tools
  "Griptape Tool: Audio Transcription",
  "Griptape Tool: Extraction",
  // Sub Menu Item - Agent Rules
  "Griptape Retrieve: Cloud Ruleset",
  // Sub Menu Item -  Audio
  "Griptape Load: Audio",
  // Sub Menu Items - Image
  "Griptape Load: Image From URL",
  "Griptape Run: Image Description",
  // Sub Menu Items - Text
  "Griptape Convert: Text to CLIP Encode",
  "Griptape Combine: Merge Texts",
  "Griptape Load: Text",
  "Griptape Vector Store: Add Text",
  "Griptape Run: Text Extraction",
  // Sub Menu Items - RAG
  "Griptape RAG Query: Translate Module",
  "Griptape RAG Retrieve: Text Loader Module",
  "Griptape RAG Rerank: Text Chunks Module",
  "Griptape RAG Response: Prompt Module",
];
export function setupMenuSeparator() {
  const originalAddItem = LiteGraph.ContextMenu.prototype.addItem;
  LiteGraph.ContextMenu.prototype.addItem = function (name, value, options) {
    for (let item of sep_above_items) {
      if (name === item) {
        this.addItem("", null);
      }
    }
    return originalAddItem.apply(this, arguments);
  };
}
