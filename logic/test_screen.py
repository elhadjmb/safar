import unittest
from unittest.mock import patch, Mock
from screen import Screen


class TestScreen(unittest.TestCase):

    def setUp(self):
        # Mock data for monitors
        self.mock_monitors = [
            Mock(width=1920, height=1080, x=0, y=0, name='Monitor1'),
            Mock(width=1280, height=720, x=1920, y=0, name='Monitor2')
        ]

    @patch('screen.get_monitors')
    def test_screen_initialization(self, mock_get_monitors):
        # Setup the mock
        mock_get_monitors.return_value = self.mock_monitors

        # Test initialization
        screen = Screen(select_index=0)
        self.assertEqual(screen.select_index, 0)
        self.assertEqual(screen.width, 1920)
        self.assertEqual(screen.height, 1080)
        self.assertEqual(screen.x, 0)
        self.assertEqual(screen.y, 0)
        self.assertEqual(screen.name, 'Monitor1')

    @patch('screen.get_monitors')
    def test_screen_initialization_out_of_range(self, mock_get_monitors):
        # Setup the mock
        mock_get_monitors.return_value = self.mock_monitors

        # Test initialization with out of range index
        with self.assertRaises(ValueError):
            Screen(select_index=len(self.mock_monitors))

    @patch('screen.get_monitors')
    def test_detect_monitors(self, mock_get_monitors):
        # Setup the mock
        mock_get_monitors.return_value = self.mock_monitors

        # Test detect_monitors
        screens = Screen.detect_monitors()
        self.assertEqual(len(screens), 2)
        self.assertIsInstance(screens[0], Screen)
        self.assertIsInstance(screens[1], Screen)


if __name__ == '__main__':
    unittest.main()
