# Trail 2027 · coach

Hub d'entraînement trail de Romain : plan de novembre 2026 à septembre 2027 vers le
Trail des Forts (8 mai 2027, 72 km, 2800 m D+) et le Wildstrubel (10 septembre 2027, Wild 110).
Application web statique pour GitHub Pages : fonctionne hors ligne une fois ouverte et
s'ajoute à l'écran d'accueil de l'iPhone (Partager → Sur l'écran d'accueil).

## Fichiers

- `index.html` : l'app (mise en page, styles, logique). Aucune étape de build, aucune dépendance.
- `data.js` : **tout le contenu du plan** (semaines, phases, exercices, modèles de renfo).
- `sync.js` : synchronisation du journal entre appareils via ce dépôt.
- `sw.js` : hors ligne (réseau d'abord, copie enregistrée sinon).
- `manifest.webmanifest`, `icons/` : réglages de l'app sur l'écran d'accueil.

## Journal (branche `journal`, fichier `journal.json`)

Les séances cochées et le renfo sont enregistrés dans `journal.json` sur la branche `journal`
(la branche `main` ne contient que l'app, pour ne pas relancer Pages à chaque séance).
Clé GitHub requise dans l'app : fine-grained token limité à ce dépôt, permission
**Contents : Read and write**. Sans clé, tout reste dans le navigateur (sauvegarde fichier possible).

Format :

```json
{
  "v": 1,
  "done":  { "w12k0": { "v": true, "t": 1767000000000 } },
  "renfo": { "r…": { "id": "r…", "date": "2026-11-17", "tpl": "A", "name": "Renfo A : force lourde",
                     "rpe": 7, "note": "", "t": 1767000000000,
                     "items": [ { "ex": "fb", "sets": [ { "r": 6, "kg": 14 } ] } ] } },
  "notes": {}
}
```

`done` : clé `w<semaine>k<index de la séance clé>`. `renfo` : `ex` renvoie à `EXOS` dans `data.js`
(sinon `name` et `unit` libres), `r` = répétitions (ou secondes si l'exercice est en secondes),
`kg` = charge. Une séance supprimée devient `{ "id", "del": true, "t" }`. Fusion par élément,
le plus récent (`t`) gagne.

## Modifier le plan

Éditer `PLAN.weeks` dans `data.js` (une entrée par semaine : `phase`, `h` heures, `dp` D+,
`keys` séances clés, `note`), puis mettre à jour `PLAN.updated` et le nom du cache dans `sw.js`.

### Collections ajoutées

- `tpls` : presets personnels `{id, name, mini, items:[{ex, sets:[{r,kg}]}], t}`.
- `runs` : sorties écrites par Claude à partir des FIT `{id, date, title, min, km, dp, hr, gap, ef, note, t}`. Claude coche aussi la séance clé correspondante dans `done` (`w{n}k{i}`).
- `renfo[].mini` : séance d'entretien, hors décompte des 2 séances par semaine.
