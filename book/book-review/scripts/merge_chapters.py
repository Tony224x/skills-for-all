"""
Fusionne plusieurs fichiers DOCX de chapitres en un seul document.

Usage:
  python3 merge_chapters.py <output_docx> <chapitre1.docx> <chapitre2.docx> ...
  python3 merge_chapters.py <output_docx> <chapitre1.docx> ... --base <source.docx>

- Utilise le premier chapitre (ou le fichier --base) pour les styles, themes, polices, etc.
- Collecte les paragraphes du body de chaque chapitre dans l'ordre
- Produit un seul DOCX avec tous les chapitres combines
- Ne touche jamais a la mise en page : les styles et formatages sont preserves tels quels
"""
import sys
import os
import zipfile
import shutil
import re
import xml.etree.ElementTree as ET


def merge_chapters(output_docx, chapter_files, base_docx=None):
    """Merge multiple chapter DOCX files into one document.

    Args:
        output_docx: Path for the output merged DOCX
        chapter_files: List of chapter DOCX file paths, in order
        base_docx: Optional base DOCX to use for styles/themes/fonts.
                   If None, uses the first chapter file.
    """
    if not chapter_files:
        print("ERROR: No chapter files provided")
        sys.exit(1)

    # Use base or first chapter for support files (styles, themes, fonts, etc.)
    base_file = base_docx or chapter_files[0]
    work_dir = output_docx + '_workdir'

    # Clean up any previous work
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir)

    # Extract base DOCX to get all support files
    with zipfile.ZipFile(base_file, 'r') as z:
        z.extractall(work_dir)

    # Read and register namespaces from base document.xml
    doc_xml_path = os.path.join(work_dir, 'word', 'document.xml')
    with open(doc_xml_path, 'r', encoding='utf-8') as f:
        raw_xml = f.read()

    ns_matches = re.findall(r'xmlns:?(\w*)=["\']([^"\']+)["\']', raw_xml)
    for prefix, uri in ns_matches:
        if prefix:
            ET.register_namespace(prefix, uri)
        else:
            ET.register_namespace('', uri)

    # Parse the base document
    tree = ET.parse(doc_xml_path)
    root = tree.getroot()

    ns = {}
    for prefix, uri in ns_matches:
        if prefix:
            ns[prefix] = uri

    w_ns = ns.get('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')

    # Find body
    body = root.find(f'{{{w_ns}}}body')
    if body is None:
        print("ERROR: Could not find document body in base file")
        sys.exit(1)

    para_tag = f'{{{w_ns}}}p'
    sect_tag = f'{{{w_ns}}}sectPr'

    # Save sectPr from base (page layout, margins, etc.)
    sect_pr = body.find(sect_tag)
    if sect_pr is not None:
        sect_pr_copy = sect_pr
        body.remove(sect_pr)
    else:
        sect_pr_copy = None

    # Clear the body (remove all existing children)
    for child in list(body):
        body.remove(child)

    # Process each chapter file and add its paragraphs
    total_paras = 0
    for chapter_file in chapter_files:
        if not os.path.exists(chapter_file):
            print(f"WARNING: File not found: {chapter_file}, skipping")
            continue

        # Read chapter document.xml
        with zipfile.ZipFile(chapter_file, 'r') as z:
            chapter_xml = z.read('word/document.xml')

        chapter_root = ET.fromstring(chapter_xml)
        chapter_body = chapter_root.find(f'{{{w_ns}}}body')

        if chapter_body is None:
            print(f"WARNING: No body found in {chapter_file}, skipping")
            continue

        # Add all children except sectPr
        chapter_para_count = 0
        for child in list(chapter_body):
            if child.tag == sect_tag:
                continue
            body.append(child)
            if child.tag == para_tag:
                chapter_para_count += 1

        total_paras += chapter_para_count
        print(f"  + {os.path.basename(chapter_file)}: {chapter_para_count} paragraphs")

    # Re-add sectPr at the end
    if sect_pr_copy is not None:
        body.append(sect_pr_copy)

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
    print(f"\nGenerated: {output_docx} ({total_paras} paragraphs total)")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage:')
        print('  python3 merge_chapters.py <output.docx> <ch1.docx> <ch2.docx> ...')
        print('  python3 merge_chapters.py <output.docx> <ch1.docx> ... --base <source.docx>')
        sys.exit(1)

    # Parse arguments
    args = sys.argv[1:]
    output = args[0]
    base = None

    # Check for --base flag
    chapter_args = args[1:]
    if '--base' in chapter_args:
        base_idx = chapter_args.index('--base')
        base = chapter_args[base_idx + 1]
        chapter_args = chapter_args[:base_idx] + chapter_args[base_idx + 2:]

    merge_chapters(output, chapter_args, base)
