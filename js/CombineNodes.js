const TypeSlot = {
  Input: 1,
  Output: 2,
};

const TypeSlotEvent = {
  Connect: true,
  Disconnect: false,
};

export function setupCombineNodes(nodeType, nodeData, app) {
  if (
    nodeData.name === "Griptape Combine: Merge Texts" ||
    nodeData.name === "Griptape Combine: Merge Inputs" ||
    nodeData.name === "Griptape Combine: Rules List" ||
    nodeData.name === "Griptape Combine: Tool List" ||
    nodeData.name === "Griptape Combine: RAG Module List" ||
    nodeData.name === "Griptape Util: Switch Node" ||
    nodeData.name === "Griptape Combine: Merge Dictionary" ||
    nodeData.name === "Griptape Combine: String List" ||
    nodeData.name === "Griptape Create: Pipeline"
  ) {
    setupCombineNode(nodeType, nodeData, app);
  }
}

function setupCombineNode(nodeType, nodeData, app) {
  const input_name = getInputName(nodeData.name);
  const DEFAULT_TYPE = "*";

  const onNodeCreated = nodeType.prototype.onNodeCreated;
  nodeType.prototype.onNodeCreated = function () {
    const me = onNodeCreated?.apply(this);
    
    // Add initial dynamic input if it doesn't exist
    if (!this.inputs.some(input => input.name.includes(input_name))) {
      this.addInput(`${input_name}1`, DEFAULT_TYPE);
    }
    
    return me;
  };

  const onConnectionsChange = nodeType.prototype.onConnectionsChange;
  nodeType.prototype.onConnectionsChange = function (slotType, slot_idx, event, link_info, node_slot) {
    const me = onConnectionsChange?.apply(this, arguments);

    if (slotType === TypeSlot.Input) {
      if (link_info && event === TypeSlotEvent.Connect) {
        // Get the origin node and determine the type
        const fromNode = this.graph._nodes.find(
          (otherNode) => otherNode.id == link_info.origin_id
        );

        if (fromNode) {
          const parent_link = fromNode.outputs[link_info.origin_slot];
          if (parent_link) {
            const origin_type = parent_link.type;
            
            // Don't allow connections of type "*"
            if (origin_type === "*") {
              this.disconnectInput(link_info.target_slot);
              return me;
            }

            // Update all dynamic inputs to match the connected type
            updateAllDynamicInputTypes(this, input_name, origin_type);
          }
        }
      } else if (event === TypeSlotEvent.Disconnect) {
        // Handle disconnection - remove empty slots except special ones and the last one
        handleDisconnection(this, slot_idx, input_name);
      }

      // Clean up and reorganize inputs
      reorganizeInputs(this, input_name);
      
      // Force canvas refresh
      this?.graph?.setDirtyCanvas(true);
    }

    return me;
  };
}

function getInputName(nodeName) {
  switch (nodeName) {
    case "Griptape Combine: Rules List":
      return "rules_";
    case "Griptape Combine: Tool List":
      return "tool_";
    case "Griptape Create: Pipeline":
      return "task_";
    case "Griptape Combine: RAG Module List":
      return "module_";
    case "Griptape Combine: Merge Dictionary":
      return "dict_";
    default:
      return "input_";
  }
}

function updateAllDynamicInputTypes(node, input_name, origin_type) {
  // Update all dynamic inputs to use the same type
  for (let input of node.inputs) {
    if (input.name.includes(input_name)) {
      input.type = origin_type;
    }
  }
  
  // Store the origin type for future dynamic inputs
  node.origin_type = origin_type;
}

function handleDisconnection(node, slot_idx, input_name) {
  const specialInputs = ["select", "sel_mode"];
  const inputToRemove = node.inputs[slot_idx];
  
  // Don't remove special inputs
  if (inputToRemove && !specialInputs.includes(inputToRemove.name)) {
    // Only remove if we have more than one dynamic input
    const dynamicInputCount = node.inputs.filter(input => input.name.includes(input_name)).length;
    if (dynamicInputCount > 1) {
      node.removeInput(slot_idx);
    }
  }
}

function reorganizeInputs(node, input_name) {
  const specialInputs = ["select", "sel_mode"];
  let slot_i = 1;
  
  // Rename all dynamic inputs sequentially
  for (let i = 0; i < node.inputs.length; i++) {
    let input_i = node.inputs[i];
    if (!specialInputs.includes(input_i.name) && input_i.name.includes(input_name)) {
      input_i.name = `${input_name}${slot_i}`;
      slot_i++;
    }
  }

  // Check if we need to add a new input slot
  const dynamicInputs = node.inputs.filter(input => input.name.includes(input_name));
  const lastDynamicInput = dynamicInputs[dynamicInputs.length - 1];
  
  if (lastDynamicInput && lastDynamicInput.link !== null) {
    // The last dynamic input is connected, so add a new one
    const inputType = node.origin_type || "*";
    node.addInput(`${input_name}${slot_i}`, inputType);
  }

  // Update widgets if they exist
  updateWidgets(node, input_name);
}

function updateWidgets(node, input_name) {
  if (!node.widgets) return;

  const inputWidget = node.widgets.find((w) => w.name.includes(input_name));
  if (inputWidget) {
    const specialInputs = ["select", "sel_mode"];
    const dynamicInputCount = node.inputs.filter(input => 
      !specialInputs.includes(input.name) && input.name.includes(input_name)
    ).length;
    
    inputWidget.options.max = dynamicInputCount;
    inputWidget.value = Math.min(
      Math.max(1, inputWidget.value),
      inputWidget.options.max
    );
  }
}
