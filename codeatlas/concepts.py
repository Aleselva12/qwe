"""Conservative, deterministic functional suggestions; never claims runtime correctness."""
import hashlib
import re

RULES = [
    ('runtime', 'Ambiente e dipendenze', 'roots', r'(^|/)(requirements[^/]*|package\.json|pyproject\.toml|Dockerfile|.*compose.*|Makefile)$'),
    ('tests', 'Verifica e qualità', 'branches', r'(^|/)(tests?|test_[^/]+)(/|\.)|\.(test|spec)\.'),
    ('calendar', 'Calendario e sincronizzazione', 'branches', r'calendar|schedule|agenda'),
    ('auth', 'Identità e permessi', 'trunk', r'auth|permission|security'),
    ('storage', 'Memoria e persistenza', 'roots', r'database|storage|migration|models?\b|memory'),
    ('ui', 'Interfaccia e navigazione', 'branches', r'frontend|components?|views?|pages?|index\.html|desktop'),
    ('analysis', 'Analisi e classificazione', 'branches', r'scanner|engine|intelligence|concepts|overlay'),
    ('core', 'Avvio e orchestrazione', 'trunk', r'(^|/)(app|main|server|orchestrator|__main__)\.'),
    ('api', 'Comunicazione e integrazioni', 'branches', r'api|routes?|integrations?|client'),
]

def suggest(atlas, intelligence):
    groups, buckets, owner = [], {}, {}
    for node in atlas['nodes']:
        if node['kind'] != 'file':
            continue
        path = node['path']
        rule = next((r for r in RULES if re.search(r[3], path, re.I)), None)
        if rule:
            key, name, lens, _ = rule
            reason = 'Parole e convenzioni nel percorso: ' + path
        else:
            # Unknown areas stay explicitly uncertain, rather than pretending to know intent.
            area = path.split('/')[0] if '/' in path else 'altre'
            key = 'area-' + area
            name, lens = 'Area da interpretare · ' + area, 'unassigned'
            reason = 'Raggruppamento per area; funzione da confermare.'
        if key not in buckets:
            buckets[key] = dict(id='concept:'+key, name=name, lens=lens, parent=None,
                description='Raggruppa evidenze statiche associate a questa responsabilità proposta.',
                purpose='', future='', issues=[], goals=[], decisions=[], evidence=[],
                status='unknown', code_refs=[], source='heuristic', confidence='da confermare',
                reason=reason)
            groups.append(buckets[key])
        buckets[key]['code_refs'].append(node['id'])
        owner[node['id']] = buckets[key]['id']
    for group in groups:
        docs = [n.get('documentation', '').strip().split('\n')[0] for n in atlas['nodes']
                if n['id'] in group['code_refs'] and n.get('documentation')]
        if docs:
            group['description'] = 'Documentazione dichiarata nei moduli associati (non verificata):\n' + '\n'.join(dict.fromkeys(docs[:4]))
        else:
            group['description'] = ('Responsabilità proposta: '+group['name']+'. '+
                str(len(group['code_refs']))+' sorgenti associati tramite nomi e percorsi; comportamento da confermare.')
    # Runtimes are observed from source languages; hardware is deliberately not guessed.
    for language in sorted({n.get('language') for n in atlas['nodes'] if n.get('language') in ('python', 'javascript', 'typescript')}):
        ident = 'concept:runtime-' + language
        refs = [n['id'] for n in atlas['nodes'] if n.get('language') == language and n['kind'] == 'file']
        groups.append(dict(id=ident, name='Runtime ' + language.title(), lens='roots', parent=None,
            description='Ambiente necessario per i sorgenti '+language+' rilevati. Versione e requisiti da confermare.',
            purpose='', future='', issues=[], code_refs=refs, source='heuristic', confidence='da confermare',
            reason='Linguaggio dei file estratti; nessuna verifica del runtime installato.', status='unknown'))
    # Keep the map navigable: responsibility -> source file -> declaration.
    # File identities do not depend on line numbers, so edits survive insertions.
    file_groups = {}
    by_id = {node['id']: node for node in atlas['nodes']}
    group_by_id = {group['id']: group for group in groups}
    for fid, parent in owner.items():
        node = by_id[fid]
        ident = 'concept:file:' + node['path']
        file_groups[fid] = ident
        groups.append(dict(id=ident, name=node['path'], lens=group_by_id[parent]['lens'],
            parent=parent, description=node.get('documentation') or 'File sorgente associato tramite nomi e percorsi.',
            purpose='', future='', issues=[], code_refs=[fid], source='heuristic',
            confidence='evidenza statica', reason='File rilevato: ' + node['path'], status='unknown'))
    children = {}
    for node in atlas['nodes']:
        parent = file_groups.get(node.get('parent'))
        if not parent or node['kind'] not in ('class', 'function', 'symbol'):
            continue
        key = (parent, node['name'])
        if key not in children:
            children[key] = dict(id='concept:'+hashlib.sha256(repr(key).encode()).hexdigest()[:16],
                name=node['name'].replace('_', ' '), lens=group_by_id[owner[node['parent']]]['lens'],
                parent=parent, description='Dichiarazione rilevata nel sorgente; responsabilità da confermare.',
                purpose='', future='', issues=[], goals=[], decisions=[], evidence=[], status='unknown',
                code_refs=[], source='heuristic', confidence='bassa', reason='Nome estratto dal codice, non interpretazione semantica.')
        children[key]['code_refs'].append(node['id'])
    groups.extend(children.values())
    relations = set()
    for group in groups:
        if group.get('parent') or group['lens'] == 'roots':
            continue
        for language in ('python', 'javascript', 'typescript'):
            root = 'concept:runtime-' + language
            if any(g['id'] == root and set(g['code_refs']) & set(group['code_refs']) for g in groups):
                relations.add((group['id'], root))
    for edge in atlas['edges']:
        a, b = owner.get(edge['from']), owner.get(edge['to'])
        if a and b and a != b:
            relations.add((a,b))
        fa, fb = file_groups.get(edge['from']), file_groups.get(edge['to'])
        if fa and fb and fa != fb:
            relations.add((fa, fb))
    return dict(schema_version=1, project=atlas['project'], groups=groups,
        relations=[dict(**{'from':a,'to':b}, kind='depends_on', source='language_requirement' if b.startswith('concept:runtime-') else 'static_import') for a,b in sorted(relations)],
        limitations=['Classificazione euristica per nomi e percorsi, da confermare.',
            'Scopo, futuro e problemi richiedono input umano; assenza di problemi non significa assenza di difetti.',
            'Hardware, modelli e dipendenze dinamiche non sono rilevati automaticamente.'])
