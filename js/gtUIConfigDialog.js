import { app } from "../../../scripts/app.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";
import { ComfyDialog } from "../../../scripts/ui/dialog.js";

export class GriptapeConfigDialog {
  constructor() {
    this.element = $el("div.comfy-modal", { parent: document.body }, [
      $el("div.comfy-modal-content", [
        $el("p", { $: (p) => (this.textElement = p) }),
        ...this.createButtons(),
      ]),
    ]);
  }

  show(html2) {
    const html = $el("div", [
      $el("h1", { textContent: "Griptape Setup" }),
      $el("p", { textContent: "Coming soon..." }),
    ]);
    this.textElement.replaceChildren(html);
    this.element.style.display = "flex";
  }

  createButtons() {
    const buttonContainer = $el(
      "div",
      { style: { display: "flex", gap: "10px", justifyContent: "center" } },
      [
        $el("button", {
          type: "button",
          textContent: "Close",
          style: {
            padding: "8px",
          },
          onclick: () => this.close(),
        }),
        $el("button", {
          type: "button",
          textContent: "Save",
          style: {
            padding: "8px",
          },
          onclick: () => this.save(),
        }),
      ]
    );
    return [buttonContainer];
  }
  save() {
    console.log("Save action triggered");
  }

  close() {
    this.element.style.display = "none";
  }
}
