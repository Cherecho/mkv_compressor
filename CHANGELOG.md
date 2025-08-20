# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-20

### Added
- Initial release of MKV Video Compressor
- Core video compression functionality using FFmpeg
- Graphical user interface (GUI) with tkinter
- Command-line interface (CLI) for batch processing
- Multiple compression presets (High Quality, Balanced, Small Size, Mobile, Web Optimized)
- Drag and drop support in GUI
- Real-time progress monitoring with speed and ETA
- Batch processing capabilities
- Configuration management system
- Comprehensive logging system
- Error handling and recovery
- Cross-platform support (Windows, macOS, Linux)
- Unit tests and integration tests
- Complete documentation (README, User Guide, API Reference)
- Professional project structure
- Setup and packaging scripts

### Features
- **Video Compression**: High-quality MKV compression using FFmpeg
- **Multiple Interfaces**: Both GUI and CLI for different use cases
- **Preset System**: Pre-configured settings for various quality/size needs
- **Custom Settings**: Fine-tune compression parameters
- **Progress Tracking**: Real-time progress with visual feedback
- **Batch Processing**: Compress multiple files simultaneously
- **Settings Management**: Save and load user preferences
- **File Management**: Smart output naming and directory handling
- **Error Recovery**: Robust error handling and logging
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Technical Details
- **Python Version**: Requires Python 3.8 or higher
- **Dependencies**: FFmpeg, ffmpeg-python, tkinter, psutil, tqdm, pydantic
- **Output Format**: MKV (Matroska Video) container
- **Input Formats**: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V, and more
- **Video Codecs**: H.264 (libx264), H.265 (libx265), VP9 (libvpx-vp9)
- **Audio Codecs**: AAC, MP3, Vorbis, with bitrate options

### Installation Methods
- Source installation with virtual environment
- Pip installation (when available on PyPI)
- Standalone executable (future release)

### Documentation
- Comprehensive README with quick start guide
- Detailed user guide with examples
- Complete API reference documentation
- Troubleshooting guide
- Development setup instructions

### Testing
- Unit tests for core functionality
- Integration tests for compression workflows
- Mocked tests for external dependencies
- Continuous integration setup ready

### Project Structure
```
mkv_compressor/
├── src/mkv_compressor/     # Main source code
│   ├── core/               # Core compression logic
│   ├── gui/                # GUI interface
│   ├── utils/              # Utility functions
│   └── cli.py              # Command-line interface
├── tests/                  # Test suite
├── docs/                   # Documentation
├── config/                 # Configuration files
├── scripts/                # Build and utility scripts
└── requirements.txt        # Dependencies
```

## [Unreleased]

### Planned Features
- Hardware acceleration support (NVENC, Quick Sync)
- Additional video codecs (AV1)
- Video quality analysis tools
- Custom preset sharing
- Plugin system for extensions
- Advanced filtering options
- Subtitle processing
- Multi-language support
- Standalone executable builds
- Web interface option

### Known Issues
- Two-pass encoding progress reporting needs improvement
- Large file handling could be optimized
- Memory usage optimization for batch processing
- GUI responsiveness during long operations

### Future Improvements
- Better error messages and user guidance
- Performance optimizations
- Enhanced progress reporting
- Additional compression formats
- Cloud storage integration
- Automated quality testing