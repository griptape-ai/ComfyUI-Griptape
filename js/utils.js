
export function fitHeight(node) {
    node.onResize?.(node.size);
    node.setSize([node.size[0], node.computeSize([node.size[0], node.size[1]])[1]+10])
    node?.graph?.setDirtyCanvas(true, true);
}

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

const COMMENT_TYPE = "comment-widget";
function skewColor(color) {
    
    // Ensure the color is in the correct format
    color = color.replace(/^#/, '');
    
    // Parse the color, handling both 3-digit and 6-digit hex
    let r, g, b;
    if (color.length === 3) {
        r = parseInt(color[0] + color[0], 16);
        g = parseInt(color[1] + color[1], 16);
        b = parseInt(color[2] + color[2], 16);
    } else if (color.length === 6) {
        r = parseInt(color.slice(0, 2), 16);
        g = parseInt(color.slice(2, 4), 16);
        b = parseInt(color.slice(4, 6), 16);
    } else {
        return color; // Return original color if invalid
    }
    
    // Calculate the average brightness
    const avg = (r + g + b) / 3;
    
    // Determine new color based on average brightness
    const newColor = avg < 128 ? "#000000" : "#ffffff";
    
    return newColor;
}


export function commentWidget(node, widget) {
    const nodeColors = LGraphCanvas.node_colors;
    let link_color = skewColor(LiteGraph.NODE_TITLE_COLOR);
    if (widget.type === COMMENT_TYPE) return;

    // Store original properties
    widget.origType = widget.type;
    widget.origComputeSize = widget.computeSize;
    widget.origSerializeValue = widget.serializeValue;
    widget.origDraw = widget.draw;

    // Change widget type
    widget.type = COMMENT_TYPE;

    // Modify computeSize to give it a specific height
    widget.computeSize = () => [node.size[0], 25]; // Adjust height as needed

    // Prevent serialization
    widget.serializeValue = () => undefined;

    // Custom draw function for comment style
    widget.draw = function(ctx, node, widgetWidth, y, headerHeight) {
        if (this.inputEl) {
            // Style the input element
            Object.assign(this.inputEl.style, {
                backgroundColor: "#4a4a4a",
                color: "#333333",
                fontWeight: "200",
                border: "none",
                padding: "5px",
                width: "100%",
                boxSizing: "border-box"
            });
            this.inputEl.readOnly = true;
        }

        // Draw the comment text
        ctx.save();
        ctx.fillStyle = link_color;
        // ctx.fillStyle = "#ffffff";
        ctx.font = "bold 12px Lato";
        ctx.fillText(this.value.toUpperCase(), 18, y + 20);
        ctx.restore();
    };

    // Ensure the widget doesn't accept inputs
    if (node.inputs) {
        const input = node.inputs.find(input => input.name === widget.name);
        if (input) {
            input.type = -1; // This prevents connections to the input
        }
    }
}

export function uncommentWidget(widget) {
    if (widget.type !== COMMENT_TYPE) return;

    // Restore original properties
    widget.type = widget.origType;
    widget.computeSize = widget.origComputeSize;
    widget.serializeValue = widget.origSerializeValue;
    widget.draw = widget.origDraw;

    delete widget.origType;
    delete widget.origComputeSize;
    delete widget.origSerializeValue;
    delete widget.origDraw;

    // Restore input functionality if needed
    const node = widget.parent;
    if (node && node.inputs) {
        const input = node.inputs.find(input => input.name === widget.name);
        if (input) {
            input.type = widget.origType; // Restore the original input type
        }
    }

    // Reset any styling on the input element
    if (widget.inputEl) {
        widget.inputEl.style = {};
        widget.inputEl.readOnly = false;
    }
}
