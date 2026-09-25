"""Behavioral regression checks: python -m unittest discover -s scripts -v"""
from pathlib import Path
import tempfile
import unittest
import zipfile

from PIL import Image

import package
import validate


class RepositoryToolsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def skill_fixture(self):
        self.write("LICENSE", "MIT License\nCopyright Example\n")
        self.write("skills/feature-ideas/SKILL.md", "---\nname: feature-ideas\nlicense: MIT\ndescription: Propose useful illustrated features for a project.\n---\n# Feature Ideas\n")
        self.write("skills/feature-ideas/agents/openai.yaml", "interface:\n  display_name: Illustrated Feature Ideas\n  short_description: Discover features with detailed illustrations\n  default_prompt: Use $feature-ideas to propose seven illustrated project features.\n")

    def test_broken_relative_link_reports_failure_but_valid_link_passes(self):
        readme = self.write("docs/README.md", "[Guide](guide.md)\n")
        self.assertTrue(validate.validate_markdown(self.root, readme))
        self.write("docs/guide.md", "# Guide\n")
        self.assertEqual([], validate.validate_markdown(self.root, readme))

    def test_bad_frontmatter_is_reported_without_crashing(self):
        self.skill_fixture()
        self.assertEqual([], validate.validate_skill(self.root))
        self.write("skills/feature-ideas/SKILL.md", "---\nname: [broken\n---\n# Broken\n")
        self.assertTrue(validate.validate_skill(self.root))

    def test_corrupted_image_is_rejected_and_valid_png_decodes(self):
        path = self.root / "illustration.png"
        Image.new("RGB", (800, 450), "white").save(path)
        self.assertEqual([], validate.validate_png(path))
        path.write_bytes(b"\x89PNG\r\n\x1a\ncorrupted")
        self.assertTrue(validate.validate_png(path))

    def test_svg_script_and_remote_resource_are_rejected(self):
        path = self.write("diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')
        self.assertTrue(validate.validate_svg(path))
        self.write("diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/image.png"/></svg>')
        self.assertTrue(validate.validate_svg(path))
        self.write("diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"><path fill="url(#local)" d="M0 0"/></svg>')
        self.assertEqual([], validate.validate_svg(path))
        self.write("diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"><path style="fill:url(\'#local\')" d="M0 0"/></svg>')
        self.assertEqual([], validate.validate_svg(path))

    def test_machine_path_detection_does_not_confuse_https_or_generic_examples(self):
        self.assertIsNone(validate.LOCAL_PATH.search("https://example.com/guide"))
        self.assertIsNone(validate.LOCAL_PATH.search("C:/path/to/checkout"))
        private_path = "C:" + "/" + "Users" + "/" + "person" + "/secret.txt"
        self.assertIsNotNone(validate.LOCAL_PATH.search(private_path))

    def test_archive_is_reproducible_across_runs_and_checkout_newlines(self):
        self.skill_fixture()
        archive = package.build(self.root, self.root / "out-a")
        first = archive.read_bytes()
        skill = self.root / "skills/feature-ideas/SKILL.md"
        skill.write_bytes(skill.read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))
        other = package.build(self.root, self.root / "out-b")
        self.assertEqual(first, other.read_bytes())
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()), {"feature-ideas/LICENSE", "feature-ideas/SKILL.md", "feature-ideas/agents/openai.yaml"})
            self.assertEqual(bundle.read("feature-ideas/LICENSE"), b"MIT License\nCopyright Example\n")

    def test_references_and_image_alt_text_are_checked(self):
        self.write("image.png", "fixture")
        readme = self.write("README.md", "![Diagram][visual]\n\n[visual]: image.png\n")
        self.assertEqual([], validate.validate_markdown(self.root, readme))
        self.write("README.md", "![](image.png)\n")
        self.assertTrue(validate.validate_markdown(self.root, readme))


if __name__ == "__main__":
    unittest.main()
