# Book — Skills d'edition litteraire

Skills dedies a l'accompagnement d'auteurs dans l'ecriture et la relecture de manuscrits.

## Skills disponibles

### book-review

Relecture experte de manuscrits avec un workflow chapitre par chapitre :
- Correction linguistique (orthographe, grammaire, temps verbaux, typographie)
- Analyse stylistique et avis litteraire
- Production de DOCX corriges avec mise en page intacte
- Notation sur 5 avec grille detaillee
- Suivi de coherence entre chapitres (personnages, histoire, style)

**Scripts inclus :**
- `extract_chapter.py` — Extrait un chapitre d'un DOCX en conservant la mise en page, avec application optionnelle de corrections
- `merge_chapters.py` — Fusionne plusieurs DOCX de chapitres en un seul document

### beta-reader

Beta-lecture immersive simulant un comite de lecture :
- 4 personas obligatoires : lecteur-cible, critique litteraire, editeur, grand public
- Personas supplementaires configurables
- Lecture sequentielle chapitre par chapitre (reactions a chaud)
- Notation sur 5 avec grilles detaillees par critere (8 criteres)
- Synthese croisee avec consensus, divergences, et priorites d'amelioration
- Parallelisation via subagents (un par persona)

**Script inclus :**
- `extract_chapters_text.py` — Extrait les chapitres d'un DOCX en fichiers Markdown separes

## Complementarite

Les deux skills sont distincts et complementaires :

| | book-review | beta-reader |
|---|---|---|
| **Focus** | Correction & qualite d'ecriture | Experience de lecture |
| **Angle** | Editeur/correcteur professionnel | Panel de lecteurs divers |
| **Sortie** | DOCX corriges + rapport | Avis par persona + synthese |
| **Notation** | Sur 5 (8 criteres techniques) | Sur 5 (8 criteres d'experience) |
| **Workflow** | Chapitre par chapitre, sequentiel | Chapitre par chapitre, parallelise |

**Usage typique :** `book-review` d'abord pour corriger le texte, puis `beta-reader` sur le manuscrit corrige pour evaluer l'experience de lecture.

## Prerequis

- Python 3.8+
- Aucune dependance externe (les scripts utilisent uniquement la bibliotheque standard Python)
