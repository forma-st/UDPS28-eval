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

## Étape suivante : un vrai numéro de téléphone
Le relais est la base du futur numéro dédié : il suffira d'y ajouter un point d'entrée pour un opérateur téléphonique (par exemple Twilio : numéro français, reconnaissance et synthèse vocales), qui reprendra les mêmes consignes de régulateur et les mêmes scénarios qu'Eval.
