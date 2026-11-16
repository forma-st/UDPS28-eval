// Serveur relais « Eval » : garde la clé API Anthropic côté serveur.
// Les tablettes n'ont qu'un code d'accès ; le relais vérifie ce code, limite le modèle et la taille
// des réponses, puis transmet la demande à l'API Claude avec le SDK officiel.
import Anthropic from "@anthropic-ai/sdk";
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const ALLOWED_MODELS = ["claude-opus-5-5", "claude-sonnet-5-5"];
const ALLOWED_BETAS = ["server-side-fallback-2026-07-01"];
const MAX_TOKENS = 16000;

const sameCode = (a, b) => {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
};

export default {
  async fetch(request, env) {
    const cors = {
      "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": request.headers.get("Access-Control-Request-Headers") || "*",
      "Access-Control-Max-Age": "86400",
    };
    const reply = (data, status) =>
      new Response(JSON.stringify(data), { status, headers: { ...cors, "content-type": "application/json" } });
    const fail = (status, type, message) => reply({ type: "error", error: { type, message } }, status);

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const url = new URL(request.url);
    const routes = ["/v1/messages", "/eleven/session"];
    if (request.method !== "POST" || !routes.includes(url.pathname)) return fail(404, "not_found_error", "Relais Eval : route inconnue.");

    const code = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
    if (!env.ACCESS_CODE || !sameCode(code, env.ACCESS_CODE)) return fail(401, "authentication_error", "Code d'accès invalide.");

    // Appel vocal ElevenLabs : la clé reste ici ; la tablette reçoit un laissez-passer à usage unique.
    if (url.pathname === "/eleven/session") {
      if (!env.ELEVENLABS_API_KEY || !env.ELEVENLABS_AGENT_ID) return fail(501, "not_configured", "ElevenLabs n'est pas configuré sur le relais.");
      const el = new ElevenLabsClient({ apiKey: env.ELEVENLABS_API_KEY, ...(env.ELEVENLABS_BASE_URL ? { baseUrl: env.ELEVENLABS_BASE_URL } : {}) });
      const agentId = env.ELEVENLABS_AGENT_ID;
      const out = {};
      await Promise.allSettled([
        el.conversationalAi.conversations.getWebrtcToken({ agentId }).then((r) => { out.token = r.token; }),
        el.conversationalAi.conversations.getSignedUrl({ agentId }).then((r) => { out.signedUrl = r.signedUrl; }),
      ]);
      if (!out.token && !out.signedUrl) return fail(502, "api_error", "ElevenLabs n'a pas ouvert la session (clé ou identifiant d'agent ?).");
      return reply(out, 200);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return fail(400, "invalid_request_error", "Corps de requête illisible.");
    }
    if (!ALLOWED_MODELS.includes(body.model)) return fail(400, "invalid_request_error", "Modèle non autorisé par le relais.");

    const betas = (request.headers.get("anthropic-beta") || "")
      .split(",").map((s) => s.trim()).filter((b) => ALLOWED_BETAS.includes(b));
    const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY, baseURL: env.ANTHROPIC_BASE_URL || undefined });
    try {
      const params = {
        model: body.model,
        max_tokens: Math.min(Number(body.max_tokens) || 4000, MAX_TOKENS),
        system: body.system,
        messages: body.messages,
        ...(body.thinking ? { thinking: body.thinking } : {}),
        ...(body.output_config ? { output_config: body.output_config } : {}),
        ...(body.fallbacks ? { fallbacks: body.fallbacks } : {}),
        ...(betas.length ? { betas } : {}),
      };
      if (body.stream === true) {
        // Réponse en continu (appel vocal) : le flux d'événements est transmis tel quel.
        const upstream = await client.beta.messages.create({ ...params, stream: true }).asResponse();
        return new Response(upstream.body, {
          status: upstream.status,
          headers: { ...cors, "content-type": "text/event-stream", "cache-control": "no-cache" },
        });
      }
      const message = await client.beta.messages.create(params);
      return reply(message, 200);
    } catch (err) {
      if (err instanceof Anthropic.APIError && err.status) {
        return reply(err.error ?? { type: "error", error: { type: "api_error", message: err.message } }, err.status);
      }
      return fail(502, "api_error", "Relais : l'API Claude est injoignable.");
    }
  },
};
