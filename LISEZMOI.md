# Évaluations PSE · UDPS 28 (version 2.4)

Application de terrain pour les formations PSE1 et PSE2. Elle fonctionne **entièrement sans réseau**.

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

## Version 2.4
- **Journées de formation** J1… avec date et heures : PSE1 5 × 7 h = 35 h, PSE2 4 × 7 h = 28 h, formation continue 1 × 7 h. Elles peuvent être réparties sur plusieurs semaines (Modifier la formation › Journées). La présence se pointe par journée, avec le total d'heures ; la feuille de présence reste ouverte pendant le pointage. La ligne « Tous les participants » pointe (ou retire) une journée pour tout le groupe en un geste.
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
Copier `Eval-PSE.apk` sur la tablette, l'ouvrir, puis autoriser « Installer des applis inconnues ». La version 2.0 remplace la 1.0.
**Attention** : les données de la 1.0 (simple démonstration) ne sont pas reprises.

## iPhone / iPad
Ouvrir **https://forma-st.github.io/UDPS28-eval/** dans Safari, puis « Ouvrir l'application » et Partager › « Sur l'écran d'accueil ».

## Modifier l'application
- Code : `src/app.html`. Logo et icônes : `brand/`.
- `python3 build.py` régénère `docs/app/` (site GitHub Pages, publié à chaque push sur `main`) et `fichier-unique.html`.
- Après une nouvelle compilation, copier l'APK dans `docs/Eval-PSE.apk`.
- APK : `cd mobile && npx cap sync android && cd android && ./gradlew assembleDebug` (SDK Android requis). La clé de signature (`debug.keystore`, envoyée à part et volontairement absente du dépôt public) se place dans `~/.android/` : la garder pour que les mises à jour s'installent par-dessus.
