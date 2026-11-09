import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = 'karpathy-regula'
PLUGIN_REL = Path('plugins') / PLUGIN_NAME
# Fixed entry metadata so that rebuilding a tag reproduces the released archive byte for byte.
ZIP_DATE_TIME = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = 0o100644


class PackageError(Exception):
    """A repository check failed."""


def check(condition, message):
    # Explicit raise rather than assert: `python -O` strips assert statements.
    if not condition:
        raise PackageError(message)


def validate(root=ROOT):
    root = Path(root).resolve()
    plugin = root / PLUGIN_REL
    portable = json.loads((plugin / 'plugin.json').read_text(encoding='utf-8'))
    claude = json.loads((plugin / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
    codex = json.loads((plugin / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    check(portable['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'Portable schema missing')
    check(portable['name'] == PLUGIN_NAME, 'Wrong plugin identity')
    check(re.fullmatch(r'\d+\.\d+\.\d+', portable['version']), 'Version must be SemVer')
    for manifest in (claude, codex):
        for key in ('name', 'version', 'description', 'author', 'repository', 'license'):
            check(manifest[key] == portable[key], f'Host metadata drift: {key}')
    interface = portable['extensions']['com.openai']['interface']
    check(codex['interface'] == interface, 'Codex presentation metadata drift')
    check(0 < len(interface['shortDescription']) <= 30, 'Plugin subtitle exceeds 30 characters')
    check(codex['skills'] == './skills/', 'Codex skill path must use shared skills directory')

    for host_path in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
        catalog = json.loads((root / host_path).read_text(encoding='utf-8'))
        check(catalog['name'] == PLUGIN_NAME and len(catalog['plugins']) == 1, 'Unexpected catalog identity or count')
        entry = catalog['plugins'][0]
        check(entry['name'] == PLUGIN_NAME, 'Catalog/plugin identity mismatch')
        source = entry['source']
        rel = source if isinstance(source, str) else source['path']
        check(rel.startswith('./'), 'Catalog path must be relative')
        resolved = (root / rel).resolve()
        check(resolved.is_relative_to(root), 'Catalog path escapes repository')
        check(resolved == plugin, 'Catalog does not point to canonical plugin')
        if isinstance(source, dict):
            check(source['source'] == 'local', 'Unsupported local source type')
            check(entry['policy'] == {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'Incomplete install policy')
            check(entry['category'] == 'Productivity', 'Unexpected marketplace category')
        else:
            check(catalog['owner']['name'] == 'ajitta', 'Missing marketplace owner')
            check(entry['version'] == portable['version'], 'Catalog version drift')

    skill_files = list((plugin / 'skills').glob('*/SKILL.md'))
    check(len(skill_files) == 1, 'Exactly one shared skill is expected')
    skill = skill_files[0]
    text = skill.read_text(encoding='utf-8')
    match = re.fullmatch(r'---\n([\s\S]*?)\n---\n([\s\S]*)', text)
    if match is None:
        raise PackageError('Missing YAML frontmatter')
    header = yaml.safe_load(match.group(1))
    check(header['name'] == skill.parent.name == 'coding-guidelines', 'Skill identity mismatch')
    check(isinstance(header['description'], str) and header['description'], 'Missing skill description')
    check(header['metadata']['version'] == portable['version'], 'Skill/plugin version drift')
    provenance = json.loads((root / 'docs/provenance.json').read_text(encoding='utf-8'))
    check(hashlib.sha256(match.group(2).encode()).hexdigest() == provenance['reviewed_body_sha256'],
          'Reviewed body changed; update its review and provenance')
    ui = yaml.safe_load((skill.parent / 'agents/openai.yaml').read_text(encoding='utf-8'))
    check(ui['interface']['display_name'] == interface['displayName'], 'Skill and plugin display names differ')
    check(25 <= len(ui['interface']['short_description']) <= 64, 'Invalid skill subtitle length')
    check('$karpathy-regula:coding-guidelines' in ui['interface']['default_prompt'], 'Wrong default invocation')
    check((plugin / 'LICENSE').read_bytes() == (root / 'LICENSE').read_bytes(), 'License copy drift')
    check((plugin / 'NOTICE.md').is_file(), 'Attribution missing')
    for file in plugin.rglob('*'):
        check(not file.is_symlink(), f'Symlink is not allowed: {file}')
        if file.is_file():
            check(b'\r' not in file.read_bytes(), f'Use LF line endings: {file}')
    return plugin, portable['version']


def package(root=ROOT):
    plugin, version = validate(root)
    out = Path(root) / 'dist' / f'{PLUGIN_NAME}-{version}.zip'
    out.parent.mkdir(exist_ok=True)
    files = sorted(p for p in plugin.rglob('*') if p.is_file())
    with zipfile.ZipFile(out, 'w') as archive:
        for file in files:
            name = str(PurePosixPath(PLUGIN_NAME, *file.relative_to(plugin).parts))
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE_TIME)
            info.create_system = 3  # Unix, so external_attr carries the file mode
            info.external_attr = ZIP_FILE_MODE << 16
            # Stored, not deflated: deflate output differs between zlib builds.
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, file.read_bytes())
    with zipfile.ZipFile(out) as archive:
        check(len(archive.namelist()) == len(files), 'Archive omitted files')
        check(archive.testzip() is None, 'Archive integrity check failed')
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        if args.check:
            validate()
            print('Shared skill, host manifests, catalogs, YAML, provenance and license: OK')
        else:
            print(package())
    except PackageError as error:
        print(f'error: {error}', file=sys.stderr)
        sys.exit(1)
