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

## Correspondance cas concret → compétence de certification (modifiable dans Grilles)
| PSE1 formative | Compétence certif. PSE1 |
|---|---|
| C1 Comportement adapté | 6 Adapter son comportement |
| C2 Sécurité de l'intervention | 2 Protection immédiate |
| C3 Bilan conforme (+ 4 regards) | 3 Bilan et transmission |
| C4 Gestes de premiers secours | 4 Gestes de premiers secours |
| C5 Rend compte au chef d'équipe | 3 Bilan et transmission |
| C6 Conduite à tenir appropriée | 1 Cadre juridique |
| C6 Communication au sein de l'équipe | 5 Assister des équipiers |

PSE2 : C1 → 1, C2 → 2, C3 → 3, C4 → 4, C5 → 5, C6 → 6, C7 → 7 (même numérotation sur les deux fiches).

## Lien à ouvrir sur les téléphones
**https://forma-st.github.io/udps28-eval/**

## Installer sur Android
Copier `Eval-PSE.apk` sur la tablette, l'ouvrir, puis autoriser « Installer des applis inconnues ». La version 2.0 remplace la 1.0.
**Attention** : les données de la 1.0 (simple démonstration) ne sont pas reprises.

## iPhone / iPad
Ouvrir **https://forma-st.github.io/udps28-eval/** dans Safari, puis « Ouvrir l'application » et Partager › « Sur l'écran d'accueil ».

## Modifier l'application
- Code : `src/app.html`. Logo et icônes : `brand/`.
- `python3 build.py` régénère `docs/app/` (site GitHub Pages, publié à chaque push sur `main`) et `fichier-unique.html`.
- Après une nouvelle compilation, copier l'APK dans `docs/Eval-PSE.apk`.
- APK : `cd mobile && npx cap sync android && cd android && ./gradlew assembleDebug` (SDK Android requis). La clé de signature (`debug.keystore`, envoyée à part et volontairement absente du dépôt public) se place dans `~/.android/` : la garder pour que les mises à jour s'installent par-dessus.
