"""
Extrait les chapitres d'un DOCX sous forme de fichiers texte Markdown.

Usage:
  python3 extract_chapters_text.py <source_docx> <output_dir>

Détecte les chapitres via les titres (styles Heading ou texte commençant par
"Chapitre", "Avant-propos", "Prologue", "Épilogue", "Partie").
Produit un fichier par chapitre : chapitre-01.md, chapitre-02.md, etc.
Produit aussi chapters_index.json avec la liste des chapitres et métadonnées.
"""
import sys
import os
import json
import zipfile
import xml.etree.ElementTree as ET
import re


def extract_text_from_docx(docx_path):
    """Extrait tous les paragraphes avec leur style et texte."""
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')

    root = ET.fromstring(xml_content)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = root.findall('.//w:body/w:p', ns)

    result = []
    for i, p in enumerate(paragraphs):
        # Récupérer le style
        style = None
        pPr = p.find('w:pPr', ns)
        if pPr is not None:
            pStyle = pPr.find('w:pStyle', ns)
            if pStyle is not None:
                style = pStyle.get(f'{{{ns["w"]}}}val', '')

        # Récupérer le texte
        texts = []
        for t in p.findall('.//w:t', ns):
            if t.text:
                texts.append(t.text)
        text = ''.join(texts)

        # Détecter gras/italique au niveau du run
        is_bold = False
        is_italic = False
        for r in p.findall('w:r', ns):
            rPr = r.find('w:rPr', ns)
            if rPr is not None:
                if rPr.find('w:b', ns) is not None:
                    is_bold = True
                if rPr.find('w:i', ns) is not None:
                    is_italic = True

        result.append({
            'index': i,
            'text': text,
            'style': style,
            'is_bold': is_bold,
            'is_italic': is_italic,
        })

    return result


def detect_chapter_boundaries(paragraphs):
    """Détecte les limites des chapitres."""
    chapter_patterns = [
        r'^chapitre\s+\d+',
        r'^chapitre\s+[ivxlcdm]+',
        r'^avant[\s-]propos',
        r'^prologue',
        r'^[ée]pilogue',
        r'^partie\s+\d+',
        r'^partie\s+[ivxlcdm]+',
        r'^pr[ée]face',
        r'^introduction',
        r'^conclusion',
        r'^annexe',
        r'^postface',
    ]

    heading_styles = ['Heading1', 'Heading2', 'Titre', 'Titre1', 'Titre2',
                      'Title', 'heading1', 'heading2']

    chapters = []
    for p in paragraphs:
        text = p['text'].strip()
        if not text:
            continue

        is_chapter = False

        # Vérifier par style
        if p['style'] and any(h.lower() in p['style'].lower() for h in heading_styles):
            is_chapter = True

        # Vérifier par motif de texte
        for pattern in chapter_patterns:
            if re.match(pattern, text.lower()):
                is_chapter = True
                break

        if is_chapter:
            chapters.append({
                'index': p['index'],
                'title': text,
            })

    return chapters


def paragraphs_to_markdown(paragraphs):
    """Convertit une liste de paragraphes en texte Markdown."""
    lines = []
    for p in paragraphs:
        text = p['text']
        if not text.strip():
            lines.append('')
            continue

        # Dialogues (tirets)
        if text.strip().startswith(('—', '–', '- ')):
            lines.append(text)
        # Texte en italique seul
        elif p.get('is_italic') and not p.get('is_bold'):
            lines.append(f'*{text}*')
        else:
            lines.append(text)

    return '\n\n'.join(lines)


def extract_chapters(docx_path, output_dir):
    """Extrait tous les chapitres en fichiers Markdown séparés."""
    os.makedirs(output_dir, exist_ok=True)

    paragraphs = extract_text_from_docx(docx_path)
    chapters = detect_chapter_boundaries(paragraphs)

    if not chapters:
        # Pas de chapitres détectés : tout mettre dans un seul fichier
        print("Aucun chapitre détecté. Export du texte complet.")
        md_text = paragraphs_to_markdown(paragraphs)
        out_path = os.path.join(output_dir, 'texte-complet.md')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_text)

        index = [{
            'file': 'texte-complet.md',
            'title': 'Texte complet',
            'start_para': 0,
            'end_para': len(paragraphs),
            'word_count': sum(len(p['text'].split()) for p in paragraphs),
        }]
        with open(os.path.join(output_dir, 'chapters_index.json'), 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        print(f"  -> {out_path}")
        return

    # Ajouter le contenu avant le premier chapitre comme "préambule" s'il y en a
    index = []
    chapter_ranges = []

    first_chapter_idx = chapters[0]['index']
    pre_content = [p for p in paragraphs if p['index'] < first_chapter_idx and p['text'].strip()]
    if pre_content:
        chapter_ranges.append({
            'title': 'Préambule',
            'start': 0,
            'end': first_chapter_idx,
        })

    for i, ch in enumerate(chapters):
        end = chapters[i + 1]['index'] if i + 1 < len(chapters) else len(paragraphs)
        chapter_ranges.append({
            'title': ch['title'],
            'start': ch['index'],
            'end': end,
        })

    for i, ch_range in enumerate(chapter_ranges):
        chapter_paras = [p for p in paragraphs
                         if ch_range['start'] <= p['index'] < ch_range['end']]

        md_text = f"# {ch_range['title']}\n\n"
        md_text += paragraphs_to_markdown(chapter_paras[1:] if chapter_paras else [])

        filename = f'chapitre-{i:02d}.md'
        out_path = os.path.join(output_dir, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_text)

        word_count = sum(len(p['text'].split()) for p in chapter_paras)
        entry = {
            'file': filename,
            'title': ch_range['title'],
            'chapter_number': i,
            'start_para': ch_range['start'],
            'end_para': ch_range['end'],
            'word_count': word_count,
        }
        index.append(entry)
        print(f"  -> {filename}: {ch_range['title']} ({word_count} mots)")

    # Sauvegarder l'index
    index_path = os.path.join(output_dir, 'chapters_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    total_words = sum(e['word_count'] for e in index)
    print(f"\n{len(index)} chapitres extraits, {total_words} mots au total.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 extract_chapters_text.py <source.docx> <output_dir>')
        sys.exit(1)

    extract_chapters(sys.argv[1], sys.argv[2])
