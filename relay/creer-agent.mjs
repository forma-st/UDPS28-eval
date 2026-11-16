// Crée l'agent vocal « régulation 15 » d'Eval chez ElevenLabs, avec les bons réglages.
// Usage :  ELEVENLABS_API_KEY=... npm run creer-agent            (agent privé, via le relais : recommandé)
//          ELEVENLABS_API_KEY=... npm run creer-agent -- --public (agent public, pour un essai rapide sans relais)
// Variable facultative : ELEVENLABS_VOICE_ID (voix française choisie dans la bibliothèque de voix ElevenLabs).
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const apiKey = process.env.ELEVENLABS_API_KEY;
if (!apiKey) {
  console.error("Indiquez la clé : ELEVENLABS_API_KEY=xxxx npm run creer-agent");
  process.exit(1);
}
const isPublic = process.argv.includes("--public");
const client = new ElevenLabsClient({ apiKey });

const agent = await client.conversationalAi.agents.create({
  name: "Eval UDPS 28 - Régulation 15",
  conversationConfig: {
    agent: {
      firstMessage: "SAMU, centre 15, j’écoute.",
      language: "fr",
      prompt: {
        // Le rôle détaillé et le scénario sont envoyés par Eval au début de chaque appel.
        prompt: "Tu joues la régulation médicale du SAMU (le 15) dans un exercice de formation aux premiers secours. Tu parles français, au téléphone, en phrases courtes.",
        llm: "claude-sonnet-5-5",
      },
    },
    tts: { modelId: "eleven_flash_v2_5", ...(process.env.ELEVENLABS_VOICE_ID ? { voiceId: process.env.ELEVENLABS_VOICE_ID } : {}) },
    // « patient » : l'agent laisse le temps d'hésiter avant de répondre ; relance après 8 s de silence.
    turn: { turnEagerness: "patient", turnTimeout: 8 },
  },
  platformSettings: {
    // Eval envoie à chaque appel le rôle, le scénario, le niveau et la première phrase.
    overrides: { conversationConfigOverride: { agent: { firstMessage: true, language: true, prompt: { prompt: true } }, tts: { voiceId: true } } },
    auth: { enableAuth: !isPublic },
  },
});

console.log("\nAgent créé. Identifiant :", agent.agentId);
console.log(isPublic
  ? "Mode public : collez cet identifiant dans Eval (Réglages > Régulation SAMU simulée > Voix de l'appel)."
  : "Enregistrez-le sur le relais :  npx wrangler secret put ELEVENLABS_AGENT_ID");
console.log("Puis choisissez une voix française dans le tableau de bord ElevenLabs (Agents > Eval UDPS 28 > Voice).\n");
