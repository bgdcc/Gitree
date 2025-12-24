import unittest
from pathlib import Path
import tempfile
import sys
import os
from unittest.mock import MagicMock, patch
from gitree.utilities.utils import copy_to_clipboard

# Adjust path to find gitree package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from gitree.services.draw_tree import draw_tree

class TestCopyToClipboard(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.test_dir.name)
        
        # Create a dummy structure
        # root/
        #   file1.txt
        #   file2.txt
        #   folder/
        #     file3.txt
        #     file4.txt
        
        (self.root / "file1.txt").touch()
        (self.root / "file2.txt").touch()
        (self.root / "folder").mkdir()
        (self.root / "folder" / "file3.txt").touch()
        (self.root / "folder" / "file4.txt").touch()

    def tearDown(self):
        self.test_dir.cleanup()

    @patch('gitree.utilities.utils.copy_to_clipboard')
    def test_copy_to_clipboard(self, mock_copy):
        mock_copy.return_value = None

        # Whitelist specific files
        whitelist = {
            str(self.root / "file1.txt"),
            str(self.root / "folder" / "file3.txt")
        }
        
        # Capture stdout
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        
        draw_tree(
            root=self.root,
            depth=None,
            show_all=False,
            extra_ignores=[],
            respect_gitignore=False,
            gitignore_depth=None,
            whitelist=whitelist
        )
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertTrue(copy_to_clipboard(output))
        mock_copy.assert_called_once()
        
if __name__ == '__main__':
    unittest.main()
