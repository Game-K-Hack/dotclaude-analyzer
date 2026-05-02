# Inspecteur Claude

Interface graphique (style assistant / wizard, inspiree de `bkcrack-gui-master`)
pour inspecter le dossier `.claude` de Claude Code et exporter le contenu d'un
projet a une date donnee.

## Lancement

```
pip install -r requirements.txt
python main.py
```

## Pages

1. **Bienvenue** : presentation de l'outil.
2. **Source** : detection automatique du dossier `.claude` ou choix manuel.
   Le diagnostic affiche le nombre de projets et de sessions trouves.
3. **Parametres / Connexion** : aper&ccedil;u de `settings.json`,
   `settings.local.json` et resume non-sensible de `.credentials.json`
   (taille, date de modification, expiration eventuelle, liste des cles
   sans afficher les valeurs sensibles).
4. **Projets** : liste des projets, des sessions, et rendu de la
   conversation (messages utilisateur / assistant).
5. **Fichiers** : liste des fichiers crees / modifies dans la session
   selectionnee, avec une **barre de date** permettant de remonter
   le temps. Bouton d'**export** vers un dossier ou une archive ZIP.
6. **Fin** : ecran de cloture.

## Reconstruction des fichiers

A partir des evenements `tool_use` du fichier `.jsonl` de la session :

- `Write` : la version complete est connue, on l'utilise telle quelle.
- `Edit` / `MultiEdit` : applique sequentiellement les patches
  `old_string` -> `new_string` sur la base courante. Si la base n'est
  pas connue (premier evenement etait un Edit), on tente de lire le
  fichier sur le disque ; sinon il est marque "[Edits seulement]" et
  ignore a l'export.
- `NotebookEdit` : note mais non reconstruit.

L'export remappe les chemins absolus en chemins relatifs portables
(suppression de la lettre de lecteur Windows).
