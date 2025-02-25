import {
  gtUIAddUploadWidget,
  gtUIAddUrlButtonWidget,
  gtUIAddButtonWidget,
} from "./gtUIUtils.js";
const API_PROVIDERS = {
  Anthropic: { url: "https://console.anthropic.com/settings/keys" },
  Amazon: {
    url: "https://console.aws.amazon.com/iam/home?#/security_credentials",
  },
  Azure: { url: "https://portal.azure.com/" },
  "Black Forest Labs": { url: "https://api.us1.bfl.ai/auth/profile" },
  Cohere: { url: "https://dashboard.cohere.com/api-keys" },
  ElevenLabs: { url: "https://elevenlabs.io/app/settings/api-keys" },
  Google: { url: "https://console.cloud.google.com/apis/credentials" },
  LeonardoAI: { url: "https://app.leonardo.ai/api-access" },
  Grok: { url: "https://console.x.ai" },
  Groq: { url: "https://console.groq.com/keys" },
  Serper: { url: "https://serper.dev/api-key" },
  OpenAI: { url: "https://platform.openai.com/account/api-keys" },
  HuggingFace: { url: "https://huggingface.co/settings/tokens" },
  "LM Studio": {
    url: "https://lmstudio.ai/",
    buttonText: "Download LM Studio",
  },
  Ollama: {
    url: "https://ollama.com",
    buttonText: "Download Ollama",
  },
  Voyage: {
    url: "https://dashboard.voyageai.com/api-keys",
  },
  Tavily: {
    url: "https://app.tavily.com/",
  },
  Exa: { url: "https://dashboard.exa.ai/api-keys" },
  Pinecone: { url: "https://app.pinecone.io/keys" },
  Qdrant: { url: "https://cloud.qdrant.io" },
};

export function setupApiKeyButtons(nodeType, nodeData, app) {
  const providerName = Object.keys(API_PROVIDERS).find((provider) =>
    nodeData.name.includes(provider)
  );

  if (providerName) {
    const provider = API_PROVIDERS[providerName];
    const buttonText = provider.buttonText || `Get ${providerName} API Key`;

    gtUIAddUrlButtonWidget(nodeType, buttonText, provider.url, "");
  }
}
