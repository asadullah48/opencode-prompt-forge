import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InstallerTests(unittest.TestCase):
    def test_install_copies_exact_package_and_preserves_config(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / '.opencode'
            target.mkdir()
            config = target / 'opencode.json'
            config.write_text('preserve')
            paths = module.install(target)
            self.assertEqual(len(paths), 4)
            for path in paths:
                self.assertEqual((target / path).read_bytes(), (module.ROOT / '.opencode' / path).read_bytes())
            self.assertEqual(config.read_text(), 'preserve')

    def test_collision_does_not_partially_install(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            existing = target / 'skills/prompt-forge/SKILL.md'
            existing.parent.mkdir(parents=True)
            existing.write_text('custom')
            with self.assertRaises(FileExistsError):
                module.install(target)
            self.assertEqual(existing.read_text(), 'custom')
            self.assertFalse((target / 'commands').exists())

    def test_force_replaces_package_only(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            module.install(target)
            unrelated = target / 'commands/custom.md'
            unrelated.write_text('keep')
            (target / 'commands/forge.md').write_text('old')
            module.install(target, force=True)
            self.assertEqual(unrelated.read_text(), 'keep')
            self.assertIn('$ARGUMENTS', (target / 'commands/forge.md').read_text())

    def test_file_parent_is_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            (target / 'skills').write_text('obstruction')
            with self.assertRaises(ValueError):
                module.install(target)
            self.assertFalse((target / 'commands').exists())

    def test_symlink_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            outside = Path(temp) / 'outside'
            outside.mkdir()
            target = Path(temp) / 'target'
            try:
                target.symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('Symlink creation unavailable on this platform')
            with self.assertRaises(ValueError):
                module.install(target)
            self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
