import { keys_organized } from "./griptape_api_keys.js";

export function createSettings(app) {
    // Create the settings
    app.ui.settings.addSetting({
        id: `Griptape.default_config`,
        category: ["Griptape", "!Griptape", "default_config"],
        name: "default_config",
        type: "dict",
        defaultValue: "",
        tooltip: "To set this, use the Griptape: Set Default Agent node.",
        });
    app.ui.settings.addSetting({
        id: `Griptape.ollama_default_url`,
        category: ["Griptape", "Ollama", "ollama_default_url"],
        name: "default_url",
        type: "text",
        defaultValue: "http://127.0.0.1"
    });
    app.ui.settings.addSetting({
        id: `Griptape.allow_code_execution_dangerous`,
        category: ["Griptape", "!Griptape", "code_execution_dangerous"],
        name: "Enable Insecure Griptape Code: Run Python [DANGER]",
        type: "boolean",
        tooltip: "When enabled, the Griptape Code: Run Python node will not check for dangerous code.\n\n[WARNING] This setting is dangerous and should only be enabled if you know what you are doing.",
        defaultValue: false,
        onChange: (newVal, oldVal) => { if (newVal == true) { console.warn("Griptape Code: Dangerous Code Execution enabled: ", newVal)} },
        });
    app.ui.settings.addSetting({
        id: `Griptape.allow_code_execution`,
        category: ["Griptape", "!Griptape", "code_execution"],
        name: "Enable Griptape Code: Run Python Nodes",
        type: "boolean",
        tooltip: "When enabled, the `Griptape Code: Run Python` node will be available for use.",
        defaultValue: false,
        // onChange: (newVal, oldVal) => { console.log("Setting got changed!", newVal) },
        });

    Object.entries(keys_organized).forEach(([category, keys]) => {
      keys.forEach((key) => {
        app.ui.settings.addSetting({
          id: `Griptape.${key}`,
          category: ["Griptape", category, key],
          name: key,
          type: "text",
          defaultValue: "",
          /* To listen for changes, add an onChange parameter
        onChange: (newVal, oldVal) => { console.log("Setting got changed!") },
        */
        });
      });
    });

    }