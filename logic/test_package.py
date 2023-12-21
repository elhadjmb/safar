import unittest
from unittest.mock import patch, MagicMock
from . import Config
from . import Player

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Mock Screen, Video, and Sequence objects
        self.mock_screen = MagicMock()
        self.mock_video = MagicMock()
        self.mock_sequence = MagicMock()

    @patch('config.json.dump')
    @patch('builtins.open')
    def test_save(self, mock_open, mock_json_dump):
        # Test save method
        config = Config([self.mock_screen], [self.mock_video], [self.mock_sequence])
        config.save("dummy_path.json")
        mock_json_dump.assert_called_once()
        mock_open.assert_called_with("dummy_path.json", 'w')

    @patch('config.json.load')
    @patch('builtins.open')
    def test_load(self, mock_open, mock_json_load):
        # Test load method
        mock_json_load.return_value = {
            "screens": [],
            "videos": [],
            "sequences": []
        }
        config = Config()
        config.load("dummy_path.json")
        mock_open.assert_called_with("dummy_path.json", 'r')
        self.assertEqual(len(config.screens), 0)
        self.assertEqual(len(config.videos), 0)
        self.assertEqual(len(config.sequences), 0)

class TestPlayer(unittest.TestCase):

    @patch('player.input', side_effect=['y', '0', 'done', 'path/to/video.mp4', '0', 'done', '0', '0', 'done'])
    @patch('player.os.path.exists', return_value=True)
    @patch('player.Screen.detect_monitors', return_value=[MagicMock()])
    def test_player_flow(self, mock_detect_monitors, mock_path_exists, mock_input):
        # Test the overall flow of setting up and saving configurations in the Player class
        player = Player()
        player.setup_screens()
        player.setup_videos()
        player.create_sequences()
        player.save_config("dummy_path.json")
        self.assertEqual(len(player.screens), 1)
        self.assertEqual(len(player.videos), 1)
        self.assertEqual(len(player.sequences), 1)

if __name__ == '__main__':
    unittest.main()
