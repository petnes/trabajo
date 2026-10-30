"""Monta el TFM final sobre el borrador original, conservando su formato.

Uso: python3 -I assemble.py SRC.docx OUT.docx APARTADOS_DIR
"""
import copy
import glob
import os
import re
import sys

import docx
from docx.oxml.ns import qn
from lxml import etree

SRC, OUT, APDIR = sys.argv[1], sys.argv[2], sys.argv[3]
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'

d = docx.Document(SRC)
body = d.element.body

# --- mapa de identificadores (mismo orden que dump.py) ---
idmap = {}
idx = 0
for el in list(body.iterchildren()):
    if el.tag == qn('w:p'):
        idmap[idx] = el
        idx += 1
    elif el.tag == qn('w:tbl'):
        for p in el.iter(qn('w:p')):
            idmap[idx] = p
            idx += 1


def ptext(p):
    return ''.join(t.text or '' for t in p.iter(qn('w:t')))


def clean(text):
    text = text.replace('—', ', ').replace('–', '-')
    text = text.replace('**', '').replace('__', '')
    text = re.sub(r'(?<!\w)\*(?!\s)([^*]+?)\*(?!\w)', r'\1', text)
    text = re.sub(r'^\s*[-•]\s+', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.replace(' ,', ',').replace(' .', '.')
    return text.strip()


def first_rpr(p):
    for r in p.iter(qn('w:r')):
        if r.find(qn('w:t')) is not None:
            rpr = r.find(qn('w:rPr'))
            return copy.deepcopy(rpr) if rpr is not None else None
    return None


def make_run(rpr, text, italic=False, bold=None):
    r = etree.Element(qn('w:r'))
    if rpr is not None:
        rp = copy.deepcopy(rpr)
    else:
        rp = etree.Element(qn('w:rPr'))
    for tag in ('w:i', 'w:iCs'):
        for x in rp.findall(qn(tag)):
            rp.remove(x)
    if italic:
        # w:i va tras w:b/w:bCs y antes de color/sz para respetar el esquema
        anchor = None
        for tag in ('w:color', 'w:sz', 'w:szCs', 'w:lang'):
            anchor = rp.find(qn(tag))
            if anchor is not None:
                break
        i_el = etree.Element(qn('w:i'))
        if anchor is not None:
            anchor.addprevious(i_el)
        else:
            rp.append(i_el)
    if bold is not None:
        for x in rp.findall(qn('w:b')):
            rp.remove(x)
        if bold:
            rp.insert(1 if rp.find(qn('w:rFonts')) is not None else 0, etree.Element(qn('w:b')))
    r.append(rp)
    t = etree.SubElement(r, qn('w:t'))
    t.text = text
    t.set(XML_SPACE, 'preserve')
    return r


def set_runs(p, segments):
    """segments: lista de (texto, italic). Sustituye las runs conservando pPr y marcadores."""
    rpr = first_rpr(p)
    children = list(p)
    pos = None
    for i, ch in enumerate(children):
        if ch.tag in (qn('w:r'), qn('w:hyperlink'), qn('w:smartTag'), qn('w:proofErr'), qn('w:ins')):
            if pos is None:
                pos = i
            p.remove(ch)
    if pos is None:
        pos = len(p)
        if p.find(qn('w:pPr')) is not None and pos == 0:
            pos = 1
    for k, (txt, ital) in enumerate(segments):
        p.insert(pos + k, make_run(rpr, txt, italic=ital))


def set_text(p, text):
    set_runs(p, [(text, False)])


def italic_segments(s):
    parts = re.split(r'(\*[^*]+\*)', s)
    segs = []
    for part in parts:
        if not part:
            continue
        if part.startswith('*') and part.endswith('*'):
            segs.append((part[1:-1], True))
        else:
            segs.append((part, False))
    return segs


# --- 1. Sustitución de la prosa reescrita ---
def parse_blocks(fn):
    blocks, cur, buf = {}, None, []
    for line in open(fn, encoding='utf-8'):
        m = re.match(r'^\s*\[P(\d+)\]', line)
        if m:
            if cur is not None:
                blocks[cur] = '\n'.join(buf).strip()
            cur, buf = int(m.group(1)), []
        else:
            buf.append(line.rstrip('\n'))
    if cur is not None:
        blocks[cur] = '\n'.join(buf).strip()
    return blocks


report = []
for fn in sorted(glob.glob(os.path.join(APDIR, '*.md'))):
    blocks = parse_blocks(fn)
    for pid, text in blocks.items():
        p = idmap.get(pid)
        if p is None:
            report.append(f'{os.path.basename(fn)}: id {pid} inexistente')
            continue
        in_cell = p.getparent() is not None and p.getparent().tag == qn('w:tc')
        if text.strip().lower() in ('(eliminar)', 'eliminar'):
            if in_cell:
                set_text(p, '')
            else:
                p.getparent().remove(p)
            continue
        paras = [clean(' '.join(x.split('\n'))) for x in re.split(r'\n\s*\n', text) if x.strip()]
        if not paras:
            continue
        if in_cell and len(paras) > 1:
            paras = [' '.join(paras)]
        set_text(p, paras[0])
        prev = p
        for extra in paras[1:]:
            q = copy.deepcopy(p)
            set_text(q, extra)
            prev.addnext(q)
            prev = q

# --- 2. Referencias en APA 7 con cursivas ---
REFS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referencias.txt')
if os.path.exists(REFS_FILE):
    refs = [l.strip() for l in open(REFS_FILE, encoding='utf-8') if l.strip()]
    biblio = [l for l in refs if not l.startswith('#')]
    split = biblio.index('---')
    bib, norm = biblio[:split], biblio[split + 1:]
    old_bib = [idmap[i] for i in range(769, 794)]
    old_norm = [idmap[i] for i in range(795, 805)]
    for olds, news in ((old_bib, bib), (old_norm, norm)):
        template = olds[0]
        anchor = olds[0].getprevious()
        for o in olds:
            o.getparent().remove(o)
        for line in news:
            q = copy.deepcopy(template)
            set_runs(q, italic_segments(line))
            anchor.addnext(q)
            anchor = q

# --- 3. Supresión del anexo IX (heading, texto, tabla) y de su entrada en el índice ---
h9 = idmap[1319]
el = h9
to_remove = []
while el is not None:
    nxt = el.getnext()
    if el.tag == qn('w:sectPr'):
        break
    to_remove.append(el)
    el = nxt
# conservar el último párrafo vacío si contiene sectPr
for e in to_remove:
    if e.tag == qn('w:p') and e.find('.//' + qn('w:sectPr')) is not None:
        continue
    e.getparent().remove(e)
toc9 = idmap[80]
toc9.getparent().remove(toc9)

# --- 4. Fila nueva en la tabla 10 para el criterio 2.1 ---
for tbl in body.iter(qn('w:tbl')):
    rows = tbl.findall(qn('w:tr'))
    if len(rows) > 2 and ptext(rows[1]).startswith('Cuestionario inicial'):
        new = copy.deepcopy(rows[2])
        vals = ['Informe de análisis de producto',
                'Estudio de un programador de riego comercial: fabricación, uso, reparabilidad y fin de vida',
                '2.1, 6.1', 'SA1', 'Grupal']
        for tc, v in zip(new.findall(qn('w:tc')), vals):
            ps = tc.findall(qn('w:p'))
            set_text(ps[0], v)
            for extra in ps[1:]:
                tc.remove(extra)
        rows[1].addnext(new)
        report.append('tabla 10: fila del criterio 2.1 añadida')
        break

# --- 5. Tamaños de los títulos según la guía docente (12 / 11,5 / 11) ---
def set_sz(p, val):
    for r in p.iter(qn('w:r')):
        rp = r.find(qn('w:rPr'))
        if rp is None:
            rp = etree.SubElement(r, qn('w:rPr'))
            r.remove(rp)
            r.insert(0, rp)
        for tag in ('w:sz', 'w:szCs'):
            for x in rp.findall(qn(tag)):
                rp.remove(x)
        sz = etree.SubElement(rp, qn('w:sz'))
        sz.set(qn('w:val'), str(val))
        szcs = etree.SubElement(rp, qn('w:szCs'))
        szcs.set(qn('w:val'), str(val))


for p in body.iter(qn('w:p')):
    ppr = p.find(qn('w:pPr'))
    if ppr is None:
        continue
    st = ppr.find(qn('w:pStyle'))
    if st is None:
        continue
    sid = st.get(qn('w:val'))
    if sid == 'UNIETITULO':
        set_sz(p, 24)
    elif sid == 'UNIE2AZUL':
        num = ppr.find(qn('w:numPr'))
        lvl = None
        if num is not None and num.find(qn('w:ilvl')) is not None:
            lvl = num.find(qn('w:ilvl')).get(qn('w:val'))
        set_sz(p, 22 if lvl == '2' else 23)

styles = d.styles.element
for s in styles.iter(qn('w:style')):
    sid = s.get(qn('w:styleId'))
    if sid in ('UNIETITULO', 'UNIE2AZUL'):
        rp = s.find(qn('w:rPr'))
        for tag in ('w:sz', 'w:szCs'):
            for x in rp.findall(qn(tag)):
                x.set(qn('w:val'), '24' if sid == 'UNIETITULO' else '23')

# --- 5b. Títulos de tablas y figuras en formato APA 7 ---
def plain_rpr(p):
    rp = None
    for r in p.iter(qn('w:r')):
        if r.find(qn('w:t')) is not None:
            x = r.find(qn('w:rPr'))
            if x is not None and x.find(qn('w:b')) is None:
                return copy.deepcopy(x)
            if rp is None and x is not None:
                rp = copy.deepcopy(x)
    if rp is not None:
        for b in rp.findall(qn('w:b')):
            rp.remove(b)
    return rp


def apa_caption(p, label, title):
    rpr = plain_rpr(p)
    for ch in list(p):
        if ch.tag == qn('w:r'):
            p.remove(ch)
    p.append(make_run(rpr, label, bold=True))
    br = etree.SubElement(p, qn('w:r'))
    if rpr is not None:
        br.append(copy.deepcopy(rpr))
    etree.SubElement(br, qn('w:br'))
    p.append(make_run(rpr, title, italic=True, bold=False))
    return rpr


def set_spacing(p, before, after, jc=None, keep_next=None):
    ppr = p.find(qn('w:pPr'))
    if ppr is None:
        ppr = etree.Element(qn('w:pPr'))
        p.insert(0, ppr)
    sp = ppr.find(qn('w:spacing'))
    if sp is not None:
        sp.set(qn('w:before'), str(before))
        sp.set(qn('w:after'), str(after))
    if jc is not None:
        j = ppr.find(qn('w:jc'))
        if j is not None:
            j.set(qn('w:val'), jc)
    if keep_next is not None:
        kn = ppr.find(qn('w:keepNext'))
        if keep_next and kn is None:
            ppr.insert(0, etree.Element(qn('w:keepNext')))
        if not keep_next and kn is not None:
            ppr.remove(kn)


cap_count = 0
for p in list(body.iterchildren(qn('w:p'))):
    t = ptext(p).strip()
    m = re.match(r'^((?:Tabla|Cuadro) \d+)\.\s+(.*)$', t)
    nxt = p.getnext()
    if m and nxt is not None and nxt.tag == qn('w:tbl'):
        apa_caption(p, m.group(1), m.group(2).rstrip('.'))
        cap_count += 1
        continue
    m = re.match(r'^(Figura \d+)\.\s+(.*)$', t)
    prev = p.getprevious()
    if m and prev is not None and prev.find('.//' + qn('w:drawing')) is not None:
        rest = m.group(2)
        k = rest.find('. ')
        title, note = (rest[:k], rest[k + 2:]) if k > 0 else (rest.rstrip('.'), 'Elaboración propia.')
        note_p = copy.deepcopy(p)
        rpr = apa_caption(p, m.group(1), title)
        for ch in list(note_p):
            if ch.tag == qn('w:r'):
                note_p.remove(ch)
        note_p.append(make_run(rpr, 'Nota.', italic=True, bold=False))
        note_p.append(make_run(rpr, ' ' + note, italic=False, bold=False))
        prev.addprevious(p)          # el título pasa encima de la imagen
        prev.addnext(note_p)         # la nota queda debajo
        set_spacing(p, 240, 60, jc='left', keep_next=True)
        set_spacing(prev, 0, 60, keep_next=True)
        set_spacing(note_p, 0, 240, jc='left', keep_next=False)
        cap_count += 1
report.append(f'títulos APA 7 aplicados: {cap_count}')

# --- 6. Propiedades del archivo vacías ---
cp = d.core_properties
cp.author = ''
cp.last_modified_by = ''
cp.comments = ''
cp.title = ''
cp.subject = ''
cp.keywords = ''
cp.category = ''

d.save(OUT)
print('\n'.join(report) if report else 'ok')
