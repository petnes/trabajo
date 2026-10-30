"""Actualiza los números de página guardados en el índice (TOC) a partir del PDF renderizado.

Uso: python3 -I toc_update.py DOC.docx DOC.pdf
"""
import re
import sys

import docx
import pdfplumber
from docx.oxml.ns import qn

DOC, PDF = sys.argv[1], sys.argv[2]
d = docx.Document(DOC)
pages = []
with pdfplumber.open(PDF) as pdf:
    for pg in pdf.pages:
        lines = [re.sub(r'\s+', ' ', l).strip() for l in (pg.extract_text() or '').split('\n')]
        pages.append(lines)


def norm(s):
    return re.sub(r'\s+', '', s).strip().lower()


entries = []
for p in d.element.body.iter(qn('w:p')):
    ppr = p.find(qn('w:pPr'))
    if ppr is None or ppr.find(qn('w:pStyle')) is None:
        continue
    if not ppr.find(qn('w:pStyle')).get(qn('w:val')).startswith('TDC'):
        continue
    ts = [t for t in p.iter(qn('w:t'))]
    if not ts or not (ts[-1].text or '').strip().isdigit():
        continue
    texts = [t.text or '' for t in ts[:-1]]
    num = texts[0].strip() if re.fullmatch(r'\d+(\.\d+)*\.', texts[0].strip()) else ''
    title = ''.join(texts[1:] if num else texts).strip()
    entries.append((num, title, ts[-1]))

# el índice ocupa las primeras páginas: empezar a buscar después de la última página que contiene "ÍNDICE"
start = 0
for i, lines in enumerate(pages[:10]):
    if any(l.strip() == 'ÍNDICE' for l in lines):
        start = i + 1
ptr = start
changes = []
for num, title, tnode in entries:
    target = norm((num + title) if num else title)[:34]
    found = None
    for i in range(ptr, len(pages)):
        for l in pages[i]:
            if norm(l).startswith(target):
                found = i
                break
        if found is not None:
            break
    if found is None:
        changes.append(f'NO ENCONTRADO: {num} {title}')
        continue
    ptr = found
    new = str(found + 1)
    if tnode.text != new:
        changes.append(f'{num} {title[:40]}: {tnode.text} -> {new}')
        tnode.text = new
d.save(DOC)
print('\n'.join(changes) if changes else 'índice sin cambios')
