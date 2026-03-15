# Skills for All

A collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills designed to be shared and reused.

## Available Skills

### Book — Edition & lecture litteraire

| Skill | Description |
|-------|-------------|
| [book-review](book/book-review/) | Relecture experte de manuscrits : correction linguistique, analyse stylistique, notation, et production de DOCX corriges avec mise en page preservee. |
| [beta-reader](book/beta-reader/) | Beta-lecture immersive par panel de personas (lecteur-cible, critique, editeur, grand public). Evaluation chapitre par chapitre avec notation croisee. |

### UX — Audit & experience utilisateur

| Skill | Description |
|-------|-------------|
| [user-advocate](UX/user-advocate/) | Audit UX brutal et constructif du point de vue utilisateur final. Simule une session reelle, produit un diagnostic vecu avec frictions et ameliorations concretes. |
| [ux-to-specs](UX/ux-to-specs/) | Transforme retours UX et audits en fiches d'amelioration dev-ready avec criteres d'acceptation, fichiers concernes et plan d'implementation. |

## Installation

### 1. Copier le skill dans votre repertoire Claude Code

```bash
# Cloner le repo
git clone https://github.com/Tony224x/skills-for-all.git

# Copier un skill dans votre config Claude Code
cp -r skills-for-all/book/book-review ~/.claude/skills/book-review
cp -r skills-for-all/book/beta-reader ~/.claude/skills/beta-reader
```

### 2. Verifier l'installation

Les skills seront automatiquement detectes par Claude Code au prochain lancement. Vous pouvez verifier avec :

```
/skills
```

## Structure du repo

```
skills-for-all/
  book/                        # Skills d'edition litteraire
    book-review/               #   Relecture & correction de manuscrits
    beta-reader/               #   Beta-lecture par personas
  UX/                          # Skills d'audit UX
    user-advocate/             #   Audit UX vecu par persona
    ux-to-specs/               #   Frictions UX → fiches dev-ready
```

## Contribuer

Les contributions sont les bienvenues. Pour ajouter un skill :

1. Creez un dossier dans la categorie appropriee (ou creez-en une nouvelle)
2. Ajoutez un `SKILL.md` avec le frontmatter requis (`name`, `description`)
3. Incluez les scripts et references necessaires
4. Mettez a jour ce README

## Licence

[CC BY-NC 4.0](LICENSE) — Copyright (c) 2026 VON BIELER Anthony
