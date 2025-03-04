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
  // Set the base name of the input node
  const input_name = getInputName(nodeData.name);

  const onConnectionsChange = nodeType.prototype.onConnectionsChange;
  nodeType.prototype.onConnectionsChange = function (
    type,
    index,
    connected,
    link_info
  ) {
    if (!link_info) return;
    if (type == 1) {
      handleInputConnection(this, link_info, app, input_name);

      const specialInputCount = countSpecialInputs(this);
      const select_slot = this.inputs.find((x) => x.name == "select");

      handleInputRemoval(this, index, connected, specialInputCount);
      renameInputs(this, input_name);
      updateWidgets(this, input_name, select_slot);
    }
  };
}

function countSpecialInputs(node) {
  const specialInputs = ["select", "sel_mode"];
  return node.inputs.filter((input) => specialInputs.includes(input.name))
    .length;
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
function handleInputConnection(node, link_info, app, input_name) {
  const origin_node = app.graph.getNodeById(link_info.origin_id);
  let origin_type = origin_node.outputs[link_info.origin_slot].type;

  if (origin_type == "*") {
    node.disconnectInput(link_info.target_slot);
  }

  for (let i in node.inputs) {
    if (node.inputs[i].name.includes(input_name)) {
      let input_i = node.inputs[i];
      for (let i in node.inputs) {
        let input_i = node.inputs[i];
        if (input_i.name != "select" && input_i.name != "sel_mode")
          input_i.type = origin_type;
      }
    }
  }
}

function handleInputRemoval(node, index, connected, converted_count) {
  const CONNECT_TOUCH = "LGraphNode.prototype.connect";
  const CONNECT_MOUSE = "LGraphNode.connect";
  const LOAD_GRAPH = "loadGraphData";

  function isValidRemovalContext(stackTrace) {
    return (
      !stackTrace.includes(CONNECT_TOUCH) &&
      !stackTrace.includes(CONNECT_MOUSE) &&
      !stackTrace.includes(LOAD_GRAPH)
    );
  }

  if (!connected && node.inputs.length > 1 + converted_count) {
    const stackTrace = new Error().stack;
    const inputToRemove = node.inputs[index];

    if (isValidRemovalContext(stackTrace) && inputToRemove.name !== "select") {
      node.removeInput(index);
    }
  }
}

function renameInputs(node, input_name) {
  let slot_i = 1;
  for (let i = 0; i < node.inputs.length; i++) {
    let input_i = node.inputs[i];
    if (input_i.name != "select" && input_i.name != "sel_mode") {
      input_i.name = `${input_name}${slot_i}`;
      slot_i++;
    }
  }

  let last_slot = node.inputs[node.inputs.length - 1];
  if (
    (last_slot.name == "select" &&
      last_slot.name != "sel_mode" &&
      node.inputs[node.inputs.length - 2].link != undefined) ||
    (last_slot.name != "select" &&
      last_slot.name != "sel_mode" &&
      last_slot.link != undefined)
  ) {
    node.addInput(`${input_name}${slot_i}`, node.origin_type);
  }
}

function updateWidgets(node, input_name, select_slot) {
  if (!node.widgets) return;

  const inputWidget = node.widgets.find((w) => w.name.includes(input_name));
  if (inputWidget) {
    inputWidget.options.max = select_slot
      ? node.inputs.length - 1
      : node.inputs.length;
    inputWidget.value = Math.min(
      Math.max(1, inputWidget.value),
      inputWidget.options.max
    );
  }
}
