"""
Unit tests for the core compression functionality.
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mkv_compressor.core import VideoCompressor, CompressionSettings, VideoInfo
from mkv_compressor.utils import ConfigManager


class TestCompressionSettings(unittest.TestCase):
    """Test compression settings functionality."""
    
    def test_default_settings(self):
        """Test default compression settings."""
        settings = CompressionSettings()
        
        self.assertEqual(settings.video_codec, "libx264")
        self.assertEqual(settings.crf, 23)
        self.assertEqual(settings.preset, "medium")
        self.assertEqual(settings.audio_codec, "aac")
        self.assertEqual(settings.audio_bitrate, "128k")
        self.assertFalse(settings.two_pass)
    
    def test_custom_settings(self):
        """Test custom compression settings."""
        settings = CompressionSettings(
            crf=20,
            preset="slow",
            audio_bitrate="192k",
            two_pass=True
        )
        
        self.assertEqual(settings.crf, 20)
        self.assertEqual(settings.preset, "slow")
        self.assertEqual(settings.audio_bitrate, "192k")
        self.assertTrue(settings.two_pass)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        settings = CompressionSettings(crf=25, preset="fast")
        settings_dict = settings.to_dict()
        
        self.assertIsInstance(settings_dict, dict)
        self.assertEqual(settings_dict['crf'], 25)
        self.assertEqual(settings_dict['preset'], "fast")
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'crf': 20,
            'preset': 'slow',
            'audio_bitrate': '192k'
        }
        
        settings = CompressionSettings.from_dict(data)
        
        self.assertEqual(settings.crf, 20)
        self.assertEqual(settings.preset, 'slow')
        self.assertEqual(settings.audio_bitrate, '192k')


class TestVideoInfo(unittest.TestCase):
    """Test video information functionality."""
    
    def test_video_info_creation(self):
        """Test video info creation."""
        info = VideoInfo(
            filename="test.mp4",
            duration=120.5,
            width=1920,
            height=1080,
            fps=30.0,
            file_size=1024 * 1024 * 100,  # 100MB
            video_codec="h264",
            audio_codec="aac",
            bitrate=2000000
        )
        
        self.assertEqual(info.filename, "test.mp4")
        self.assertEqual(info.duration, 120.5)
        self.assertEqual(info.width, 1920)
        self.assertEqual(info.height, 1080)
        self.assertEqual(info.fps, 30.0)
        self.assertEqual(info.file_size, 1024 * 1024 * 100)
    
    def test_size_mb_property(self):
        """Test size in megabytes property."""
        info = VideoInfo(
            filename="test.mp4",
            duration=60,
            width=1280,
            height=720,
            fps=25.0,
            file_size=50 * 1024 * 1024,  # 50MB
            video_codec="h264",
            audio_codec="aac",
            bitrate=1500000
        )
        
        self.assertAlmostEqual(info.size_mb, 50.0, places=1)
    
    def test_resolution_property(self):
        """Test resolution string property."""
        info = VideoInfo(
            filename="test.mp4",
            duration=60,
            width=1920,
            height=1080,
            fps=30.0,
            file_size=1024,
            video_codec="h264",
            audio_codec="aac",
            bitrate=2000000
        )
        
        self.assertEqual(info.resolution, "1920x1080")


class TestVideoCompressor(unittest.TestCase):
    """Test video compressor functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('subprocess.run')
    def test_ffmpeg_verification(self, mock_run):
        """Test FFmpeg verification."""
        # Mock successful FFmpeg verification
        mock_run.return_value = Mock(returncode=0)
        
        # Should not raise exception
        compressor = VideoCompressor()
        
        # Verify subprocess was called
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertIn('ffmpeg', args[0])
        self.assertIn('-version', args)
    
    @patch('subprocess.run')
    def test_ffmpeg_verification_failure(self, mock_run):
        """Test FFmpeg verification failure."""
        # Mock failed FFmpeg verification
        mock_run.return_value = Mock(returncode=1)
        
        with self.assertRaises(RuntimeError):
            VideoCompressor()
    
    def test_compression_presets(self):
        """Test compression presets."""
        with patch('subprocess.run', return_value=Mock(returncode=0)):
            compressor = VideoCompressor()
            presets = compressor.get_compression_presets()
            
            self.assertIsInstance(presets, dict)
            self.assertIn("High Quality", presets)
            self.assertIn("Balanced", presets)
            self.assertIn("Small Size", presets)
            
            # Test preset structure
            balanced = presets["Balanced"]
            self.assertIsInstance(balanced, CompressionSettings)
            self.assertEqual(balanced.crf, 23)
    
    @patch('ffmpeg.probe')
    def test_get_video_info(self, mock_probe):
        """Test getting video information."""
        # Mock ffmpeg probe response
        mock_probe.return_value = {
            'format': {
                'duration': '120.5',
                'size': str(100 * 1024 * 1024),  # 100MB
                'bit_rate': '2000000'
            },
            'streams': [
                {
                    'codec_type': 'video',
                    'width': 1920,
                    'height': 1080,
                    'r_frame_rate': '30/1',
                    'codec_name': 'h264'
                },
                {
                    'codec_type': 'audio',
                    'codec_name': 'aac'
                }
            ]
        }
        
        with patch('subprocess.run', return_value=Mock(returncode=0)):
            compressor = VideoCompressor()
            info = compressor.get_video_info("test.mp4")
            
            self.assertIsInstance(info, VideoInfo)
            self.assertEqual(info.duration, 120.5)
            self.assertEqual(info.width, 1920)
            self.assertEqual(info.height, 1080)
            self.assertEqual(info.fps, 30.0)
            self.assertEqual(info.video_codec, 'h264')
            self.assertEqual(info.audio_codec, 'aac')


class TestConfigManager(unittest.TestCase):
    """Test configuration manager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_default_settings(self):
        """Test default configuration settings."""
        config = ConfigManager(self.config_file)
        defaults = config.get_default_settings()
        
        self.assertIsInstance(defaults, dict)
        self.assertIn('ffmpeg_path', defaults)
        self.assertIn('default_output_dir', defaults)
        self.assertIn('overwrite_files', defaults)
    
    def test_get_set_settings(self):
        """Test getting and setting configuration values."""
        config = ConfigManager(self.config_file)
        
        # Test setting and getting simple value
        config.set('test_key', 'test_value')
        self.assertEqual(config.get('test_key'), 'test_value')
        
        # Test nested key
        config.set('nested.key', 'nested_value')
        self.assertEqual(config.get('nested.key'), 'nested_value')
        
        # Test default value
        self.assertEqual(config.get('nonexistent', 'default'), 'default')
    
    def test_save_load_config(self):
        """Test saving and loading configuration."""
        config1 = ConfigManager(self.config_file)
        config1.set('test_setting', 'test_value')
        config1.save()
        
        # Create new instance and load
        config2 = ConfigManager(self.config_file)
        self.assertEqual(config2.get('test_setting'), 'test_value')
    
    def test_recent_directories(self):
        """Test recent directories functionality."""
        config = ConfigManager(self.config_file)
        
        # Add recent input directory
        config.add_recent_directory('/path/to/input', 'input')
        recent_input = config.get_recent_directories('input')
        
        self.assertIn('/path/to/input', recent_input)
        
        # Add another directory
        config.add_recent_directory('/another/path', 'input')
        recent_input = config.get_recent_directories('input')
        
        # Should be at the front
        self.assertEqual(recent_input[0], '/another/path')
    
    def test_custom_presets(self):
        """Test custom presets functionality."""
        config = ConfigManager(self.config_file)
        
        preset_settings = {
            'crf': 20,
            'preset': 'slow',
            'audio_bitrate': '192k'
        }
        
        config.save_custom_preset('My Custom Preset', preset_settings)
        custom_presets = config.get_custom_presets()
        
        self.assertIn('My Custom Preset', custom_presets)
        self.assertEqual(custom_presets['My Custom Preset'], preset_settings)
        
        # Test deletion
        config.delete_custom_preset('My Custom Preset')
        custom_presets = config.get_custom_presets()
        self.assertNotIn('My Custom Preset', custom_presets)


if __name__ == '__main__':
    unittest.main()