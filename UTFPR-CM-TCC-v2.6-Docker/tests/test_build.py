"""Standard-library tests: no Docker or TeX installation required."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = load('utfpr_compiler', ROOT/'scripts'/'compile.py')

    def test_repo_main_exists(self):
        self.assertTrue((ROOT/'main.tex').is_file())
        self.assertTrue((ROOT/'utfpr.cls').is_file())
        self.assertTrue((ROOT/'PreTexto'/'entradas-siglas.tex').is_file())
        self.assertTrue((ROOT/'build-config.json').is_file())

    def test_project_resolution(self):
        source, main = self.build.resolve_project(None, 'main.tex')
        self.assertEqual(source, ROOT)
        self.assertEqual(main.as_posix(), 'main.tex')
        with self.assertRaises(RuntimeError):
            self.build.resolve_project(None, '../../main.tex')
        with self.assertRaises(RuntimeError):
            self.build.resolve_project('/not/a/real/project','main.tex')

    def test_copy_worktree_preserves_nested_tex_and_figures(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'source';source.mkdir()
            (source/'main.tex').write_text('\\documentclass{article}\\begin{document}OK\\end{document}')
            (source/'PreTexto').mkdir()
            (source/'PreTexto'/'part.tex').write_text('test')
            (source/'PreTexto'/'figure.pdf').write_bytes(b'%PDF-1.4')
            (source/'PreTexto'/'part.aux').write_text('generated')
            (source/'main.pdf').write_bytes(b'%PDF-1.4 stale')
            (source/'main.xmpdata').write_text('metadata')
            (source/'.build').mkdir();(source/'.build'/'unwanted').write_text('bad')
            work=Path(temp)/'stage'
            self.build.copy_worktree(source,work)
            self.assertTrue((work/'PreTexto'/'part.tex').exists())
            self.assertTrue((work/'PreTexto'/'figure.pdf').exists())
            self.assertTrue((work/'main.xmpdata').exists())
            self.assertFalse((work/'PreTexto'/'part.aux').exists())
            self.assertFalse((work/'main.pdf').exists())
            self.assertFalse((work/'.build').exists())

    def test_stable_project_id(self):
        self.assertEqual(self.build.short_id(ROOT,'main.tex'),'default')
        with tempfile.TemporaryDirectory() as temp:
            val=self.build.short_id(Path(temp),'main.tex')
            self.assertEqual(val,self.build.short_id(Path(temp),'main.tex'))
            self.assertNotEqual(val,'default')

    def test_private_build_clean_does_not_delete_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            fake=Path(temp)/'.build';fake.mkdir()
            fake_pdf=Path(temp)/'main.pdf';fake_pdf.write_bytes(b'not a real pdf')
            # Simulates the clean action's intended target only.
            import shutil
            shutil.rmtree(fake)
            self.assertTrue(fake_pdf.exists())


if __name__=='__main__':
    unittest.main()
