import uuid
from xml.sax.saxutils import escape

def uid():
    return str(uuid.uuid4())

OUT = []

def emit2(tag, eid, fields):
    """fields: list of (name, kind, value); kind in {'val','ref','reflist'}"""
    parts = [f'<{tag} id="{eid}">']
    for name, kind, value in fields:
        if value is None or (kind == 'reflist' and not value):
            continue
        parts.append(f'<{name}>')
        if kind == 'val':
            parts.append(f'<val>{escape(str(value))}</val>')
        elif kind == 'ref':
            parts.append(f'<ref refid="{value}"/>')
        else:
            parts.append('<reflist>')
            for r in value:
                parts.append(f'<ref refid="{r}"/>')
            parts.append('</reflist>')
        parts.append(f'</{name}>')
    parts.append(f'</{tag}>')
    OUT.append('\n'.join(parts) + '\n')

SS = uid()      # StyleSheet
PKG = uid()     # Package
DIA = uid()     # Diagram
SM = uid()      # StateMachine
ROOT = uid()    # Região raiz da StateMachine

WHITE  = 'rgba(255, 255, 255, 1.0)'
BLACK  = 'rgba(0, 0, 0, 1.0)'
PINK   = 'rgba(255, 192, 203, 1.0)'
RED    = 'rgba(224, 62, 62, 1.0)'
MAGENTA= 'rgba(214, 42, 214, 1.0)'
CYAN   = 'rgba(132, 222, 239, 1.0)'
BLUE   = 'rgba(53, 102, 222, 1.0)'
GREEN  = 'rgba(134, 222, 134, 1.0)'
YELLOW = 'rgba(249, 240, 107, 1.0)'
ORANGE = 'rgba(255, 163, 72, 1.0)'
LGRAY  = 'rgba(211, 211, 211, 1.0)'
GRAY   = 'rgba(154, 153, 150, 1.0)'
DGRAY  = 'rgba(94, 92, 100, 1.0)'

MODULES = [
    {
        'key': 'm1',
        'name': 'M1 — Entendendo o problema  [Bloom: Lembrar + Compreender]',
        'pos': (40, 80), 'size': (1200, 190),
        'blocks': [
            ('custoquery', 'CustoQuery : conceito : slides — Explanatório: custo de query, ciclo da consulta; métricas: Tempo, I/O, CPU, Memória', 30, 70, 260, 90, PINK, BLACK),
            ('querylenta', 'QueryLenta : exemplo : video — Exemplo: demonstração de query lenta no PostgreSQL real', 320, 70, 260, 90, PINK, BLACK),
            ('ad_m1', 'AD_M1 : avaliacao_diagnostica : quiz — Avaliação diagnóstica: quiz com 3 questões sobre conhecimento prévio', 610, 70, 270, 90, RED, WHITE),
            ('fin_m1', 'Finalidade: Sensibilizar sobre o custo de queries e a importância da otimização', 910, 70, 270, 90, MAGENTA, WHITE),
        ],
        'flow': [('custoquery', 'querylenta'), ('querylenta', 'ad_m1')],
    },
    {
        'key': 'm2',
        'name': 'M2 — Diagnóstico  [Bloom: Compreender + Analisar]',
        'pos': (40, 320), 'size': (580, 620),
        'blocks': [
            ('explain', 'EXPLAIN : conceito : slides — Explanatório: EXPLAIN, EXPLAIN ANALYZE, BUFFERS, FORMAT JSON', 20, 60, 260, 90, CYAN, BLACK),
            ('explain_analyze', 'EXPLAIN_ANALYZE : procedimento : codigo_sql — Procedimento: executar e interpretar a saída do EXPLAIN ANALYZE', 300, 60, 260, 90, CYAN, BLACK),
            ('plano', 'PlanoExecucao : conceito : slides — Explanatório: plano de execução; Seq Scan, Index Scan, Index Only Scan, Bitmap Heap Scan', 300, 170, 260, 90, CYAN, BLACK),
            ('joins_c', 'EstrategiasJoin : conceito : slides — Explanatório: Nested Loop, Hash Join, Merge Join — condições de uso', 20, 170, 260, 90, CYAN, BLACK),
            ('joins_p', 'EstrategiasJoin : principio : slides — Princípio: quando o planejador escolhe cada estratégia de join', 20, 280, 260, 90, CYAN, BLACK),
            ('pgstat', 'pgStatStatements : conceito : slides — Explanatório: pg_stat_statements e pg_stat_activity', 300, 280, 260, 90, CYAN, BLACK),
            ('diag', 'DiagnosticarQuery : exercicio : hands_on — Exercício: diagnosticar query real com EXPLAIN', 300, 390, 260, 90, CYAN, BLACK),
            ('af_m2', 'AF_M2 : avaliacao_formativa : quiz — Avaliação formativa sobre diagnóstico e plano de execução', 20, 390, 260, 90, BLUE, WHITE),
            ('fin_m2', 'Finalidade: Identificar gargalos de performance em queries', 20, 500, 540, 90, BLUE, WHITE),
        ],
        'flow': [('explain', 'explain_analyze'), ('explain_analyze', 'plano'), ('plano', 'joins_c'),
                 ('joins_c', 'joins_p'), ('joins_p', 'pgstat'), ('pgstat', 'diag'), ('diag', 'af_m2')],
    },
    {
        'key': 'm3a',
        'name': 'M3A — Índices  [Bloom: Analisar]',
        'pos': (660, 320), 'size': (580, 620),
        'blocks': [
            ('btree', 'BTree_GIN_GIST_BRIN : conceito : slides — Explanatório: B-Tree (igualdade/intervalos), GIN (arrays/JSONB), GiST (espacial), BRIN (sequências longas)', 20, 60, 260, 90, GREEN, BLACK),
            ('parcial_c', 'IndiceParcial_Composto : conceito : slides — Explanatório: índice parcial (WHERE), índice composto (múltiplas colunas)', 300, 60, 260, 90, GREEN, BLACK),
            ('ios', 'IndexOnlyScan : principio : slides — Princípio: índice cobridor (Index Only Scan) — quando e como aplicar', 300, 170, 260, 90, GREEN, BLACK),
            ('parcial_p', 'IndiceParcial : principio : slides — Princípio: regras de uso e trade-offs de cada tipo de índice', 20, 170, 260, 90, GREEN, BLACK),
            ('aplicar', 'AplicarIndice : exercicio : hands_on — Exercício: aplicar índice correto e comparar plano antes/depois', 20, 280, 260, 90, GREEN, BLACK),
            ('af_m3a', 'AF_M3A : avaliacao_formativa : quiz — Avaliação formativa sobre tipos de índice e condições de uso', 300, 280, 260, 90, GREEN, BLACK),
            ('fin_m3a', 'Finalidade: Escolher o índice correto para cada situação', 20, 500, 540, 90, GREEN, BLACK),
        ],
        'flow': [('btree', 'parcial_c'), ('parcial_c', 'ios'), ('ios', 'parcial_p'),
                 ('parcial_p', 'aplicar'), ('aplicar', 'af_m3a')],
    },
    {
        'key': 'm3b',
        'name': 'M3B — Reescrita de consulta  [Bloom: Aplicar]',
        'pos': (40, 990), 'size': (580, 510),
        'blocks': [
            ('boas', 'BoasPraticas : conceito : slides — Explanatório: EXISTS, CTE (WITH), JOIN explícito', 20, 60, 260, 90, YELLOW, BLACK),
            ('anti_c', 'Antipadroes : conceito : slides — Explanatório: SELECT *, função em coluna WHERE, OFFSET elevado, N+1 Queries, conversão implícita de tipo', 300, 60, 260, 90, YELLOW, BLACK),
            ('anti_e', 'Antipadroes : exemplo : codigo_sql — Exemplo: código SQL antes e depois de cada antipadrão', 300, 170, 260, 90, YELLOW, BLACK),
            ('reescrever', 'ReescreverQuery : exercicio : hands_on — Exercício: reescrever queries reais com antipadrões identificados', 20, 170, 260, 90, YELLOW, BLACK),
            ('af_m3b', 'AF_M3B : avaliacao_formativa : quiz — Avaliação formativa sobre antipadrões SQL', 20, 280, 260, 90, ORANGE, BLACK),
            ('fin_m3b', 'Finalidade: Eliminar antipadrões de SQL e reescrever queries eficientes', 20, 390, 540, 90, ORANGE, BLACK),
        ],
        'flow': [('boas', 'anti_c'), ('anti_c', 'anti_e'), ('anti_e', 'reescrever'), ('reescrever', 'af_m3b')],
    },
    {
        'key': 'm3c',
        'name': 'M3C — Infraestrutura e manutenção  [Bloom: Compreender]',
        'pos': (660, 990), 'size': (580, 510),
        'blocks': [
            ('estat', 'Estatisticas : conceito : slides — Explanatório: cardinalidade, histograma, MCV (Most Common Values)', 20, 60, 260, 90, LGRAY, BLACK),
            ('vacuum', 'VACUUM : conceito : slides — Explanatório: VACUUM remove tuplas mortas e fragmentação', 300, 60, 260, 90, LGRAY, BLACK),
            ('analyze', 'ANALYZE : procedimento : slides — Procedimento: ANALYZE atualiza estatísticas do planejador', 300, 170, 260, 90, LGRAY, BLACK),
            ('estat_p', 'EstatisticasDesatualizadas : principio : slides — Princípio: impacto de estatísticas desatualizadas no plano', 20, 170, 260, 90, LGRAY, BLACK),
            ('impacto', 'ImpactoEstatisticas : exercicio : hands_on — Exercício: demonstrar impacto de estatísticas desatualizadas', 20, 280, 260, 90, LGRAY, BLACK),
            ('af_m3c', 'AF_M3C : avaliacao_formativa : quiz — Avaliação formativa sobre estatísticas e VACUUM', 300, 280, 260, 90, BLUE, WHITE),
            ('fin_m3c', 'Finalidade: Manter o planejador com estatísticas precisas', 20, 390, 540, 90, BLUE, WHITE),
        ],
        'flow': [('estat', 'vacuum'), ('vacuum', 'analyze'), ('analyze', 'estat_p'),
                 ('estat_p', 'impacto'), ('impacto', 'af_m3c')],
    },
    {
        'key': 'af',
        'name': 'Avaliação Final  [Bloom: Avaliar]',
        'pos': (40, 1550), 'size': (1200, 220),
        'blocks': [
            ('queries', 'QueriesProblematicas : avaliacao_somativa : hands_on — Avaliação somativa: 5 queries problemáticas — diagnosticar, corrigir e justificar', 30, 70, 330, 90, GRAY, BLACK),
            ('feedback', 'FeedbackAutomatico : complementar : sistema — Complementar: feedback automático com explicação de cada resposta', 400, 70, 330, 90, GRAY, BLACK),
            ('fin_af', 'Finalidade: Avaliar a aprendizagem de todo o OA', 860, 70, 310, 90, DGRAY, WHITE),
        ],
        'flow': [('queries', 'feedback')],
    },
]

DD_KEYS = ['m1', 'm2', 'm3a', 'm3b', 'm3c']
GUARD_DD = 'DD'
GUARD_AF = 'todos os módulos concluídos'

state_id = {}        # key -> id semântico
item_id = {}         # key -> id do item de apresentação
abs_center = {}      # key -> (cx, cy) absoluto no diagrama
incoming = {}        # state id -> [transition ids]
outgoing = {}        # state id -> [transition ids]
presentations = []   # ids de todos os itens (ownedPresentation)
region_of = {}       # module key -> region id (container dos filhos)

for m in MODULES:
    state_id[m['key']] = uid()
    item_id[m['key']] = uid()
    region_of[m['key']] = uid()
    mx, my = m['pos']
    mw, mh = m['size']
    abs_center[m['key']] = (mx + mw / 2, my + mh / 2)
    for b in m['blocks']:
        key = b[0]
        state_id[key] = uid()
        item_id[key] = uid()
        bx, by, bw, bh = b[2], b[3], b[4], b[5]
        abs_center[key] = (mx + bx + bw / 2, my + by + bh / 2)

P0 = uid(); P0_ITEM = uid()                    # pseudostate inicial (raiz)
FINAL = uid(); FINAL_ITEM = uid()              # estado final (dentro da AF)
abs_center['__p0__'] = (100, 30)
afm = MODULES[-1]
abs_center['__final__'] = (afm['pos'][0] + 770 + 15, afm['pos'][1] + 100 + 15)

def add_edge(d, k, v):
    d.setdefault(k, []).append(v)

# (tid, cid, ti_id, container_region, src_sid, tgt_sid, src_item, tgt_item, guard, p1, p2)
transitions = []

def make_transition(container, src_key, tgt_key, guard=None,
                    src_sid=None, tgt_sid=None, src_item=None, tgt_item=None):
    tid, cid, ti = uid(), uid(), uid()
    s_sid = src_sid or state_id[src_key]
    t_sid = tgt_sid or state_id[tgt_key]
    s_it = src_item or item_id[src_key]
    t_it = tgt_item or item_id[tgt_key]
    p1 = abs_center[src_key] if src_key in abs_center else None
    p2 = abs_center[tgt_key] if tgt_key in abs_center else None
    transitions.append((tid, cid, ti, container, s_sid, t_sid, s_it, t_it, guard, p1, p2))
    add_edge(outgoing, s_sid, tid)
    add_edge(incoming, t_sid, tid)
    presentations.append(ti)
    return tid

# fluxo interno de cada módulo
for m in MODULES:
    for src, tgt in m['flow']:
        make_transition(region_of[m['key']], src, tgt)

# feedback -> estado final (dentro da AF)
make_transition(region_of['af'], 'feedback', '__final__',
                tgt_sid=FINAL, tgt_item=FINAL_ITEM)

# inicial -> M1
make_transition(ROOT, '__p0__', 'm1', src_sid=P0, src_item=P0_ITEM)

# [DD] navegação livre: todos os pares ordenados entre módulos
for a in DD_KEYS:
    for b in DD_KEYS:
        if a != b:
            make_transition(ROOT, a, b, guard=GUARD_DD)

# [guard] módulos -> Avaliação Final
for a in DD_KEYS:
    make_transition(ROOT, a, 'af', guard=GUARD_AF)

# StyleSheet (CSS por nome de estado)
css_rules = ['diagram {\n}\n']
for m in MODULES:
    css_rules.append(f'state[name="{m["name"]}"] {{\n  background-color: {WHITE};\n  text-color: {BLACK};\n}}\n')
    for b in m['blocks']:
        css_rules.append(f'state[name="{b[1]}"] {{\n  background-color: {b[6]};\n  text-color: {b[7]};\n}}\n')
css = '\n'.join(css_rules)

emit2('Core:StyleSheet', SS, [('styleSheet', 'val', css)])

emit2('UML:Package', PKG, [
    ('name', 'val', 'Otimização de Consultas com PostgreSQL'),
    ('ownedDiagram', 'reflist', [DIA]),
    ('ownedType', 'reflist', [SM]),
    ('packagedElement', 'reflist', [SM]),
])

# itens de apresentação: módulos, blocos, pseudostate, final, transições
all_items = [P0_ITEM]
for m in MODULES:
    all_items.append(item_id[m['key']])
    for b in m['blocks']:
        all_items.append(item_id[b[0]])
all_items.append(FINAL_ITEM)
all_items += presentations

emit2('UML:Diagram', DIA, [
    ('element', 'ref', PKG),
    ('name', 'val', 'Modelo Instrucional — IMA-CID (Otimização de Consultas com PostgreSQL)'),
    ('ownedPresentation', 'reflist', all_items),
])

emit2('UML:StateMachine', SM, [
    ('name', 'val', 'OA: Otimização de Consultas com PostgreSQL'),
    ('owningPackage', 'ref', PKG),
    ('package', 'ref', PKG),
    ('region', 'reflist', [ROOT]),
])

root_subvertex = [P0] + [state_id[m['key']] for m in MODULES]
emit2('UML:Region', ROOT, [
    ('stateMachine', 'ref', SM),
    ('subvertex', 'reflist', root_subvertex),
])

# pseudostate inicial
emit2('UML:Pseudostate', P0, [
    ('container', 'ref', ROOT),
    ('outgoing', 'reflist', outgoing.get(P0, [])),
    ('presentation', 'reflist', [P0_ITEM]),
])
emit2('UML:PseudostateItem', P0_ITEM, [
    ('matrix', 'val', '(1.0, 0.0, 0.0, 1.0, 90.0, 20.0)'),
    ('top-left', 'val', '(0.0, 0.0)'),
    ('width', 'val', '20.0'),
    ('height', 'val', '20.0'),
    ('diagram', 'ref', DIA),
    ('subject', 'ref', P0),
])

# módulos e blocos
for m in MODULES:
    mk = m['key']
    msid, mitem, mregion = state_id[mk], item_id[mk], region_of[mk]
    mx, my = m['pos']
    mw, mh = m['size']
    child_states = [state_id[b[0]] for b in m['blocks']]
    child_items = [item_id[b[0]] for b in m['blocks']]
    if mk == 'af':
        child_states.append(FINAL)
        child_items.append(FINAL_ITEM)

    emit2('UML:State', msid, [
        ('container', 'ref', ROOT),
        ('incoming', 'reflist', incoming.get(msid, [])),
        ('name', 'val', m['name']),
        ('outgoing', 'reflist', outgoing.get(msid, [])),
        ('presentation', 'reflist', [mitem]),
        ('region', 'reflist', [mregion]),
    ])
    emit2('UML:StateItem', mitem, [
        ('matrix', 'val', f'(1.0, 0.0, 0.0, 1.0, {float(mx)}, {float(my)})'),
        ('top-left', 'val', '(0.0, 0.0)'),
        ('width', 'val', float(mw)),
        ('height', 'val', float(mh)),
        ('children', 'reflist', child_items),
        ('diagram', 'ref', DIA),
        ('subject', 'ref', msid),
    ])
    emit2('UML:Region', mregion, [
        ('state', 'ref', msid),
        ('subvertex', 'reflist', child_states),
    ])
    for b in m['blocks']:
        bk, bname, bx, by, bw, bh = b[0], b[1], b[2], b[3], b[4], b[5]
        bsid, bitem = state_id[bk], item_id[bk]
        emit2('UML:State', bsid, [
            ('container', 'ref', mregion),
            ('incoming', 'reflist', incoming.get(bsid, [])),
            ('name', 'val', bname),
            ('outgoing', 'reflist', outgoing.get(bsid, [])),
            ('presentation', 'reflist', [bitem]),
        ])
        emit2('UML:StateItem', bitem, [
            ('matrix', 'val', f'(1.0, 0.0, 0.0, 1.0, {float(bx)}, {float(by)})'),
            ('top-left', 'val', '(0.0, 0.0)'),
            ('width', 'val', float(bw)),
            ('height', 'val', float(bh)),
            ('diagram', 'ref', DIA),
            ('parent', 'ref', mitem),
            ('subject', 'ref', bsid),
        ])

# estado final (dentro da Avaliação Final)
emit2('UML:FinalState', FINAL, [
    ('container', 'ref', region_of['af']),
    ('incoming', 'reflist', incoming.get(FINAL, [])),
    ('presentation', 'reflist', [FINAL_ITEM]),
])
emit2('UML:FinalStateItem', FINAL_ITEM, [
    ('matrix', 'val', '(1.0, 0.0, 0.0, 1.0, 770.0, 100.0)'),
    ('top-left', 'val', '(0.0, 0.0)'),
    ('width', 'val', '30.0'),
    ('height', 'val', '30.0'),
    ('diagram', 'ref', DIA),
    ('parent', 'ref', item_id['af']),
    ('subject', 'ref', FINAL),
])

# transições
for (tid, cid, ti, container, s_sid, t_sid, s_it, t_it, guard, p1, p2) in transitions:
    emit2('UML:Transition', tid, [
        ('container', 'ref', container),
        ('guard', 'ref', cid),
        ('presentation', 'reflist', [ti]),
        ('source', 'ref', s_sid),
        ('target', 'ref', t_sid),
    ])
    cfields = []
    if guard:
        cfields.append(('specification', 'val', guard))
    cfields.append(('transition', 'ref', tid))
    emit2('UML:Constraint', cid, cfields)
    x1, y1 = p1
    x2, y2 = p2
    emit2('UML:TransitionItem', ti, [
        ('diagram', 'ref', DIA),
        ('horizontal', 'val', 'False'),
        ('orthogonal', 'val', 'False'),
        ('subject', 'ref', tid),
        ('matrix', 'val', '(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)'),
        ('points', 'val', f'[({x1}, {y1}), ({x2}, {y2})]'),
        ('head-connection', 'ref', s_it),
        ('tail-connection', 'ref', t_it),
    ])

header = ('<?xml version="1.0" encoding="utf-8"?>\n'
          '<gaphor xmlns="https://gaphor.org/model" '
          'xmlns:Core="https://gaphor.org/modelinglanguage/Core" '
          'xmlns:UML="https://gaphor.org/modelinglanguage/UML" '
          'xmlns:general="https://gaphor.org/modelinglanguage/general" '
          'version="4" gaphor-version="3.3.2">\n<model>\n')
footer = '</model>\n</gaphor>\n'

content = header + ''.join(OUT) + footer

with open('modelo_instrucional.gaphor', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

import re
ids = set(re.findall(r'id="([0-9a-f-]{36})"', content))
refs = set(re.findall(r'refid="([0-9a-f-]{36})"', content))
dangling = refs - ids
print(f'elementos: {len(ids)}, refs: {len(refs)}, refs órfãs: {len(dangling)}')
if dangling:
    raise SystemExit(f'ERRO: refs órfãs: {dangling}')
import xml.dom.minidom
xml.dom.minidom.parseString(content.encode('utf-8'))
print('XML bem-formado. OK ->', 'modelo_instrucional.gaphor')

# ================================================================
# Preview SVG do diagrama (imgs/modelo-instrucional.svg)
# ================================================================
import textwrap, os

svg = []
add = svg.append

VB = '-95 -10 1470 1880'
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" '
    f'font-family="Segoe UI, Arial, sans-serif">')
add('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
    'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    '<path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>')
add('<rect x="-95" y="-10" width="1470" height="1880" fill="white"/>')
add('<text x="640" y="28" text-anchor="middle" font-size="19" font-weight="bold">'
    'Otimização de Consultas com PostgreSQL — Modelo Instrucional (IMA–CID / HMBS Instrucional)</text>')

def esc(t):
    return escape(t)

def arrow(points, label=None, double=False, lx=None, ly=None,
          fs=10, rotate=False):
    pts = ' '.join(f'{x},{y}' for x, y in points)
    ms = ' marker-start="url(#arr)"' if double else ''
    add(f'<polyline points="{pts}" fill="none" stroke="#333" '
        f'stroke-width="1.4"{ms} marker-end="url(#arr)"/>')
    if label:
        if rotate:
            add(f'<text transform="translate({lx},{ly}) rotate(-90)" '
                f'font-size="{fs}" fill="#333">{esc(label)}</text>')
        else:
            add(f'<text x="{lx}" y="{ly}" font-size="{fs}" fill="#333">{esc(label)}</text>')

abs_rect = {}
for m in MODULES:
    mx, my = m['pos']
    for b in m['blocks']:
        abs_rect[b[0]] = (mx + b[2], my + b[3], b[4], b[5])
abs_rect['__final__'] = (MODULES[-1]['pos'][0] + 770, MODULES[-1]['pos'][1] + 100, 30, 30)

# módulos
for m in MODULES:
    mx, my = m['pos']
    mw, mh = m['size']
    add(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="12" '
        f'fill="white" stroke="#333" stroke-width="1.8"/>')
    add(f'<text x="{mx + mw / 2}" y="{my + 24}" text-anchor="middle" '
        f'font-size="14" font-weight="bold">{esc(m["name"])}</text>')
    for b in m['blocks']:
        bx, by, bw, bh = abs_rect[b[0]]
        bg, fg = b[6], b[7]
        add(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" '
            f'fill="{bg}" stroke="#333" stroke-width="1"/>')
        name = b[1]
        if ' — ' in name:
            head, desc = name.split(' — ', 1)
        else:
            head, desc = name, ''
        maxc = max(20, int(bw / 6.6))
        lines = [(l, True) for l in textwrap.wrap(head, maxc)]
        lines += [(l, False) for l in textwrap.wrap(desc, maxc)]
        ty = by + 17
        for line, bold in lines:
            if ty > by + bh - 4:
                break
            w = ' font-weight="bold"' if bold else ''
            add(f'<text x="{bx + bw / 2}" y="{ty}" text-anchor="middle" '
                f'font-size="10"{w} fill="{fg}">{esc(line)}</text>')
            ty += 13

# estado inicial -> M1
add('<circle cx="100" cy="55" r="8" fill="#333"/>')
arrow([(100, 63), (100, 80)])

# estado final (dentro da Avaliação Final)
fx, fy, fw, fh = abs_rect['__final__']
cx, cy = fx + fw / 2, fy + fh / 2
add(f'<circle cx="{cx}" cy="{cy}" r="12" fill="white" stroke="#333" stroke-width="1.5"/>')
add(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#333"/>')

# fluxo interno (blocos alinhados por linha ou coluna)
for m in MODULES:
    for src, tgt in m['flow'] + ([('feedback', '__final__')] if m['key'] == 'af' else []):
        sx, sy, sw, sh = abs_rect[src]
        tx, ty, tw, th = abs_rect[tgt]
        scy, tcy = sy + sh / 2, ty + th / 2
        if abs(scy - tcy) < 1 or src == 'feedback':
            if tx > sx:
                arrow([(sx + sw, scy), (tx, tcy)])
            else:
                arrow([(sx, scy), (tx + tw, tcy)])
        else:
            arrow([(sx + sw / 2, sy + sh), (tx + tw / 2, ty)])

# [DD] navegação livre entre módulos (bidirecional)
DD = '[DD]'
arrow([(330, 270), (330, 320)], DD, True, 338, 301)        # M1<->M2
arrow([(950, 270), (950, 320)], DD, True, 958, 301)        # M1<->M3A
arrow([(620, 630), (660, 630)], DD, True, 622, 622)        # M2<->M3A
arrow([(330, 940), (330, 990)], DD, True, 338, 971)        # M2<->M3B
arrow([(950, 940), (950, 990)], DD, True, 958, 971)        # M3A<->M3C
arrow([(620, 1245), (660, 1245)], DD, True, 622, 1237)     # M3B<->M3C
arrow([(40, 175), (-20, 175), (-20, 1245), (40, 1245)], DD, True, -14, 700)    # M1<->M3B
arrow([(1240, 175), (1300, 175), (1300, 1245), (1240, 1245)], DD, True, 1248, 700)  # M1<->M3C
arrow([(500, 940), (500, 962), (840, 962), (840, 990)], DD, True, 655, 957)    # M2<->M3C
arrow([(790, 940), (790, 968), (450, 968), (450, 990)], DD, True, 600, 983)    # M3A<->M3B

# [guard] módulos -> Avaliação Final
G = '[todos os módulos concluídos]'
arrow([(200, 1500), (200, 1550)], G, False, 206, 1528, 9)
arrow([(1080, 1500), (1080, 1550)], G, False, 1086, 1528, 9)
arrow([(40, 230), (-65, 230), (-65, 1620), (40, 1620)], G, False, -70, 1000, 9, rotate=True)
arrow([(40, 870), (-35, 870), (-35, 1640), (40, 1640)], G, False, -40, 1330, 9, rotate=True)
arrow([(1240, 870), (1315, 870), (1315, 1640), (1240, 1640)], G, False, 1325, 1330, 9, rotate=True)

# legenda
add('<text x="640" y="1810" text-anchor="middle" font-size="11" fill="#333">'
    '[DD] = navegação livre (decisão do aprendiz — Especificação Aberta)  •  '
    '[guard] = pré-requisito para a Avaliação Final</text>')
add('<text x="640" y="1830" text-anchor="middle" font-size="11" fill="#333">'
    'Categorias CDT: Explanatório, Exemplo, Procedimento, Princípio, Exercício, Complementar  •  '
    'Avaliações: diagnóstica (M1), formativa (M2–M3C), somativa (Final)</text>')

add('</svg>')

os.makedirs('imgs', exist_ok=True)
with open(os.path.join('imgs', 'modelo-instrucional.svg'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(svg) + '\n')
print('Preview SVG OK -> imgs/modelo-instrucional.svg')
