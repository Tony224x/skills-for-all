# Contribuer

Merci de l'intérêt. Ce dépôt rassemble des skills Claude Code réutilisables ; la barre n'est pas la
quantité mais la **réutilisabilité par quelqu'un d'autre que son auteur**.

## Ajouter un skill

1. **Créer le dossier** dans la catégorie existante (`book/`, `UX/`) ou proposer une nouvelle
   catégorie en majuscules si aucun ne correspond.
2. **Écrire `SKILL.md`** avec le frontmatter minimal :

   ```yaml
   ---
   name: nom-du-skill              # identique au nom du dossier, en kebab-case
   description: "Une phrase : ce que le skill fait ET quand il doit se déclencher."
   license: MIT
   ---
   ```

   La `description` est le seul texte que le modèle lit avant de charger le skill : elle doit dire
   le **déclencheur** (« Déclencher pour… », « sur 'mets-toi à la place de…' »), pas seulement le sujet.

3. **Séparer ce qui se charge** : les instructions dans `SKILL.md`, les scripts dans `scripts/`,
   les documents longs dans `references/` (lus à la demande). Un `SKILL.md` reste lisible d'un trait ;
   au-delà, c'est du matériau de référence, pas de la consigne.
4. **Rendre les scripts exécutables** et sans dépendance exotique : `python3` + bibliothèque standard
   quand c'est possible, dépendances déclarées en tête de fichier sinon.
5. **Mettre à jour le README** (tableau des skills disponibles) et, si nécessaire, `book/README.md`.

## Checklist avant d'ouvrir une PR

- [ ] `SKILL.md` présent, frontmatter `name` + `description` complets
- [ ] `name` identique au dossier
- [ ] description qui dit **quand** déclencher le skill, pas seulement ce qu'il fait
- [ ] scripts testés au moins une fois sur un cas réel, résultat reproduit dans la PR
- [ ] aucun secret, aucune donnée personnelle, aucun chemin absolu propre à votre machine
- [ ] README à jour
- [ ] pas de contenu copié d'un skill tiers sans attribution explicite

## Style

- Français pour les instructions, anglais dans le code si c'est la convention du fichier
- Impératif direct, pas de remplissage : un skill qui dit « sois rigoureux » n'apprend rien
- Décrire le **comment décider**, pas seulement la procédure heureuse

## Licence des contributions

Toute contribution est publiée sous [MIT](LICENSE), comme le reste du dépôt : réutilisation libre,
y compris commerciale, notice de copyright conservée.
