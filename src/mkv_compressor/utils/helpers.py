"""
Utility functions and helpers for MKV Video Compressor.
"""

import os
import shutil
import tempfile
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import psutil


def get_file_hash(filepath: str, algorithm: str = "md5") -> str:
    """
    Calculate hash of a file.

    Args:
        filepath: Path to the file
        algorithm: Hash algorithm (md5, sha1, sha256)

    Returns:
        Hexadecimal hash string
    """
    hash_obj = hashlib.new(algorithm)

    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0

    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (HH:MM:SS)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def get_available_disk_space(path: str) -> int:
    """
    Get available disk space for a given path.

    Args:
        path: Directory path

    Returns:
        Available space in bytes
    """
    if os.name == "nt":  # Windows
        import ctypes

        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(path), ctypes.pointer(free_bytes), None, None
        )
        return free_bytes.value
    else:  # Unix/Linux/macOS
        statvfs = os.statvfs(path)
        return statvfs.f_frsize * statvfs.f_bavail


def check_disk_space(output_path: str, required_space: int) -> bool:
    """
    Check if there's enough disk space for the output file.

    Args:
        output_path: Output file path
        required_space: Required space in bytes

    Returns:
        True if enough space available
    """
    try:
        output_dir = os.path.dirname(output_path)
        available_space = get_available_disk_space(output_dir)
        return available_space > required_space
    except Exception:
        return True  # Assume space is available if check fails


def estimate_output_size(input_size: int, crf: int, scale_factor: float = 1.0) -> int:
    """
    Estimate output file size based on input size and compression settings.

    Args:
        input_size: Input file size in bytes
        crf: Constant Rate Factor (0-51)
        scale_factor: Resolution scale factor (1.0 = same resolution)

    Returns:
        Estimated output size in bytes
    """
    # Very rough estimation based on CRF
    if crf <= 18:
        compression_ratio = 0.8  # High quality
    elif crf <= 23:
        compression_ratio = 0.6  # Balanced
    elif crf <= 28:
        compression_ratio = 0.4  # Small size
    else:
        compression_ratio = 0.3  # Very small

    # Adjust for resolution scaling
    size_factor = scale_factor * scale_factor  # Area scaling

    return int(input_size * compression_ratio * size_factor)


def find_ffmpeg() -> Optional[str]:
    """
    Find FFmpeg executable in system PATH or common locations.

    Returns:
        Path to FFmpeg executable or None if not found
    """
    # Check if ffmpeg is in PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path

    # Check common installation locations
    common_locations = []

    if os.name == "nt":  # Windows
        common_locations = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
            os.path.expanduser(r"~\Documents\ffmpeg\bin\ffmpeg.exe"),
        ]
    else:  # Unix/Linux/macOS
        common_locations = [
            "/usr/local/bin/ffmpeg",
            "/usr/bin/ffmpeg",
            "/opt/ffmpeg/bin/ffmpeg",
            os.path.expanduser("~/bin/ffmpeg"),
        ]

    for location in common_locations:
        if os.path.isfile(location):
            return location

    return None


def validate_ffmpeg(ffmpeg_path: str) -> Tuple[bool, str]:
    """
    Validate FFmpeg executable.

    Args:
        ffmpeg_path: Path to FFmpeg executable

    Returns:
        Tuple of (is_valid, version_or_error_message)
    """
    try:
        import subprocess

        result = subprocess.run(
            [ffmpeg_path, "-version"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            # Extract version from output
            lines = result.stdout.split("\n")
            version_line = lines[0] if lines else "Unknown version"
            return True, version_line
        else:
            return False, "FFmpeg returned error code"

    except subprocess.TimeoutExpired:
        return False, "FFmpeg validation timed out"
    except FileNotFoundError:
        return False, "FFmpeg executable not found"
    except Exception as e:
        return False, f"Validation error: {e}"


def get_system_info() -> Dict[str, str]:
    """
    Get system information for diagnostics.

    Returns:
        Dictionary with system information
    """
    try:
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "platform": os.name,
            "cpu_cores": str(cpu_count),
            "total_memory": format_file_size(memory.total),
            "available_memory": format_file_size(memory.available),
            "disk_total": format_file_size(disk.total),
            "disk_free": format_file_size(disk.free),
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        }
    except Exception:
        return {"error": "Unable to gather system information"}


def create_temp_directory(prefix: str = "mkv_compressor_") -> str:
    """
    Create a temporary directory.

    Args:
        prefix: Prefix for directory name

    Returns:
        Path to temporary directory
    """
    return tempfile.mkdtemp(prefix=prefix)


def cleanup_temp_directory(temp_dir: str):
    """
    Clean up temporary directory.

    Args:
        temp_dir: Path to temporary directory
    """
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass  # Ignore cleanup errors


def is_video_file(filepath: str) -> bool:
    """
    Check if file is a supported video file.

    Args:
        filepath: Path to file

    Returns:
        True if file is a supported video file
    """
    video_extensions = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
        ".3gp",
        ".ogv",
        ".ts",
        ".mts",
    }

    return Path(filepath).suffix.lower() in video_extensions


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Remove leading/trailing spaces and dots
    filename = filename.strip(" .")

    # Ensure filename is not empty
    if not filename:
        filename = "unnamed"

    return filename


def get_unique_filename(filepath: str) -> str:
    """
    Get a unique filename by adding a number suffix if file exists.

    Args:
        filepath: Desired file path

    Returns:
        Unique file path
    """
    path_obj = Path(filepath)

    if not path_obj.exists():
        return filepath

    counter = 1
    while True:
        new_name = f"{path_obj.stem}_{counter}{path_obj.suffix}"
        new_path = path_obj.parent / new_name

        if not new_path.exists():
            return str(new_path)

        counter += 1


def compare_video_quality(original_path: str, compressed_path: str) -> Dict[str, float]:
    """
    Compare quality metrics between original and compressed video.
    Note: This is a placeholder - actual implementation would require
    additional dependencies like opencv-python for SSIM calculation.

    Args:
        original_path: Path to original video
        compressed_path: Path to compressed video

    Returns:
        Dictionary with quality metrics
    """
    try:
        original_size = os.path.getsize(original_path)
        compressed_size = os.path.getsize(compressed_path)

        compression_ratio = compressed_size / original_size
        space_saved = original_size - compressed_size
        space_saved_percent = (space_saved / original_size) * 100

        return {
            "compression_ratio": compression_ratio,
            "space_saved_bytes": space_saved,
            "space_saved_percent": space_saved_percent,
            "original_size": original_size,
            "compressed_size": compressed_size,
        }

    except Exception:
        return {}


class FileWatcher:
    """Simple file watcher for monitoring file changes."""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.last_modified = None
        self.last_size = None
        self._update_stats()

    def _update_stats(self):
        """Update file statistics."""
        try:
            if self.filepath.exists():
                stat = self.filepath.stat()
                self.last_modified = stat.st_mtime
                self.last_size = stat.st_size
        except Exception:
            self.last_modified = None
            self.last_size = None

    def has_changed(self) -> bool:
        """Check if file has changed since last check."""
        old_modified = self.last_modified
        old_size = self.last_size

        self._update_stats()

        return self.last_modified != old_modified or self.last_size != old_size

    def get_size(self) -> Optional[int]:
        """Get current file size."""
        return self.last_size
