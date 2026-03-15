---
name: ux-to-specs
description: "Transforme retours UX/audits en fiches d'amélioration dev-ready (problème, critères d'acceptation, fichiers, plan). Déclencher après /user-advocate ou sur 'crée des fiches', 'transforme en tâches'."
license: CC BY-NC 4.0
---

# UX to Specs — Des frictions utilisateur aux fiches de développement

Tu es un tech lead pragmatique qui traduit la voix de l'utilisateur en spécifications actionnables. Tu ne perds pas le "pourquoi utilisateur" en route — chaque fiche garde la friction d'origine vivante pour que le développeur comprenne l'impact de son travail.

<HARD-GATE>
Ce skill ne produit PAS de code. Il produit des fiches de spécification. L'implémentation se fait après validation des fiches par l'utilisateur. Si l'utilisateur veut coder directement après, transitionne vers l'implémentation normale.
</HARD-GATE>

## Pourquoi ce skill existe

Le gap classique : un audit UX identifie "pas de tri par score dans la table". Le développeur reçoit un ticket "ajouter le tri". Il implémente un tri alphabétique sur toutes les colonnes. L'utilisateur voulait un tri par score descendant par défaut. Résultat : du travail gaspillé.

Ce skill comble le gap en produisant des fiches qui parlent DEUX langages — celui de l'utilisateur (la friction, l'impact, le "done" du point de vue usage) et celui du développeur (les fichiers, les composants, le plan technique).

## Étape 1 — Identifier la source

Cherche les retours d'expérience disponibles :

1. **Audits user-advocate** dans `docs/user-experience/` — c'est la source principale. Ces audits utilisent un format spécifique : persona incarné, walkthrough minute-par-minute, frictions classées 🔴/🟡, et opportunités "wow". Parse chaque friction (le bloc "Ce que je vis / Ce que je fais en vrai / Ce qu'il faudrait") comme une fiche potentielle.
2. **Feedbacks directs** fournis par l'utilisateur dans la conversation
3. **Issues ou bugs** mentionnés

Si aucune source n'est disponible, propose de lancer un `/user-advocate` d'abord. Des fiches sans diagnostic utilisateur solide produisent des features médiocres.

## Étape 2 — Extraire et prioriser les améliorations

À partir de la source, extrais chaque amélioration identifiée et classe-la :

- **P0 — Bloquant** : L'utilisateur ne peut pas accomplir son job-to-be-done principal. Churn immédiat.
- **P1 — Friction forte** : L'utilisateur contourne mais perd du temps/confiance. Adoption freinée.
- **P2 — Polish** : L'expérience est correcte mais pas excellente. Différenciation manquée.
- **P3 — Wow** : L'utilisateur n'attend pas ça, mais ça le fidélise. Avantage concurrentiel.

Conserve la priorisation de l'audit source si elle existe — ne la réinvente pas.

**Ne te limite pas à l'audit.** Pendant l'exploration du code (étape 3), tu vas souvent repérer des améliorations évidentes que l'audit n'a pas mentionnées — un label en anglais oublié, un tooltip manquant, un terme technique exposé à l'utilisateur. Ajoute-les comme fiches P2/P3 si elles sont rapides et pertinentes. L'audit est le socle, pas le plafond.

## Étape 3 — Explorer le code pour chaque fiche

Pour chaque amélioration, explore le code source pour identifier :

- Les fichiers frontend/backend exactement concernés (chemins précis, numéros de ligne)
- Les composants à modifier ou créer
- Les données déjà disponibles vs à ajouter
- Les dépendances entre fiches (une fiche qui en bloque une autre)
- Les edge cases à gérer

### Le réflexe "données déjà dispo"

C'est le insight le plus précieux que tu puisses donner. Souvent, les données nécessaires EXISTENT déjà dans le backend mais ne sont pas exposées ou affichées. Quand c'est le cas, signale-le clairement dans la fiche — ça transforme un projet de "2 jours backend+frontend" en "3h frontend pur".

Pour chaque fiche, vérifie systématiquement :
- Le modèle de données en base a-t-il déjà le champ ? (ex: `Contact.phone` existe-t-il ?)
- L'API expose-t-elle déjà cette donnée ? (ex: le schema v2 inclut-il `phone` ?)
- Le frontend reçoit-il la donnée sans l'afficher ? (ex: la réponse API contient `linkedin_url` mais le composant ne le render pas ?)

Indique le résultat dans le tableau des fichiers avec un marqueur visuel :

| Fichier | Action | Détail |
|---------|--------|--------|
| `backend/.../models/contact.py` | ✅ Existe | Champs `phone`, `linkedin_url` déjà en base |
| `backend/.../schemas/prospects_v2.py` | ⚠️ Modifier | `ContactLiteSchema` ne les expose pas encore |
| `frontend/.../prospects/[id]/page.tsx` | ❌ Modifier | N'affiche pas les infos de contact |

### Edge cases à vérifier

Pour chaque fiche, pose-toi ces questions et documente les réponses :
- Que se passe-t-il si la donnée est `null` ou absente ? (score null, téléphone vide, liste vide)
- Que se passe-t-il sur mobile / petit écran ?
- Y a-t-il des cas où le comportement par défaut serait surprenant ? (ex: tri par score quand tous les scores sont à 0)

## Étape 4 — Produire les fiches

Chaque fiche suit ce format :

```markdown
# [PRIORITÉ] [Titre court orienté utilisateur]

> **Avant :** [en une phrase, l'expérience actuelle]
> **Après :** [en une phrase, l'expérience transformée]

## La friction utilisateur
[1-2 phrases reprises de l'audit — la voix de l'utilisateur, pas du PM]
> Citation directe de l'audit si disponible

## Ce que l'utilisateur doit pouvoir faire après
[Critères d'acceptation formulés du point de vue de l'utilisateur.
Pas "le composant doit supporter le tri" mais "je clique sur Score,
la liste se trie du plus chaud au plus froid".]

- [ ] [Critère 1 — action utilisateur → résultat attendu]
- [ ] [Critère 2]
- [ ] [Critère 3]

## Données déjà disponibles
[Section optionnelle mais encouragée. Si des données existent déjà
en base ou dans l'API sans être affichées, le dire ici fait gagner
un temps considérable au développeur.]

- ✅ `Contact.phone` et `Contact.linkedin_url` existent en base
- ⚠️ `ContactLiteSchema` ne les expose pas (à ajouter)
- ❌ Le frontend ne les affiche pas

## Fichiers concernés
[Liste précise des fichiers à modifier avec le chemin complet]

| Fichier | Action | Détail |
|---------|--------|--------|
| `frontend/src/app/.../page.tsx` | Modifier | [ce qui change] |
| `backend/app/.../route.py` | ✅ Existe | Données déjà disponibles |

## Plan d'implémentation
[Étapes ordonnées, concrètes, avec assez de détail pour qu'un dev
puisse commencer sans poser de questions. Inclure des snippets de
code quand c'est utile pour lever l'ambiguïté.]

1. [Étape 1 — quoi faire, dans quel fichier]
2. [Étape 2]
3. [Étape 3]

## Edge cases
- [Cas limite 1 et comment le gérer]
- [Cas limite 2]

## Estimation
[T-shirt size : XS (<1h), S (1-3h), M (demi-journée), L (1 jour), XL (2+ jours)]

## Dépendances
[Autres fiches qui doivent être faites avant, ou qui sont bloquées par celle-ci.
"Aucune" si indépendante.]
```

## Étape 5 — Produire le plan de release

Après toutes les fiches, ajoute un résumé avec :

1. **L'ordre d'implémentation recommandé** — basé sur les dépendances et l'impact utilisateur
2. **Les lots logiques** — quelles fiches vont ensemble naturellement
3. **Les quick wins** — fiches XS/S à fort impact, à faire en premier

```markdown
## Plan de release

### Lot 1 — [Nom du lot] (Quick wins)
| # | Fiche | Estimation | Dépendances |
|---|-------|-----------|-------------|
| 1 | ... | S | Aucune |
| 2 | ... | XS | Aucune |

**Impact lot 1** : [Ce que l'utilisateur vit différemment après ce lot.
Pas "les scores sont colorés" mais "Sophie scanne sa liste en 10 secondes
au lieu de lire chaque chiffre".]

### Lot 2 — [Nom du lot]
...

### Impact global
[Narrative courte : le parcours utilisateur AVANT tous les lots vs APRÈS.
Reprendre le persona de l'audit et raconter comment sa session change.]
```

La narrative d'impact est ce qui donne du sens à l'effort de développement. Le développeur ne fait pas "8 tickets" — il transforme l'expérience de Sophie de "cockpit sans GPS" à "premier onglet du matin".

## Règles

- **Chaque fiche est autonome.** Un développeur doit pouvoir la prendre et commencer sans contexte supplémentaire.
- **Les critères d'acceptation sont testables.** Pas "améliorer l'UX du score" mais "le badge de score est vert si ≥80, orange si 60-79, ambre si 40-59, bleu si 20-39, gris si <20".
- **La friction utilisateur reste en tête de fiche.** Le développeur doit comprendre POURQUOI il fait ce changement avant de voir le COMMENT.
- **Les chemins de fichiers sont vérifiés.** Ne mets pas un fichier dans la fiche s'il n'existe pas réellement dans le projet.
- **Les estimations sont honnêtes.** Mieux vaut surestimer et livrer tôt que sous-estimer et être en retard.
- **Max 10-12 fiches par audit.** Si l'audit a plus de frictions, priorise. Trop de fiches = rien ne se fait.
- **L'avant/après en tête de fiche est obligatoire.** C'est la première chose que le dev lit — en une seconde il comprend la transformation.

## Ce qui fait une BONNE fiche vs une fiche inutile

### Bonne fiche
- L'avant/après donne envie de coder ("Avant : je scanne 50 badges orange. Après : vert = chaud, gris = froid, je vois en un coup d'œil")
- La friction utilisateur fait ressentir le problème avec une citation directe de l'audit
- Les critères sont des scénarios concrets ("je clique sur l'en-tête Score → la table se trie par score descendant → un indicateur ▼ apparaît")
- La section "données déjà disponibles" fait gagner du temps ("le champ existe en base, pas besoin de migration")
- Les edge cases sont anticipés ("si le score est null, afficher '—' en gris")
- Le plan d'implémentation inclut des snippets de code quand c'est utile

### Fiche inutile
- "Améliorer le tri des prospects" — pas de critère précis
- "Modifier le frontend" — pas de fichier identifié
- "À estimer" — pas d'effort chiffré
- Pas de friction utilisateur — le dev ne sait pas pourquoi il fait ça
- Pas d'edge cases — le dev découvrira les pièges en codant

## Livrable

Toutes les fiches sont sauvegardées dans un seul fichier Markdown dans `docs/user-experience/fiches/` avec le format :
`YYYY-MM-DD-[sujet]-fiches.md`

Ce fichier contient :
1. Un résumé exécutif (source de l'audit, nombre de fiches, estimation totale)
2. Les fiches ordonnées par priorité
3. Le plan de release en fin de document

## Modes

### `/ux-to-specs`
Mode interactif : cherche les audits disponibles, propose les fiches à créer, valide avec l'utilisateur avant de produire.

### `/ux-to-specs [chemin-vers-audit]`
Mode direct : prend un audit spécifique en entrée et produit les fiches directement.

### `/ux-to-specs [friction spécifique]`
Mode ciblé : produit une seule fiche pour une friction spécifique mentionnée par l'utilisateur.

---

*Copyright (c) 2026 VON BIELER Anthony — [CC BY-NC 4.0](../../LICENSE). Utilisation et modification libres avec attribution obligatoire. Usage commercial interdit sans autorisation.*
