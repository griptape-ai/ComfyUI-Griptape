export function setupFlowNodes(nodeType, nodeData, app) {
  if (nodeData.name === "Griptape Start Workflow") {
    setupFlowStartNode(nodeType, nodeData, app);
  }

  if (nodeData.name === "Griptape End Workflow") {
    setupflowEndNode(nodeType, nodeData, app);
  }
}
function setupflowEndNode(nodeType, nodeData, app) {
  const onNodeCreated = nodeType.prototype.onNodeCreated;
  nodeType.prototype.onNodeCreated = function () {
    onNodeCreated?.apply(this, arguments);
  };
  const input_name = "get_property_";
  const onConnectionsChange = nodeType.prototype.onConnectionsChange;
  nodeType.prototype.onConnectionsChange = function (
    type,
    index,
    connected,
    link_info
  ) {
    if (!link_info) return;

    const target_id = link_info.target_id;
    const target_inputs = app.graph.getNodeById(target_id).inputs;

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
      input_i.type = "*";
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
    node.addInput(`${input_name}${slot_i}`, "*");
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

function setupFlowStartNode(nodeType, nodeData, app) {
  // Check for connections change
  const onConnectionsChange = nodeType.prototype.onConnectionsChange;
  nodeType.prototype.onConnectionsChange = function (
    type, // 1 = input, 2 = output
    index, // the index in the connection
    connected, // if it is connected or not
    link_info // link info with all the information
  ) {
    if (!link_info) return;

    const widget_name = "property";
    const label_widget = this.widgets.find((w) => w.name === "label");
    if (type == 2) {
      if (connected == true) {
        const target_id = link_info.target_id;
        const target_slot = link_info.target_slot;
        const target_type = link_info.type;
        const target_node = app.graph.getNodeById(target_id);
        const widgets = target_node.widgets;
        const inputs = target_node.inputs;
        const target_input = inputs[target_slot];
        // check if target_input.name exists
        if (!target_input) {
          console.log("This has already been connected - we'll just return.");
          return;
        }
        const target_widget_name = target_input.name;
        const target_widget = widgets.find(
          (w) => w.name === target_widget_name
        );
        const target_value = target_widget.value;

        // Set the input label
        label_widget.value = target_widget_name;

        // Create the appropriate widget
        let widget = null;

        // delete the existing property widget if it exists:
        const existing_widget = this.widgets.find(
          (w) => w.name === widget_name
        );
        if (existing_widget) {
          const widgetIndex = this.widgets.findIndex(
            (w) => w.name === widget_name
          );
          this.widgets.splice(widgetIndex, 1);
        }

        // Create the new widget
        let new_widget_type = target_type;
        if (target_type == "FLOAT" || target_type == "INT") {
          new_widget_type = "number";
        }
        if (target_type == "BOOLEAN") {
          new_widget_type = "toggle";
        }

        widget = this.addWidget(
          new_widget_type,
          widget_name,
          target_value,
          () => {},
          {
            serialize: true,
          }
        );
        for (const key in target_widget.options) {
          widget.options[key] = target_widget.options[key];
        }
      } else {
        label_widget.value = "Input Label";

        // find the widget with the name and remove it
        const widgetIndex = this.widgets.findIndex(
          (w) => w.name === widget_name
        );

        // If widget exists, remove it from the widgets array
        if (widgetIndex !== -1) {
          this.widgets.splice(widgetIndex, 1);

          // Force the node to update its UI
          this.setDirtyCanvas(true, true);
        }

        // Now re-create the property widget
        const widget = this.addWidget("STRING", widget_name, "", () => {}, {
          serialize: true,
        });
      }
    }
    // Call original handler if it exists
    if (onConnectionsChange) onConnectionsChange.apply(this, arguments);
  };
}
function none() {
  console.log("None");
}
