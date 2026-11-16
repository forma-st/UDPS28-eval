# Serveur relais Eval (régulation SAMU simulée)

Le relais garde la clé API Anthropic sur un serveur : les tablettes n'ont qu'un **code d'accès**.
Il vérifie ce code, n'autorise que le modèle utilisé par Eval, limite la taille des réponses, puis transmet la demande à l'API Claude avec le SDK officiel.

Hébergement prévu : Cloudflare Workers (offre gratuite suffisante pour une association).

## Mise en ligne (une fois)
1. Créer un compte sur console.anthropic.com, ajouter un moyen de paiement et créer une **clé API** (fixer une limite de dépense mensuelle dans la console).
2. Créer un compte gratuit sur cloudflare.com.
3. Sur un ordinateur avec Node.js, dans ce dossier `relay` :

```bash
npm install
```

```bash
npx wrangler login
```

```bash
npx wrangler secret put ANTHROPIC_API_KEY
```

```bash
npx wrangler secret put ACCESS_CODE
```

```bash
npx wrangler deploy
```

La dernière commande affiche l'adresse du relais (par exemple `https://eval-relais.<compte>.workers.dev`).

4. Dans Eval : Réglages › Régulation SAMU simulée › « Serveur relais de l'organisme », coller l'adresse et le code d'accès, puis « Tester la connexion ».

Pour changer le code (formateur parti, code diffusé) : relancer `npx wrangler secret put ACCESS_CODE` ; l'ancien code ne fonctionne plus aussitôt.

## Appel au 15 avec ElevenLabs (voix naturelle)
Le relais ouvre aussi les appels vocaux ElevenLabs : la clé ElevenLabs reste sur le relais, la tablette ne reçoit qu'un laissez-passer à usage unique.

1. Sur elevenlabs.io : Profil › API Keys › créer une clé (droits « ElevenAgents » au minimum).
2. Dans ce dossier `relay`, créer l'agent avec les bons réglages (Claude Sonnet 5.5, français, tours de parole « patients », réglages par appel autorisés) :

```bash
ELEVENLABS_API_KEY=votre_cle npm run creer-agent
```

3. Enregistrer la clé et l'identifiant d'agent affiché sur le relais, puis redéployer :

```bash
npx wrangler secret put ELEVENLABS_API_KEY
```

```bash
npx wrangler secret put ELEVENLABS_AGENT_ID
```

```bash
npx wrangler deploy
```

4. Dans le tableau de bord ElevenLabs (Agents › Eval UDPS 28 - Régulation 15 › Voice), choisir une **voix française**.
5. Dans Eval : Réglages › Régulation SAMU simulée › Voix de l'appel : « ElevenLabs », Accès : « Par le serveur relais ».

Essai rapide sans relais : `npm run creer-agent -- --public` crée un agent public ; collez son identifiant dans Eval (« Agent public »). Limitez-le alors à votre adresse (Security › Allowlist) et fixez un plafond de dépense, car quiconque connaît l'identifiant peut l'utiliser.

## Étape suivante : un vrai numéro de téléphone
Le relais est la base du futur numéro dédié : l'agent ElevenLabs peut être relié à un numéro de téléphone (Twilio ou SIP) depuis son tableau de bord ; il restera à lui transmettre le scénario choisi pour chaque appel.
