import unittest
from pathlib import Path
import tempfile
import sys
import os
from io import StringIO

# Adjust path to find gitree package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from gitree.services.draw_tree import draw_tree

class TestDrawTreeDepth(unittest.TestCase):
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
        #     folder2/
        #       file5.txt
        #       file6.txt
        
        (self.root / "file1.txt").touch()
        (self.root / "file2.txt").touch()
        (self.root / "folder1").mkdir()
        (self.root / "folder1" / "file3.txt").touch()
        (self.root / "folder1" / "file4.txt").touch()
        (self.root / "folder1" / "folder2").mkdir()
        (self.root / "folder1" / "folder2" / "file5.txt").touch()
        (self.root / "folder1" / "folder2" / "file6.txt").touch()

    def tearDown(self):
        self.test_dir.cleanup()

    def test_draw_tree_depth(self):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        draw_tree(
            root=self.root,
            depth=2,
            show_all=False,
            extra_ignores=[],
            respect_gitignore=False,
            gitignore_depth=None,
            whitelist=None
        )
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("file1.txt", output)
        self.assertIn("file3.txt", output)
        self.assertIn("folder2", output)
        self.assertNotIn("file5.txt", output)

if __name__ == '__main__':
    unittest.main()
