"""Regression checks for the public documentation boundary."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class PublicScopeTests(unittest.TestCase):
    def check_files(self, files, rejected):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in files:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Example content")
            with patch.object(validate, "ROOT", root):
                if rejected:
                    with self.assertRaises(validate.ValidationError):
                        validate.validate_public_scope()
                else:
                    validate.validate_public_scope()

    def test_public_guides_allowed(self):
        self.check_files(["README.md", "docs/client-verification.md"], False)

    def test_research_document_rejected(self):
        self.check_files(["docs/vendor-research.md"], True)

    def test_nested_report_rejected(self):
        self.check_files(["docs/reviews/report.txt"], True)

    def test_root_report_rejected(self):
        self.check_files(["internal-review.md"], True)


if __name__ == "__main__":
    unittest.main()
