# Skills for All

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-4-blue.svg)](#skills-disponibles)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skills-d97757.svg)](https://docs.anthropic.com/en/docs/claude-code)

Une collection de skills [Claude Code](https://docs.anthropic.com/en/docs/claude-code) conçus pour être partagés et réutilisés.

## Skills disponibles

### Book — Édition & lecture littéraire

| Skill | Description |
|-------|-------------|
| [book-review](book/book-review/) | Relecture experte de manuscrits : correction linguistique, analyse stylistique, notation, et production de DOCX corrigés avec mise en page préservée. |
| [beta-reader](book/beta-reader/) | Bêta-lecture immersive par panel de personas (lecteur-cible, critique, éditeur, grand public). Évaluation chapitre par chapitre avec notation croisée. |

### UX — Audit & expérience utilisateur

| Skill | Description |
|-------|-------------|
| [user-advocate](UX/user-advocate/) | Audit UX brutal et constructif du point de vue utilisateur final. Simule une session réelle, produit un diagnostic vécu avec frictions et améliorations concrètes. |
| [ux-to-specs](UX/ux-to-specs/) | Transforme retours UX et audits en fiches d'amélioration dev-ready avec critères d'acceptation, fichiers concernés et plan d'implémentation. |

## Installation

### 1. Copier le skill dans votre répertoire Claude Code

```bash
# Cloner le repo
git clone https://github.com/Tony224x/skills-for-all.git

# Copier un skill dans votre config Claude Code
cp -r skills-for-all/book/book-review ~/.claude/skills/book-review
cp -r skills-for-all/book/beta-reader ~/.claude/skills/beta-reader

# Les skills UX s'installent de la même façon
cp -r skills-for-all/UX/user-advocate ~/.claude/skills/user-advocate
cp -r skills-for-all/UX/ux-to-specs ~/.claude/skills/ux-to-specs
```

### 2. Vérifier l'installation

Les skills sont détectés automatiquement par Claude Code au prochain lancement. Pour vérifier :

```
/skills
```

## Structure du repo

```
skills-for-all/
  book/                        # Skills d'édition littéraire
    book-review/               #   Relecture & correction de manuscrits
    beta-reader/               #   Bêta-lecture par personas
  UX/                          # Skills d'audit UX
    user-advocate/             #   Audit UX vécu par persona
    ux-to-specs/               #   Frictions UX → fiches dev-ready
```

Chaque skill suit la même anatomie : un `SKILL.md` (frontmatter `name` + `description`, puis les
instructions), des `scripts/` exécutables quand le skill produit des fichiers, et des `references/`
chargées à la demande plutôt que noyées dans le prompt.

## Contribuer

Les contributions sont bienvenues — voir [CONTRIBUTING.md](CONTRIBUTING.md) pour le format exact
attendu et la checklist avant d'ouvrir une PR.

## Licence

[MIT](LICENSE) — Copyright (c) 2026 VON BIELER Anthony
