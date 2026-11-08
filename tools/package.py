import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = 'karpathy-regula'
PLUGIN_REL = Path('plugins') / PLUGIN_NAME


def validate(root=ROOT):
    root = Path(root).resolve()
    plugin = root / PLUGIN_REL
    portable = json.loads((plugin / 'plugin.json').read_text(encoding='utf-8'))
    claude = json.loads((plugin / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
    codex = json.loads((plugin / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    assert portable['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'Portable schema missing'
    assert portable['name'] == PLUGIN_NAME, 'Wrong plugin identity'
    assert re.fullmatch(r'\d+\.\d+\.\d+', portable['version']), 'Version must be SemVer'
    for manifest in (claude, codex):
        for key in ('name', 'version', 'description', 'author', 'repository', 'license'):
            assert manifest[key] == portable[key], f'Host metadata drift: {key}'
    interface = portable['extensions']['com.openai']['interface']
    assert codex['interface'] == interface, 'Codex presentation metadata drift'
    assert 0 < len(interface['shortDescription']) <= 30, 'Plugin subtitle exceeds 30 characters'
    assert codex['skills'] == './skills/', 'Codex skill path must use shared skills directory'

    for host_path in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
        catalog = json.loads((root / host_path).read_text(encoding='utf-8'))
        assert catalog['name'] == PLUGIN_NAME and len(catalog['plugins']) == 1, 'Unexpected catalog identity or count'
        entry = catalog['plugins'][0]
        assert entry['name'] == PLUGIN_NAME, 'Catalog/plugin identity mismatch'
        source = entry['source']
        rel = source if isinstance(source, str) else source['path']
        assert rel.startswith('./'), 'Catalog path must be relative'
        resolved = (root / rel).resolve()
        assert resolved.is_relative_to(root), 'Catalog path escapes repository'
        assert resolved == plugin, 'Catalog does not point to canonical plugin'
        if isinstance(source, dict):
            assert source['source'] == 'local', 'Unsupported local source type'
            assert entry['policy'] == {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'Incomplete install policy'
            assert entry['category'] == 'Productivity', 'Unexpected marketplace category'
        else:
            assert catalog['owner']['name'] == 'ajitta', 'Missing marketplace owner'
            assert entry['version'] == portable['version'], 'Catalog version drift'

    skill_files = list((plugin / 'skills').glob('*/SKILL.md'))
    assert len(skill_files) == 1, 'Exactly one shared skill is expected'
    skill = skill_files[0]
    text = skill.read_text(encoding='utf-8')
    match = re.fullmatch(r'---\n([\s\S]*?)\n---\n([\s\S]*)', text)
    assert match, 'Missing YAML frontmatter'
    header = yaml.safe_load(match.group(1))
    assert header['name'] == skill.parent.name == 'coding-guidelines', 'Skill identity mismatch'
    assert isinstance(header['description'], str) and header['description'], 'Missing skill description'
    assert header['metadata']['version'] == portable['version'], 'Skill/plugin version drift'
    provenance = json.loads((root / 'docs/provenance.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(match.group(2).encode()).hexdigest() == provenance['reviewed_body_sha256'], 'Reviewed body changed; update its review and provenance'
    ui = yaml.safe_load((skill.parent / 'agents/openai.yaml').read_text(encoding='utf-8'))
    assert 25 <= len(ui['interface']['short_description']) <= 64, 'Invalid skill subtitle length'
    assert '$karpathy-regula:coding-guidelines' in ui['interface']['default_prompt'], 'Wrong default invocation'
    assert (plugin / 'LICENSE').read_bytes() == (root / 'LICENSE').read_bytes(), 'License copy drift'
    assert (plugin / 'NOTICE.md').is_file(), 'Attribution missing'
    for file in plugin.rglob('*'):
        assert not file.is_symlink(), f'Symlink is not allowed: {file}'
        if file.is_file():
            assert b'\r' not in file.read_bytes(), f'Use LF line endings: {file}'
    return plugin, portable['version']


def package(root=ROOT):
    plugin, version = validate(root)
    out = Path(root) / 'dist' / f'{PLUGIN_NAME}-{version}.zip'
    out.parent.mkdir(exist_ok=True)
    files = sorted(p for p in plugin.rglob('*') if p.is_file())
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, Path(PLUGIN_NAME) / file.relative_to(plugin))
    with zipfile.ZipFile(out) as archive:
        assert len(archive.namelist()) == len(files), 'Archive omitted files'
        assert archive.testzip() is None, 'Archive integrity check failed'
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        validate()
        print('Shared skill, host manifests, catalogs, YAML, provenance and license: OK')
    else:
        print(package())
