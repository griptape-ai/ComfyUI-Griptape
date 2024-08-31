export function fitHeight(node) {
    node.onResize?.(node.size);
    node.setSize([node.size[0], node.computeSize([node.size[0], node.size[1]])[1]])
    node?.graph?.setDirtyCanvas(true, true);
}
// export function fitHeight(node) {
//     if (!node) return null;

//     try {
//         node.onResize?.(node.size);
        
//         // Get the base height from computeSize
//         let computedHeight = node.computeSize([node.size[0], node.size[1]])[1];
        
//         // Account for multiline widgets
//         if (node.widgets) {
//             for (const widget of node.widgets) {
//                 if (widget.type === "textarea" || widget.options?.multiline) {
//                     // Adjust height based on content
//                     const lines = (widget.value || "").split("\n").length;
//                     const lineHeight = 20; // Adjust this value based on your CSS
//                     const widgetHeight = Math.max(lines * lineHeight, widget.options?.minHeight || 60);
//                     computedHeight += widgetHeight - (widget.options?.minHeight || 60); // Add extra height
//                 }
//             }
//         }

//         // Set minimum height
//         computedHeight = Math.max(computedHeight, node.options?.minHeight || 100);

//         if (computedHeight !== node.size[1]) {
//             node.setSize([node.size[0], computedHeight]);
//             node.graph?.setDirtyCanvas(true, true);
//         }

//         return [node.size[0], computedHeight];
//     } catch (error) {
//         console.error("Error in fitHeight:", error);
//         return null;
//     }
// }

export function node_add_dynamic(nodeType, prefix, type='*', count=-1) {
    const onNodeCreated = nodeType.prototype.onNodeCreated
    nodeType.prototype.onNodeCreated = function () {
        const me = onNodeCreated?.apply(this)
        this.addInput(`${prefix}_1`, type);
        return me
    }

    const onConnectionsChange = nodeType.prototype.onConnectionsChange
    nodeType.prototype.onConnectionsChange = function (slotType, slot, event, link_info, data) {
        const me = onConnectionsChange?.apply(this, arguments)
        if (slotType === TypeSlot.Input) {
            if (!this.inputs[slot].name.startsWith(prefix)) {
                return
            }

            // remove all non connected inputs
            if (event == TypeSlotEvent.Disconnect && this.inputs.length > 1) {
                if (this.widgets) {
                    const w = this.widgets.find((w) => w.name === this.inputs[slot].name)
                    if (w) {
                        w.onRemoved?.()
                        this.widgets.length = this.widgets.length - 1
                    }
                }
                this.removeInput(slot)

                // make inputs sequential again
                for (let i = 0; i < this.inputs.length; i++) {
                    const name = `${prefix}_${i + 1}`
                    this.inputs[i].label = name
                    this.inputs[i].name = name
                }
            }

            // add an extra input
            if (count-1 < 0) {
                count = 1000;
            }
            const length = this.inputs.length - 1;
            if (length < count-1 && this.inputs[length].link != undefined) {
                const nextIndex = this.inputs.length
                const name = `${prefix}_${nextIndex + 1}`
                this.addInput(name, type)
            }

            if (event === TypeSlotEvent.Connect && link_info) {
                const fromNode = this.graph._nodes.find(
                    (otherNode) => otherNode.id == link_info.origin_id
                )
                if (fromNode) {
                    const old_type = fromNode.outputs[link_info.origin_slot].type;
                    this.inputs[slot].type = old_type;
                }
            } else if (event === TypeSlotEvent.Disconnect) {
                this.inputs[slot].type = type
                this.inputs[slot].label = `${prefix}_${slot + 1}`
            }
        }
        return me;
    }
    return nodeType;
}

// TAKEN FROM:  ComfyUI\web\extensions\core\widgetInputs.js
// IN CASE someone tries to tell you they invented core functions...
// they simply are not exported
//
const CONVERTED_TYPE = "converted-widget";

export function hideWidget(node, widget, suffix = "") {
	if (widget.type?.startsWith(CONVERTED_TYPE)) return;
	widget.origType = widget.type;
	widget.origComputeSize = widget.computeSize;
	widget.origSerializeValue = widget.serializeValue;
	widget.computeSize = () => [0, -4]; // -4 is due to the gap litegraph adds between widgets automatically
	widget.type = CONVERTED_TYPE + suffix;
	widget.serializeValue = () => {
		// Prevent serializing the widget if we have no input linked
		if (!node.inputs) {
			return undefined;
		}
		let node_input = node.inputs.find((i) => i.widget?.name === widget.name);

		if (!node_input || !node_input.link) {
			return undefined;
		}
		return widget.origSerializeValue ? widget.origSerializeValue() : widget.value;
	};

	// Hide any linked widgets, e.g. seed+seedControl
	if (widget.linkedWidgets) {
		for (const w of widget.linkedWidgets) {
			hideWidget(node, w, ":" + widget.name);
		}
	}
}

export function showWidget(widget) {
	widget.type = widget.origType;
	widget.computeSize = widget.origComputeSize;
	widget.serializeValue = widget.origSerializeValue;

	delete widget.origType;
	delete widget.origComputeSize;
	delete widget.origSerializeValue;

	// Hide any linked widgets, e.g. seed+seedControl
	if (widget.linkedWidgets) {
		for (const w of widget.linkedWidgets) {
			showWidget(w);
		}
	}
}