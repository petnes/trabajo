"""Control de estilo (fase 4) sobre el texto de un .docx montado."""
import re
import statistics
import sys

import docx
from docx.oxml.ns import qn

d = docx.Document(sys.argv[1])
body = d.element.body
paras = []
for el in body.iterchildren():
    if el.tag == qn('w:p'):
        st = el.find(qn('w:pPr'))
        sid = ''
        if st is not None and st.find(qn('w:pStyle')) is not None:
            sid = st.find(qn('w:pStyle')).get(qn('w:val'))
        t = ''.join(x.text or '' for x in el.iter(qn('w:t')))
        paras.append((sid, t))
    elif el.tag == qn('w:tbl'):
        for p in el.iter(qn('w:p')):
            t = ''.join(x.text or '' for x in p.iter(qn('w:t')))
            paras.append(('TC', t))

prose = [(s, t) for s, t in paras if s in ('VIUCUERPOTEXTO', 'TC') and len(t.split()) > 25]
full = '\n'.join(t for _, t in paras)
prose_txt = '\n'.join(t for _, t in prose)

FORB = [r'\babord\w*', r'\binabordable\b', r'enfoque integral', r'\bintegral\b', r'multifac[eé]tic\w*', r'\bpanorama\b',
        r'hol[ií]stic\w*', r'sinergi\w*', r'paradigm\w*', r'resulta fundamental', r'resulta crucial',
        r'juega un papel', r'pone de manifiesto', r'en el mundo actual', r'en el contexto actual', r'cabe destacar',
        r'cabe señalar', r'es importante señalar', r'\basimismo\b', r'por otro lado', r'en este sentido', r'en suma\b',
        r'en definitiva', r'en conclusión', r'en última instancia', r'desde esta perspectiva', r'no solo\b.{0,80}sino también',
        r'\bademás\b', r'\bclave\b', r'\bconviene\b', r'\bresulta\b', r'\bprecisamente\b', r'\bdecisiv\w*', r'descansa en',
        r'se despliega', r'\barticul\w+', r'vertebr\w*', r'materializ\w*', r'lejos de', r'por sí sol\w', r'punto por punto',
        r'cheque en blanco', r'\bimpregna\w*', r'en adelante']
print('== Expresiones vigiladas (todo el documento) ==')
for pat in FORB:
    hits = [m.group(0) for m in re.finditer(pat, prose_txt, re.I)]
    if hits:
        print(f'{pat}: {len(hits)}')
print('rayas —:', full.count('—'), ' guiones medios –:', full.count('–'))
print('preguntas ¿:', prose_txt.count('¿'))
MARCAS = ['Esto no significa que', 'Aquí conviene distinguir', 'Lo que sí parece claro', 'Más interesante resulta',
          'Dicho de otro modo', 'Visto con perspectiva']
for m in MARCAS:
    print('marca', m, prose_txt.count(m))
print('es decir:', prose_txt.count('es decir'), ' por ejemplo:', prose_txt.lower().count('por ejemplo'))
print('primera persona (creo|a mi juicio|me ha):', len(re.findall(r'\b(creo|a mi juicio|me ha|considero)\b', prose_txt, re.I)))

print('\n== Párrafos seguidos que empiezan igual (2 primeras palabras) ==')
body_paras = [t for s, t in paras if s == 'VIUCUERPOTEXTO' and t.strip()]
for a, b in zip(body_paras, body_paras[1:]):
    wa, wb = a.split()[:2], b.split()[:2]
    if [w.lower() for w in wa] == [w.lower() for w in wb]:
        print('  >', ' '.join(wa), '|', a[:60], '||', b[:60])

print('\n== Arranques con demostrativo recapitulativo ==')
dem = [t[:70] for t in body_paras if re.match(r'^(Esa|Ese|Esta|Este|Esto|Estas|Estos|Esas|Esos)\b', t)]
print(len(dem))
sent_dem = re.findall(r'(?:^|\. )(Esa|Ese|Esas|Esos) [a-záéíóúñ]+', prose_txt)
print('frases que empiezan por Esa/Ese/Esas/Esos:', len(sent_dem))

print('\n== Dos puntos dentro de prosa (revisar si son dramáticos) ==')
for t in body_paras:
    for m in re.finditer(r'([^.:]{0,60}): ([^.]{0,40})', t):
        pre = m.group(1).split()
        if len(pre) <= 9:
            print('  :', m.group(0)[:110])

print('\n== Longitud de frases ==')
sents = [s for s in re.split(r'(?<=[.!?])\s+', prose_txt) if len(s.split()) > 2]
lens = [len(s.split()) for s in sents]
print('frases:', len(lens), 'media', round(statistics.mean(lens), 1), 'desv', round(statistics.pstdev(lens), 1),
      'cortas<=8:', sum(1 for x in lens if x <= 8), 'largas>=35:', sum(1 for x in lens if x >= 35))
plens = [len(t.split()) for t in body_paras]
same = sum(1 for a, b in zip(plens, plens[1:]) if abs(a - b) <= 5 and a > 40)
print('párrafos de cuerpo:', len(plens), 'pares seguidos de longitud casi idéntica:', same)
print('palabras de prosa de cuerpo:', sum(plens))
