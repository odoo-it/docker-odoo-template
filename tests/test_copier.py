from unittest import TestCase
from pathlib import Path
from tempfile import TemporaryDirectory
from copier.main import run_copy


class TemporaryDirectoryCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.directory = TemporaryDirectory()
        cls.path = Path(cls.directory.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.directory.cleanup()
        return super().tearDownClass()


class TestCopier(TemporaryDirectoryCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.answers = dict(
            odoo_version=17.0,
            project_slug="my-project",
            project_name="My Project",
        )
        cls.template_path = Path(__file__).parent.parent
        # Initialize the template
        run_copy(
            src_path=str(cls.template_path),
            dst_path=cls.path,
            data=cls.answers,
            vcs_ref="HEAD",
        )

    def test_copied_files(self):
        self.assertTrue((self.path / "README.md").is_file())
        self.assertTrue((self.path / "requirements.txt").is_file())
        self.assertTrue((self.path / "Dockerfile").is_file())
