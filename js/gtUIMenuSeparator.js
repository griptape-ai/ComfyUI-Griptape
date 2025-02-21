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
export function setupMenuSeparator(app) {
  // Store original constructor
  const originalContextMenu = LiteGraph.ContextMenu;

  LiteGraph.ContextMenu = function (values, parentMenu, event) {
    // If this is a submenu (values is an array)
    if (Array.isArray(values)) {
      // Add separators before specific items
      for (let i = 0; i < values.length; i++) {
        const item = values[i];
        if (!item) continue;

        // Check if this item needs a separator
        // We'll check both content and value since some menus might use either
        const itemText = item.content || item.value;
        if (itemText && sep_above_items.includes(itemText)) {
          values.splice(i, 0, null);
          i++; // Skip ahead since we added an item
        }
      }
    }

    // Create the menu
    return new originalContextMenu(values, parentMenu, event);
  };

  // Maintain the prototype chain
  LiteGraph.ContextMenu.prototype = originalContextMenu.prototype;
}
