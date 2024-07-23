
import { getStorageValue, setStorageValue } from "../../scripts/utils.js";

export const griptapeMenuItems = [
  // // TODO: Figure out how to pull and set the environment variables
  // {
  //   content: "⚙️ Environment Variables",
  //   callback: (...args) => {
  //     const dialog = new GriptapeConfigDialog();
  //     dialog.show();
  //   },
  // },
  {
    content: "⭐ Star on Github",
    callback: (...args) => {
      window.open(
        "https://github.com/griptape-ai/ComfyUI-Griptape",
        "_blank"
      );
    },
  },
  {
    content: "📺 Watch Tutorials",
    callback: (...args) => {
      window.open(
        "https://youtube.com/playlist?list=PLZRzNKLLiEyeK9VN-i53sUU1v5vBLl-nG&si=M34Y00EDo-V_Qg0w",
        "_blank"
      );
    },
  },
  {
    content: "",
    disabled: true,
  },
  // // Set automatic node colors on or off
  // {
  //   content: "🎨 Node Colors On",
  //   callback: (...args) => {
  //     setStorageValue(
  //       "Comfy.Griptape.ColorNodes",
  //       true
  //     );
  //   },
  // },
  // {
  //   content: "🎨 Node Colors Off",
  //   callback: (...args) => {
  //     setStorageValue(
  //       "Comfy.Griptape.ColorNodes",
  //       false
  //     );
  //   },
  // },
  // {
  //   content: "",
  //   disabled: true,
  // },
  {
    content: "Griptape Home",
    callback: (...args) => {
      window.open("https://griptape.ai", "_blank");
    },
  },
  {
    content: "Griptape Cloud",
    callback: (...args) => {
      window.open("https://cloud.griptape.ai", "_blank");
    },
  },
  {
    content: "Griptape Docs",
    callback: (...args) => {
      window.open("https://docs.griptape.ai", "_blank");
    },
  },
  {
    content: "Griptape Tradeschool",
    callback: (...args) => {
      window.open("https://learn.griptape.ai", "_blank");
    },
  },
  {
    content: "Griptape Discord",
    callback: (...args) => 
      {
      window.open("https://discord.gg/gnWRz88eym", "_blank");
    },
  },
];

