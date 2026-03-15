"""
Extrait un chapitre d'un fichier DOCX en conservant la mise en page originale.

Usage: python3 extract_chapter.py <source_docx> <start_para> <end_para> <output_docx> [corrections_json]

- Copie tous les fichiers du DOCX source (styles, themes, polices, etc.)
- Ne garde que les paragraphes du chapitre (start_para inclus, end_para exclus)
- Si un fichier corrections_json est fourni, applique les corrections textuelles
  Format du JSON: {"index_paragraphe": "texte_corrige", ...}
  Les index sont relatifs au document complet (pas au chapitre)
"""
import sys
import os
import zipfile
import shutil
import json
import xml.etree.ElementTree as ET
import re


def extract_chapter(source_docx, start_para, end_para, output_docx, corrections=None):
    work_dir = output_docx + '_workdir'

    # Clean up any previous work
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir)

    # Extract source DOCX
    with zipfile.ZipFile(source_docx, 'r') as z:
        z.extractall(work_dir)

    # Read and register all namespaces from the raw XML
    doc_xml_path = os.path.join(work_dir, 'word', 'document.xml')
    with open(doc_xml_path, 'r', encoding='utf-8') as f:
        raw_xml = f.read()

    # Extract namespace declarations from root element
    ns_matches = re.findall(r'xmlns:?(\w*)=["\']([^"\']+)["\']', raw_xml)
    for prefix, uri in ns_matches:
        if prefix:
            ET.register_namespace(prefix, uri)
        else:
            ET.register_namespace('', uri)

    # Parse the document
    tree = ET.parse(doc_xml_path)
    root = tree.getroot()

    # Find the w namespace
    ns = {}
    for prefix, uri in ns_matches:
        if prefix:
            ns[prefix] = uri

    w_ns = ns.get('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')

    # Find body
    body = root.find(f'{{{w_ns}}}body')
    if body is None:
        print("ERROR: Could not find document body")
        sys.exit(1)

    # Get all children of body (paragraphs, tables, section properties, etc.)
    all_children = list(body)

    # Count paragraphs to identify which children to keep
    para_tag = f'{{{w_ns}}}p'
    tbl_tag = f'{{{w_ns}}}tbl'
    sect_tag = f'{{{w_ns}}}sectPr'

    # Build a map: for each child, track its paragraph index range
    children_to_keep = []
    children_to_remove = []
    sect_pr = None
    para_idx = 0

    for child in all_children:
        if child.tag == sect_tag:
            # Always keep section properties (page layout, margins, etc.)
            sect_pr = child
            continue

        if child.tag == para_tag:
            if start_para <= para_idx < end_para:
                children_to_keep.append((child, para_idx))
            else:
                children_to_remove.append(child)
            para_idx += 1
        elif child.tag == tbl_tag:
            # Tables: count their paragraphs but keep/remove as a unit
            table_paras = child.findall(f'.//{{{w_ns}}}p')
            table_start = para_idx
            table_end = para_idx + len(table_paras)
            if table_start >= start_para and table_end <= end_para:
                children_to_keep.append((child, table_start))
            else:
                children_to_remove.append(child)
            para_idx = table_end
        else:
            # Other elements: keep if between our range
            children_to_remove.append(child)

    # Remove children not in our chapter
    for child in children_to_remove:
        body.remove(child)

    # Apply text corrections if provided
    if corrections:
        for child, orig_idx in children_to_keep:
            str_idx = str(orig_idx)
            if str_idx in corrections:
                corrected_text = corrections[str_idx]
                if child.tag == para_tag:
                    apply_correction_to_paragraph(child, corrected_text, w_ns)

    # Make sure sectPr is at the end of body (required for valid DOCX)
    if sect_pr is not None:
        body.append(sect_pr)

    # Write modified document.xml
    tree.write(doc_xml_path, xml_declaration=True, encoding='UTF-8')

    # Repackage as DOCX
    if os.path.exists(output_docx):
        os.remove(output_docx)

    with zipfile.ZipFile(output_docx, 'w', zipfile.ZIP_DEFLATED) as zout:
        for dirpath, dirnames, filenames in os.walk(work_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                arcname = os.path.relpath(file_path, work_dir)
                zout.write(file_path, arcname)

    # Clean up
    shutil.rmtree(work_dir)
    print(f'Generated: {output_docx} (paragraphs {start_para}-{end_para-1})')


def apply_correction_to_paragraph(para, corrected_text, w_ns):
    """Replace the text content of a paragraph while preserving formatting.

    Only modifies the text (<w:t> elements), never the formatting (<w:rPr>, <w:pPr>).
    This ensures the original mise en page (fonts, sizes, styles, etc.) is untouched.
    """
    t_elements = para.findall(f'.//{{{w_ns}}}t')

    if not t_elements:
        return

    if len(t_elements) == 1:
        t_elements[0].text = corrected_text
        t_elements[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    else:
        # Multiple text runs: put all text in the first one, clear the rest
        t_elements[0].text = corrected_text
        t_elements[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        for t in t_elements[1:]:
            t.text = ''


def list_chapters(source_docx):
    """List chapters detected in the DOCX with their paragraph ranges."""
    with zipfile.ZipFile(source_docx) as z:
        xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = root.findall('.//w:body/w:p', ns)

    chapters = []
    for i, p in enumerate(paragraphs):
        texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
        text = ''.join(texts).strip()
        if text.lower().startswith('chapitre') or text.lower().startswith('avant-propos'):
            chapters.append((i, text))

    print(f'Total paragraphs: {len(paragraphs)}')
    print(f'Chapters detected:')
    for idx, title in chapters:
        print(f'  P{idx}: {title}')
    return chapters


def extract_text(source_docx, start_para, end_para):
    """Extract raw text from a range of paragraphs. Useful for building corrections."""
    with zipfile.ZipFile(source_docx) as z:
        xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = root.findall('.//w:body/w:p', ns)

    result = []
    for i in range(start_para, min(end_para, len(paragraphs))):
        p = paragraphs[i]
        texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
        text = ''.join(texts)
        is_dialogue = text.strip().startswith('—') or text.strip().startswith('–')
        result.append({'index': i, 'text': text, 'is_dialogue': is_dialogue})

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python3 extract_chapter.py list <source_docx>')
        print('  python3 extract_chapter.py extract <source_docx> <start> <end> <output> [corrections_json]')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'list':
        list_chapters(sys.argv[2])
    elif command == 'extract':
        source = sys.argv[2]
        start = int(sys.argv[3])
        end = int(sys.argv[4])
        output = sys.argv[5]
        corrections = None
        if len(sys.argv) > 6:
            with open(sys.argv[6], 'r') as f:
                corrections = json.load(f)
        extract_chapter(source, start, end, output, corrections)
    else:
        # Legacy mode: direct args
        source = sys.argv[1]
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        output = sys.argv[4]
        corrections = None
        if len(sys.argv) > 5:
            with open(sys.argv[5], 'r') as f:
                corrections = json.load(f)
        extract_chapter(source, start, end, output, corrections)
