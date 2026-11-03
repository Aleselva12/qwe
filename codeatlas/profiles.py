"""Validation of portable profile data; no executable hooks are supported."""
import re

VIEWS = {'graph', 'text', 'network', 'layers', 'matrix', 'files'}
STATES = {'idea', 'planned', 'in_progress', 'implemented', 'verified', 'blocked', 'unknown'}

def validate_profile(profile):
    if not isinstance(profile, dict) or profile.get('schema_version') != 1 or not isinstance(profile.get('name'), str) or not profile['name'].strip() or profile.get('default_view', 'graph') not in VIEWS:
        raise ValueError('Invalid profile version, name or default view')
    for key in ('categories', 'fields', 'nodes', 'rules', 'test_links'):
        if not isinstance(profile.get(key, []), list):
            raise ValueError('Invalid profile list: ' + key)
    for key in ('categories', 'fields'):
        seen = set()
        for item in profile.get(key, []):
            if not isinstance(item, dict):
                raise ValueError('Invalid category or field')
            ident = item.get('id')
            if not isinstance(ident, str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', ident) or ident in {'constructor', 'prototype', '__proto__'} or ident in seen or not isinstance(item.get('label'), str) or not item['label'].strip():
                raise ValueError('Invalid or duplicate category/field ID')
            seen.add(ident)
            if key == 'categories' and (not isinstance(item.get('color'), str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', item['color'])):
                raise ValueError('Invalid category color')
    seen = set()
    for node in profile.get('nodes', []):
        if not isinstance(node, dict) or not isinstance(node.get('id'), str) or not node['id'] or node['id'] in seen or not isinstance(node.get('name'), str) or not node['name'] or node.get('source') not in {'manual', 'ai_suggestion'} or node.get('status') not in STATES:
            raise ValueError('Invalid profile node')
        seen.add(node['id'])
    for rule in profile.get('rules', []):
        if not isinstance(rule, dict) or not isinstance(rule.get('path_glob'), str) or not 1 <= len(rule['path_glob']) <= 300 or not isinstance(rule.get('group_id'), str):
            raise ValueError('Invalid profile grouping rule')
    for link in profile.get('test_links', []):
        if not isinstance(link, dict) or not isinstance(link.get('group_id'), str) or link.get('source') not in {'manual', 'ai_suggestion'} or not any(isinstance(link.get(k), str) and link[k] for k in ('name', 'classname', 'file')) or any(k in link and not isinstance(link[k], str) for k in ('name', 'classname', 'file')):
            raise ValueError('Invalid test association')
    return profile
