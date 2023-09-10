#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


from kcontext import initialize_colors, display_contexts, exit_gracefully

class TestKContext(unittest.TestCase):

    @patch('curses.start_color')
    @patch('curses.init_pair')
    def test_initialize_colors(self, mock_init_pair, mock_start_color):
        initialize_colors()
        mock_start_color.assert_called_once()
        mock_init_pair.assert_called_with(10, 10, 0)

    @patch('curses.endwin')
    @patch('builtins.exit')
    def test_exit_gracefully(self, mock_exit, mock_endwin):
        exit_gracefully()
        mock_endwin.assert_called_once()
        mock_exit.assert_called_with(0)

if __name__ == '__main__':
    unittest.main()
