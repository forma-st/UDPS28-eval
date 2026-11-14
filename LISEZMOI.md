# Évaluations PSE · UDPS 28 (version 2.0)

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
