# Eval · UDPS 28 (version 2.13.1)

Application de terrain pour les formations PSE1, PSE2, PIC F, PAE FPSE et Chef d'équipe (CE). Elle fonctionne **entièrement sans réseau**.

## Fonctionnement
1. **Formations** (1er onglet) : choisir ou créer une formation (PSE1, PSE2…), les formateurs de la session et les participants (saisie un par un ou liste collée).
2. **Cas concret** : la fiche formative est préremplie. On choisit les apprenants et les formateurs dans des listes déroulantes, puis on note A / B / C / NE et on écrit une observation par apprenant.
3. **Participant** : il a sa fiche de **technicité** (cases « Fait ») et sa **fiche de certification individuelle**.
   - Chaque cas concret enregistré devient un **passage** (N°01 à N°06). Une note A ou B donne « A » (acquis), une note C donne « NA » (non acquis).
   - La ligne **A** passe à OUI quand toutes les techniques de la fiche de technicité sont cochées.
   - La ligne **B** passe à OUI quand toutes les compétences sont validées.
   - La validation finale **APTE / INAPTE** se calcule automatiquement.
4. **Export** : chaque fiche sort en PDF au format des fiches d'origine. On peut aussi exporter un dossier PDF par participant, toutes les fiches d'une formation, un tableur CSV ou une sauvegarde. Le menu de partage d'Android propose ensuite mail, Bluetooth, Quick Share, Drive, WhatsApp ou Fichiers.
5. **Réglages** : liste des formateurs, logo sur les PDF, sauvegarde complète, import sur une autre tablette.
6. **Grilles** : toutes les grilles sont modifiables. Pour ajouter une formation (SST, PSC…), dupliquer les trois grilles PSE1 et changer le nom de formation.

## Règles des référentiels ANPS 2025 appliquées automatiquement
- **Passages** : chaque cas concret enregistré devient un passage (3 minimum, 6 maximum). Le niveau reporté (A, B ou C) est le plus faible des critères liés à la compétence ; NE est ignoré.
- **Niveau d'acquisition** : « 3B » signifie 3 validations au niveau B ou mieux, « 2A » 2 validations au niveau A. La compétence passe à OUI dès que le compte est atteint. Le formateur peut toujours forcer OUI ou NON.
- **Conditions particulières**
  - PSE1, compétence 3 : au moins un passage avec le 3e et le 4e regard acquis.
  - PSE1, compétence 4 : au moins une prise en charge d'arrêt cardiaque (situation cochée sur le cas concret).
  - PSE2, compétence 2 : au moins un relevage.
  - PSE2, compétence 6 : au moins un bilan complet.
- **A** : OUI quand toutes les techniques de la fiche de technicité sont cochées « Fait ».
- **B** : OUI quand toutes les compétences sont validées.
- **C** : OUI quand le participant est pointé présent à toutes les journées (feuille de présence).
- **D** : OUI à partir de 12/20 au questionnaire. Entre 10 et 11 : entretien de rattrapage avec le responsable pédagogique. Sous 10 : NON.
- **Dossier** par participant, dans l'ordre du référentiel : technicité, fiches d'évaluation, certification.

## Version 2.13.1 : agent vocal de l'UDPS 28 branché par défaut
- L'agent ElevenLabs « Eval UDPS 28 - Régulation 15 » est créé (Claude Sonnet 5.5, français, tours de parole patients) et utilisé par défaut sur tous les appareils, sans réglage.
- Agent public protégé : seules l'application publiée (forma-st.github.io) et l'application Android peuvent l'appeler ; 3 appels simultanés et 40 appels par jour au maximum ; 10 minutes au maximum par appel.
- Quand le serveur relais sera en ligne, passer l'agent en privé et l'accès d'Eval en « Par le serveur relais ».

## Version 2.13 : appel au 15 avec une voix naturelle (ElevenLabs)
- Nouveau moteur d'appel **ElevenLabs** : voix française naturelle, réponse en moins d'une seconde, tours de parole gérés par l'agent (il attend pendant les hésitations), et on peut couper la parole au régulateur comme au téléphone. Le cerveau reste Claude (Sonnet 5.5), avec le même rôle d'assistant de régulation puis de médecin régulateur, le scénario et le niveau choisis.
- Plus de reconnaissance vocale du téléphone, donc plus de bip, et l'enregistrement pour la réécoute fonctionne sur tous les appareils.
- Correction du bilan inchangée (Claude Opus 5.5) ; sans accès à Claude, l'appel garde sa transcription et son enregistrement.
- Réglages › Régulation SAMU simulée › « Voix de l'appel » : ElevenLabs (par le serveur relais, ou agent public pour un essai) ou voix du téléphone (sans compte). Mise en place : `relay/LISEZMOI.md`.

## Version 2.12 : réécouter l'appel
- L'appel à la voix est **enregistré** (voix de l'apprenant et du régulateur sur le haut-parleur) et se **réécoute** dans l'écran de correction.
- Le son reste **sur l'appareil**, n'est jamais envoyé, et est **effacé automatiquement au bout de 30 minutes**. Un badge « ● Enregistrement » est visible pendant l'appel ; l'écran d'avant l'appel rappelle de prévenir l'apprenant.
- Certains téléphones ne peuvent pas écouter (reconnaissance vocale) et enregistrer en même temps : l'application le détecte, arrête l'enregistrement et l'appel continue normalement.
- Désactivable dans Réglages › Régulation SAMU simulée.

## Version 2.11 : appel plus fluide, régulation médicale approfondie
- **Rien à lire pendant l'appel** : écran de téléphone seulement (qui parle, durée, boutons). La transcription complète s'affiche à la fin, avec la correction.
- **L'apprenant n'est plus coupé à la moindre hésitation** : les morceaux de phrase sont recollés et le message ne part qu'après une vraie pause. Durée réglable : courte (1,5 s), normale (2,3 s), longue (3,2 s), dans Réglages ou avant l'appel.
- **Régulation plus réaliste** : l'assistant de régulation prend l'appelant, le numéro de rappel, l'adresse complète et le motif, puis passe le médecin régulateur. Le médecin mène un interrogatoire médical complet (circonstances, urgence vitale chiffrée, douleur, examen, antécédents, traitements, allergies, gestes et leur effet, évolution), fait préciser, demande de nouvelles mesures, relève les incohérences, puis donne sa décision (moyen engagé, consignes précises, délai de rappel). En niveau certification, il exige le collationnement des consignes.
- Mode écrit toujours possible, choisi avant l'appel (salle bruyante, pas de micro).

## Version 2.10 : appel au 15 en conversation continue
- **Comme un vrai appel** : plus de bouton entre les phrases. L'application écoute, détecte la fin de la prise de parole (courte pause), envoie seule, le régulateur répond à voix haute, puis l'écoute reprend.
- Le régulateur commence à parler dès sa première phrase, sans attendre la fin de sa réponse.
- Boutons pendant l'appel : couper / rouvrir le micro, interrompre le régulateur, passer à l'écrit, rappel pour le bilan de surveillance, raccrocher et corriger. Après un long silence, le régulateur demande « Allô ? Vous m'entendez ? », puis le micro se coupe.
- Modèles : Claude Sonnet 5.5 sans réflexion préalable pour la conversation (réponse la plus rapide), Claude Opus 5.5 pour la correction du bilan (la plus fiable). Le serveur relais accepte les deux et transmet la réponse en continu.

## Version 2.9 : appel au 15 avec un régulateur simulé par l'IA
- Sur chaque scénario (et sur la fiche d'évaluation créée depuis un scénario) : **« Appeler le 15 »**. L'apprenant parle au micro de la tablette ou du téléphone (ou écrit) ; un régulateur simulé par l'IA Claude décroche, pose les questions d'un vrai régulateur et donne une décision cohérente avec le scénario. Le scénario sert à l'IA pour savoir ce qu'un bon bilan doit contenir ; elle ne le révèle pas.
- Trois niveaux : débutant (guide l'apprenant), standard, certification (exigeant). Bouton « Rappel : bilan de surveillance ».
- **« Raccrocher et corriger le bilan »** : note sur 10, 11 critères (présentation, adresse, motif, victimes, bilan vital, paramètres, bilan complémentaire, gestes, demande, clarté, prise en compte des consignes), points forts, points à améliorer, exemple de bilan bien transmis et proposition A / B / C pour la fiche d'évaluation (le formateur décide). PDF disponible ; les appels restent listés sur le scénario.
- **Accès à l'IA** (Réglages › Régulation SAMU simulée) : soit une clé API Anthropic enregistrée sur l'appareil, soit le **serveur relais** de l'organisme (dossier `relay/`, voir son LISEZMOI) qui garde la clé et ne donne aux tablettes qu'un code d'accès. Il faut du réseau pendant l'appel ; le reste de l'application reste hors ligne.
- Confidentialité : seuls le scénario et ce qui est dit pendant l'appel sont envoyés. Le nom de l'apprenant reste sur l'appareil.
- Coût indicatif : quelques centimes à une vingtaine de centimes par appel corrigé (modèle Claude Opus 5.5).

## Version 2.8 : 60 scénarios et onglet Scénarios
- **30 scénarios PSE1 et 30 scénarios PSE2**, répartis sur les jours de formation.
- Nouvel onglet **Scénarios** dans la barre du bas : consulter, imprimer, créer ou modifier les scénarios sans ouvrir de formation, avec un choix PSE1 / PSE2.
- Depuis une formation, le planning, la liste de matériel et « Évaluer ce cas » restent disponibles pour les scénarios du même niveau.

## Version 2.7 : éditeur de scénarios
- **Créer un scénario** depuis la liste des scénarios : identification, situations travaillées (cochées d’office sur la fiche d’évaluation), objectifs, message d’alerte, rôles (autant de victimes et de tiers que nécessaire), évolution « si… alors… », attendus, observation critère par critère, matériel, sécurité, débriefing.
- **Modifier** un scénario fourni (marqué « Modifié », avec « Rétablir l’original ») ou **dupliquer** un scénario pour en faire une variante.
- **Partager mes scénarios** : fichier .json à envoyer aux autres formateurs ; ils l’importent dans Réglages › Importer. Les scénarios personnels sont aussi dans la sauvegarde complète.

## Version 2.6 : scénarios de cas concrets
- **32 scénarios** prêts à jouer (17 PSE1, 15 PSE2), classés selon la progression de la formation (J1 à J5 en PSE1, J1 à J4 en PSE2) et du plus simple au plus complet.
- Chaque fiche donne : thème, objectifs, lieu, équipe, message d’alerte, contexte, briefings de la victime et des témoins (jeu, constantes à donner, maquillage), briefing des secouristes, évolution selon les actions, gestes attendus, points observés sur la fiche d’évaluation, matériel (décor, maquillage, accessoires, matériel de secours), sécurité de l’exercice et questions de débriefing.
- Dans une formation : bouton **« Choisir et préparer les scénarios »**, filtre par jour, ajout au planning, cases à cocher du matériel prêt.
- **« Évaluer ce cas »** crée la fiche d’évaluation avec le thème, les situations travaillées déjà cochées et le rappel de ce qu’il faut observer.
- PDF : fiche scénario pour le formateur, **briefings à remettre** (une page par victime, témoin et pour les secouristes) et **liste de matériel** de tous les scénarios prévus.
- Contenu modifiable dans `tools/scenarios_pse1.py` et `tools/scenarios_pse2.py`, puis `python3 tools/scenarios.py`.

## Version 2.5 : PIC F, PAE FPSE, Chef d'équipe
- L'application s'appelle désormais **Eval** (l'APK devient `Eval.apk` ; la mise à jour s'installe par-dessus la 2.4 et garde les données).
- **PIC F** (4 jours, 28 h) : les 11 fiches d'évaluation du référentiel (étude de cas, travail de groupe…), cotées A / B, sur le fond d'origine. La **fiche de suivi** se remplit seule : pour chaque jour, la note la plus fréquente des fiches du jour (en cas d'égalité, la moins favorable). Chaque case peut être modifiée d'une touche. La capacité est validée dès qu'elle a été évaluée au moins une fois. Page 2 : points forts et axes d'amélioration par journée, puis observations.
- **PAE FPSE** (6 jours, 49 h) : les fiches d'évaluation du référentiel cotées A / B / C / NO, la fiche de suivi sur 6 jours, la note finale et l'**avis final de l'équipe pédagogique** (évaluateurs, validations OUI/NON, aptitude, lieu et date). Les compétences 1 à 4.2 demandent A ou B, et 5.1 à 6.2 demandent A. Une case « titulaire du PAE FPSC » valide d'office 1, 2.1, 2.2, 5.1 et 5.2. Le NON reste une décision du jury : l'application ne l'impose jamais d'elle-même.
- **Chef d'équipe** (3 jours) : fiche d'évaluation formative (C1, C2, C4, C7, C8 avec les 4 types de bilan) et fiche de certification individuelle (2 passages minimum, niveaux 2B / 2B / 1A / 2B / 2B, QCM sur 40 avec 24 minimum, sans rattrapage).
- **Procès-verbaux** de formation PIC F, PAE FPSE (formation initiale et continue) et Chef d'équipe, sur le fond d'origine.
- Tous ces documents se trouvent dans le dossier du participant, dans l'export à la carte et dans l'export de session.

## Version 2.4
- **Journées de formation** J1… avec date et heures : PSE1 5 × 7 h = 35 h, PSE2 4 × 7 h = 28 h, formation continue 1 × 7 h. Elles peuvent être réparties sur plusieurs semaines (Modifier la formation › Journées). La présence se pointe par journée, avec le total d'heures ; la feuille de présence reste ouverte pendant le pointage. La ligne « Tous les participants » (et le bouton « Présence du jour » quand une journée tombe aujourd’hui) pointe (ou retire) une journée pour tout le groupe en un geste.
- **Fiches de technicité** (bouton dans la formation) : liste déroulante pour passer d'un participant à l'autre, ou mode « Tous les participants » pour cocher une technique, ou une rubrique entière, pour tout le groupe en une fois.
- **Évaluation théorique** : la note /20 se saisit dans la formation (tableau du groupe), sur la fiche du participant ou sur la certification. OUI / NON reste modifiable à la main : la décision du formateur prime sur le calcul, par exemple après un entretien de rattrapage.

## Format d'origine des PDF (version 2.3)
Les fiches exportées utilisent comme fond **la page des fichiers d'origine** (dossier `modeles/`), et les données sont placées dans les cases mesurées au dixième de millimètre :
- fiches formatives PSE1 et PSE2 (2 apprenants par page ; au-delà, page suivante avec « APPRENANT N°3 »…) ;
- fiches de technicité PSE1 et PSE2 ;
- fiche de certification individuelle PSE1 ;
- procès-verbaux de formation FI / FC, PSE1 / PSE2 (10 participants par page ; au-delà, page suivante numérotée).

Les fonds sont régénérés avec `python3 tools/forms.py` et les mesures sont faites avec `tools/geom.py` et `tools/grid.py`.
Une grille modifiée ou ajoutée, ou l'option « habiletés complémentaires », bascule automatiquement sur la version redessinée, puisque le modèle papier n'a pas ces lignes.
La fiche de certification PSE2 reste redessinée : seul un exemplaire à 96 dpi, trop flou, est disponible dans le référentiel.

## Fin de formation (version 2.2)
- **Procès-verbal de l'équipe pédagogique** : n° et date à saisir dans « Modifier la formation ». Il contient la liste des participants APTE / INAPTE et des cases de signature.
- **Certificats de compétences** PSE1 / PSE2 (texte des annexes 7 et 8) : ils sont réservés aux participants APTE. Le bouton « Numéroter les certificats » attribue des numéros à la suite (Réglages › Organisme).
- **Notification d'évaluation défavorable** pour les participants INAPTE. Le texte « formation initiale » a été corrigé, car le modèle des référentiels reprenait celui de la formation continue. Les deux textes sont modifiables dans Réglages.
- **Formation continue** : type de session FI/FC. En FC, chaque fiche formative propose une auto-évaluation par apprenant, reportée dans la case Observations du PDF. Les APTE reçoivent une attestation de formation continue (annexe 9), les autres une notification FC (annexe 10).
- **Questionnaire de satisfaction** (annexe 11) : la tablette passe en « mode stagiaire » anonyme, avec 8 critères notés de 1 à 4 et une justification obligatoire pour toute note ≤ 2. La synthèse PDF contient la cible, les moyennes et les commentaires.
- **QCM** : les corrigés des référentiels PSE1 et PSE2 (40 questions) sont intégrés. On corrige question par question (Juste / Faux, ou en cochant les réponses du stagiaire), et la note /20 est reportée sur la ligne D. Le questionnaire corrigé s'ajoute au dossier.
- **Habiletés complémentaires** (Réglages) : surveille la victime, utilise le matériel, tient sa place dans l'équipe, plusieurs victimes. Désactivées, les fiches restent strictement au format d'origine.
- **État civil** (civilité, date et lieu de naissance) : à saisir sur la fiche du participant, pour les certificats.

| Cas concret PSE1 | Compétence | Cas concret PSE2 | Compétence |
|---|---|---|---|
| C1 Comportement adapté | 1 | C1 Prise en charge | 1 |
| C2 Sécurité | 2 | C2 Immobilisation / relevage / brancardage | 2 |
| C3 Bilan (+ 4 regards) | 3 | C3 Coordination | 3 |
| C4 Gestes de premiers secours | 4 | C4 Conduite à tenir | 4 |
| C5 Rend compte au chef d'équipe | 5 | C5 Sécurité | 5 |
| C6 Conduite à tenir / communication | 6 | C6 Bilan / rend compte | 6 |
| | | C7 Comportement | 7 |

## Lien à ouvrir sur les téléphones
**https://forma-st.github.io/UDPS28-eval/**

## Installer sur Android
Copier `Eval.apk` sur la tablette, l'ouvrir, puis autoriser « Installer des applis inconnues ». La version 2.0 remplace la 1.0.
**Attention** : les données de la 1.0 (simple démonstration) ne sont pas reprises.

## iPhone / iPad
Ouvrir **https://forma-st.github.io/UDPS28-eval/** dans Safari, puis « Ouvrir l'application » et Partager › « Sur l'écran d'accueil ».

## Modifier l'application
- Code : `src/app.html`. Logo et icônes : `brand/`.
- `python3 build.py` régénère `docs/app/` (site GitHub Pages, publié à chaque push sur `main`) et `fichier-unique.html`.
- Après une nouvelle compilation, copier l'APK dans `docs/Eval.apk`.
- APK : `cd mobile && npx cap sync android && cd android && ./gradlew assembleDebug` (SDK Android requis). La clé de signature (`debug.keystore`, envoyée à part et volontairement absente du dépôt public) se place dans `~/.android/` : la garder pour que les mises à jour s'installent par-dessus.
