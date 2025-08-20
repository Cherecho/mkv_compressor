"""
Tests for utility functions.
"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mkv_compressor.utils import (
    format_file_size, format_duration, is_video_file,
    sanitize_filename, get_unique_filename, find_ffmpeg,
    validate_ffmpeg, estimate_output_size
)


class TestHelperFunctions(unittest.TestCase):
    """Test utility helper functions."""
    
    def test_format_file_size(self):
        """Test file size formatting."""
        self.assertEqual(format_file_size(0), "0 B")
        self.assertEqual(format_file_size(512), "512.0 B")
        self.assertEqual(format_file_size(1024), "1.0 KB")
        self.assertEqual(format_file_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_file_size(1024 * 1024 * 1024), "1.0 GB")
        self.assertEqual(format_file_size(1536), "1.5 KB")  # 1.5 KB
    
    def test_format_duration(self):
        """Test duration formatting."""
        self.assertEqual(format_duration(0), "00:00")
        self.assertEqual(format_duration(30), "00:30")
        self.assertEqual(format_duration(90), "01:30")
        self.assertEqual(format_duration(3661), "01:01:01")  # 1 hour, 1 minute, 1 second
        self.assertEqual(format_duration(7200), "02:00:00")  # 2 hours
    
    def test_is_video_file(self):
        """Test video file detection."""
        self.assertTrue(is_video_file("movie.mp4"))
        self.assertTrue(is_video_file("video.avi"))
        self.assertTrue(is_video_file("clip.MOV"))  # Case insensitive
        self.assertTrue(is_video_file("file.mkv"))
        self.assertTrue(is_video_file("test.webm"))
        
        self.assertFalse(is_video_file("audio.mp3"))
        self.assertFalse(is_video_file("document.pdf"))
        self.assertFalse(is_video_file("image.jpg"))
        self.assertFalse(is_video_file("text.txt"))
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        self.assertEqual(sanitize_filename("normal_file.mp4"), "normal_file.mp4")
        self.assertEqual(sanitize_filename("file<with>bad:chars.mp4"), "file_with_bad_chars.mp4")
        self.assertEqual(sanitize_filename("file/with\\slashes.mp4"), "file_with_slashes.mp4")
        self.assertEqual(sanitize_filename("file|with?other*chars.mp4"), "file_with_other_chars.mp4")
        self.assertEqual(sanitize_filename("  spaced file  "), "spaced file")
        self.assertEqual(sanitize_filename(""), "unnamed")
    
    def test_get_unique_filename(self):
        """Test unique filename generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, 'w') as f:
                f.write("test")
            
            # Test with non-existing file
            non_existing = os.path.join(temp_dir, "new_file.txt")
            self.assertEqual(get_unique_filename(non_existing), non_existing)
            
            # Test with existing file
            unique_name = get_unique_filename(test_file)
            expected = os.path.join(temp_dir, "test_1.txt")
            self.assertEqual(unique_name, expected)
    
    def test_estimate_output_size(self):
        """Test output size estimation."""
        input_size = 100 * 1024 * 1024  # 100MB
        
        # High quality (CRF 18)
        high_quality = estimate_output_size(input_size, 18)
        self.assertGreater(high_quality, input_size * 0.7)  # Should be larger
        
        # Balanced (CRF 23)
        balanced = estimate_output_size(input_size, 23)
        self.assertGreater(balanced, input_size * 0.5)
        self.assertLess(balanced, input_size * 0.7)
        
        # Small size (CRF 28)
        small = estimate_output_size(input_size, 28)
        self.assertLess(small, balanced)
        
        # Test with scale factor
        scaled = estimate_output_size(input_size, 23, scale_factor=0.5)
        self.assertLess(scaled, balanced)  # Should be smaller due to resolution scaling
    
    @patch('shutil.which')
    def test_find_ffmpeg(self, mock_which):
        """Test FFmpeg discovery."""
        # Test when ffmpeg is in PATH
        mock_which.return_value = "/usr/bin/ffmpeg"
        result = find_ffmpeg()
        self.assertEqual(result, "/usr/bin/ffmpeg")
        
        # Test when ffmpeg is not in PATH
        mock_which.return_value = None
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = False
            result = find_ffmpeg()
            self.assertIsNone(result)
    
    @patch('subprocess.run')
    def test_validate_ffmpeg(self, mock_run):
        """Test FFmpeg validation."""
        # Test successful validation
        mock_run.return_value = Mock(
            returncode=0,
            stdout="ffmpeg version 4.4.0"
        )
        
        is_valid, message = validate_ffmpeg("/usr/bin/ffmpeg")
        self.assertTrue(is_valid)
        self.assertIn("ffmpeg version", message)
        
        # Test failed validation
        mock_run.return_value = Mock(returncode=1)
        
        is_valid, message = validate_ffmpeg("/usr/bin/ffmpeg")
        self.assertFalse(is_valid)
        self.assertIn("error", message.lower())


class TestConfigurationFunctions(unittest.TestCase):
    """Test configuration-related functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()