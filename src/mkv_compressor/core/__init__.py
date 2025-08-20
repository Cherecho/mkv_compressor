"""
Core module initialization.
"""

from .compressor import (
    VideoCompressor,
    CompressionSettings,
    VideoInfo,
    CompressionProgress,
)

__all__ = ["VideoCompressor", "CompressionSettings", "VideoInfo", "CompressionProgress"]
