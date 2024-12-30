
import { getStorageValue, setStorageValue } from "../../scripts/utils.js";
import { getVersion } from "./versions.js";

export const griptapeMenuItems = [
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
    content: "🐞 Log a feature request or issue",
    callback: (...args) => {
      window.open(
        "https://github.com/griptape-ai/ComfyUI-Griptape/issues/new",
        "_blank"
      );
    },
  },
  {
    content: `📦 Version: Loading...`,
    disabled: true, // This makes it non-clickable
  },
  {
    content: "----------------------",
    disabled: true,
  },
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

// Replace version placeholder
getVersion().then(version => {
  griptapeMenuItems[3].content = `📦 Version: ${version}`;
});
