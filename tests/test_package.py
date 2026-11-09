import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package_tool', ROOT / 'tools/package.py')
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        assert self.root.is_relative_to(Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup)
        for name in ('.claude-plugin', '.agents', 'plugins', 'docs', 'tools'):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / 'LICENSE', self.root / 'LICENSE')

    def set_codex_version(self, version):
        file = self.root / 'plugins/karpathy-regula/.codex-plugin/plugin.json'
        metadata = json.loads(file.read_text(encoding='utf-8'))
        metadata['version'] = version
        file.write_text(json.dumps(metadata), encoding='utf-8')

    def test_archive_contains_one_shared_skill_and_hidden_manifests(self):
        archive_path = tool.package(self.root)
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            self.assertEqual(sum(n.endswith('/SKILL.md') for n in names), 1)
            self.assertIn('karpathy-regula/.claude-plugin/plugin.json', names)
            self.assertIn('karpathy-regula/.codex-plugin/plugin.json', names)
            self.assertIn('karpathy-regula/LICENSE', names)
            self.assertIn('karpathy-regula/NOTICE.md', names)
            self.assertFalse(any('marketplace.json' in n for n in names))

    def test_archive_order_is_posix_string_order(self):
        with zipfile.ZipFile(tool.package(self.root)) as archive:
            names = archive.namelist()
        self.assertEqual(names, sorted(names))

    def test_unexpected_plugin_file_is_rejected(self):
        (self.root / 'plugins/karpathy-regula/skills/.DS_Store').write_bytes(b'x')
        with self.assertRaisesRegex(tool.PackageError, 'Unexpected plugin files'):
            tool.validate(self.root)

    def test_missing_key_reports_an_error_line(self):
        file = self.root / 'plugins/karpathy-regula/plugin.json'
        metadata = json.loads(file.read_text(encoding='utf-8'))
        del metadata['license']
        file.write_text(json.dumps(metadata), encoding='utf-8')
        result = subprocess.run([sys.executable, str(self.root / 'tools/package.py'), '--check'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("error: missing key 'license'", result.stderr)

    def test_archive_is_reproducible(self):
        first = tool.package(self.root).read_bytes()
        for file in (self.root / 'plugins').rglob('*'):
            os.utime(file, (1_900_000_000, 1_900_000_000))
        self.assertEqual(tool.package(self.root).read_bytes(), first)

    def test_host_version_drift_is_rejected(self):
        self.set_codex_version('9.9.9')
        with self.assertRaisesRegex(tool.PackageError, 'metadata drift'):
            tool.validate(self.root)

    def test_check_fails_under_optimized_python(self):
        self.set_codex_version('9.9.9')
        result = subprocess.run([sys.executable, '-O', str(self.root / 'tools/package.py'), '--check'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('metadata drift', result.stderr)

    def test_catalog_escape_is_rejected(self):
        file = self.root / '.agents/plugins/marketplace.json'
        metadata = json.loads(file.read_text(encoding='utf-8'))
        metadata['plugins'][0]['source']['path'] = './../outside'
        file.write_text(json.dumps(metadata), encoding='utf-8')
        with self.assertRaisesRegex(tool.PackageError, 'escapes repository'):
            tool.validate(self.root)

    def test_unreviewed_body_edit_is_rejected(self):
        file = self.root / 'plugins/karpathy-regula/skills/coding-guidelines/SKILL.md'
        file.write_text(file.read_text(encoding='utf-8') + '\nNew unreviewed instruction.\n', encoding='utf-8')
        with self.assertRaisesRegex(tool.PackageError, 'Reviewed body changed'):
            tool.validate(self.root)


if __name__ == '__main__':
    unittest.main()
