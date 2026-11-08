import importlib.util
import json
from pathlib import Path
import shutil
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
        for name in ('.claude-plugin', '.agents', 'plugins', 'docs'):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / 'LICENSE', self.root / 'LICENSE')

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

    def test_host_version_drift_is_rejected(self):
        file = self.root / 'plugins/karpathy-regula/.codex-plugin/plugin.json'
        metadata = json.loads(file.read_text())
        metadata['version'] = '9.9.9'
        file.write_text(json.dumps(metadata))
        with self.assertRaisesRegex(AssertionError, 'metadata drift'):
            tool.validate(self.root)

    def test_catalog_escape_is_rejected(self):
        file = self.root / '.agents/plugins/marketplace.json'
        metadata = json.loads(file.read_text())
        metadata['plugins'][0]['source']['path'] = './../outside'
        file.write_text(json.dumps(metadata))
        with self.assertRaisesRegex(AssertionError, 'escapes repository'):
            tool.validate(self.root)

    def test_unreviewed_body_edit_is_rejected(self):
        file = self.root / 'plugins/karpathy-regula/skills/coding-guidelines/SKILL.md'
        file.write_text(file.read_text(encoding='utf-8') + '\nNew unreviewed instruction.\n', encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'Reviewed body changed'):
            tool.validate(self.root)


if __name__ == '__main__':
    unittest.main()
