

<div align="center">

<img src="assets/images/logo.png" alt="MKV Compressor Logo" width="300" />
<p align="center">
    <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/version-1.1.0-brightgreen.svg" alt="Version">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
    <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
    <br>
    <img src="https://img.shields.io/badge/GUI-tkinter-orange.svg" alt="GUI Framework">
    <img src="https://img.shields.io/badge/video-FFmpeg-red.svg" alt="Video Engine">
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <img src="https://img.shields.io/badge/status-active-success.svg" alt="Project Status: Active">
    <br>
    <img src="https://img.shields.io/badge/compression-H.264%20%7C%20H.265-blue.svg" alt="Codecs">
    <img src="https://img.shields.io/badge/format-MKV-purple.svg" alt="Output Format">
    <img src="https://img.shields.io/badge/interface-GUI%20%7C%20CLI-green.svg" alt="Interfaces">
    <img src="https://img.shields.io/badge/batch-processing-yellow.svg" alt="Batch Processing">
</p>

# MKV Video Compressor

</div>

A professional video compression tool for MKV files with both GUI and command-line interfaces.



## 🎥 Preview

<!-- Add your demo GIF here -->
![MKV Compressor Demo](assets/demo/app_preview.gif)

*Demo showing the compression process*

## Features

- **High-Quality Compression**: Uses FFmpeg for professional-grade video compression
- **Multiple Interfaces**: Both GUI and CLI for different use cases
- **Batch Processing**: Compress multiple files at once
- **Compression Presets**: Pre-configured settings for different quality/size needs
- **Custom Settings**: Fine-tune compression parameters
- **Progress Monitoring**: Real-time progress tracking with ETA
- **Drag & Drop**: Easy file selection in GUI mode
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **FFmpeg** - Must be installed and available in system PATH
   - Windows: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent

### Install from Source

```bash
# Clone the repository
git clone https://github.com/your-username/mkv_compressor.git
cd mkv_compressor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Install from PyPI (when available)

```bash
pip install mkv-video-compressor
```

## Quick Start

### GUI Mode

Launch the graphical interface:

```bash
python -m mkv_compressor.gui
```

Or if installed globally:

```bash
mkv-compressor-gui
```

1. **Add Files**: Click "Add Files" or drag and drop video files
2. **Choose Output**: Select output directory
3. **Select Preset**: Choose from High Quality, Balanced, Small Size, etc.
4. **Start Compression**: Click "Start Compression"

### CLI Mode

Compress a single file:

```bash
python -m mkv_compressor.cli input.mp4 -o output.mkv
```

Batch compress multiple files:

```bash
python -m mkv_compressor.cli *.mp4 -d ./compressed/
```

Use a specific preset:

```bash
python -m mkv_compressor.cli input.mp4 -o output.mkv --preset "High Quality"
```

Custom settings:

```bash
python -m mkv_compressor.cli input.mp4 -o output.mkv --crf 20 --preset slow
```

## Compression Presets

| Preset | CRF | Speed | Audio | Use Case |
|--------|-----|-------|-------|----------|
| **High Quality** | 18 | slow | 192k | Best quality, larger files |
| **Balanced** | 23 | medium | 128k | Good quality/size balance |
| **Small Size** | 28 | fast | 96k | Smaller files, lower quality |
| **Mobile** | 26 | fast | 96k | Mobile devices (720p) |
| **Web Optimized** | 24 | medium | 128k | Web streaming |

## Usage Examples

### CLI Examples

```bash
# Basic compression
mkv-compressor input.mp4 -o output.mkv

# Compress multiple files to directory
mkv-compressor video1.mp4 video2.avi video3.mov -d ./compressed/

# Use high quality preset
mkv-compressor input.mp4 -o output.mkv --preset "High Quality"

# Custom CRF and preset
mkv-compressor input.mp4 -o output.mkv --crf 20 --preset slow

# Two-pass encoding for better quality
mkv-compressor input.mp4 -o output.mkv --two-pass

# Custom resolution
mkv-compressor input.mp4 -o output.mkv --resolution 1280x720

# Batch process with recursion
mkv-compressor /path/to/videos/ -d ./output/ --recursive

# Dry run (see what would be processed)
mkv-compressor *.mp4 -d ./output/ --dry-run

# Get video file information
mkv-compressor --info video.mp4

# List available presets
mkv-compressor --list-presets
```

### GUI Features

- **Drag & Drop**: Drag video files directly into the application
- **Progress Tracking**: Real-time progress with speed and ETA
- **Settings Management**: Save and load custom compression settings
- **Batch Processing**: Process multiple files simultaneously
- **History**: Track compression history and results
- **Notifications**: Desktop notifications when compression completes

## Configuration

The application stores settings in:
- **Windows**: `%LOCALAPPDATA%\MKV Compressor\settings.json`
- **macOS**: `~/.config/mkv-compressor/settings.json`
- **Linux**: `~/.config/mkv-compressor/settings.json`

### Configuration Options

```json
{
  "ffmpeg_path": "",
  "default_output_dir": "~/Videos/Compressed",
  "overwrite_files": false,
  "show_notifications": true,
  "auto_open_output": false,
  "last_used_preset": "Balanced",
  "log_level": "INFO"
}
```

## Supported Formats

### Input Formats
- MP4, AVI, MOV, MKV, WMV, FLV
- WebM, M4V, 3GP, OGV, TS, MTS
- Any format supported by FFmpeg

### Output Format
- MKV (Matroska Video) - Professional container format

## Performance Tips

1. **Use SSD storage** for faster I/O during compression
2. **Close other applications** to free up CPU and memory
3. **Choose appropriate preset** based on your needs:
   - Use "Fast" presets for quick compression
   - Use "Slow" presets for best quality
4. **Two-pass encoding** provides better quality but takes longer
5. **Lower CRF values** = better quality but larger files

## Troubleshooting

### FFmpeg Not Found

```bash
# Check if FFmpeg is installed
ffmpeg -version

# Add FFmpeg to PATH or specify path in settings
```

### Out of Memory Errors

- Close other applications
- Reduce the number of concurrent processes
- Use a lower resolution or higher CRF value

### Slow Compression

- Use faster presets (ultrafast, superfast, veryfast)
- Increase CRF value for smaller files
- Ensure input files are on fast storage (SSD)

### Permission Errors

- Run as administrator/sudo if needed
- Check write permissions for output directory
- Ensure input files are not in use by other applications

## Advanced Usage

### Custom Logo and Branding

You can customize the application's appearance by adding your own logo:

1. **Add your logo files** to the `assets/images/` directory:
   - `logo.png` - Main header logo (recommended: 48x48px)
   - `icon.ico` - Window icon for taskbar
   - `logo_large.png` - Large logo for About dialog (recommended: 256x256px)

2. **Supported formats**: PNG (recommended), ICO, JPG, GIF
3. **Logo guidelines**:
   - Use PNG format for transparency support
   - Header logo: 48x48px or 64x64px for best results
   - Large logo: 256x256px for About dialog
   - Window icon: ICO format for Windows compatibility

The application will automatically detect and use your custom logos when available.

### Demo Recording

To create a demo GIF for your customized version:

1. **Record screen activity** showing key features
2. **Save as GIF** to `assets/demo/app_preview.gif`
3. **Recommended specs**: 800x600px, under 10MB, 10-30 seconds
4. **Tools**: OBS Studio, ScreenToGif, LICEcap

### Custom Presets

Create custom compression presets in the GUI or modify the configuration file:

```json
{
  "custom_presets": {
    "My Custom Preset": {
      "crf": 22,
      "preset": "medium",
      "audio_bitrate": "160k",
      "video_codec": "libx264"
    }
  }
}
```

### Automation Scripts

Use the CLI for automated batch processing:

```bash
#!/bin/bash
# Process all videos in input directory
for file in /path/to/input/*.mp4; do
    mkv-compressor "$file" -d /path/to/output/ --preset "Balanced"
done
```

### Integration with Other Tools

The CLI can be easily integrated with:
- File watchers (automatically compress new files)
- Media servers (automated transcoding)
- Batch scripts and workflows
- Other video processing pipelines

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=mkv_compressor

# Run specific test file
python -m pytest tests/test_core.py
```

### Code Style

The project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black src/

# Check linting
flake8 src/

# Type checking
mypy src/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/your-username/mkv_compressor/issues)
- **Documentation**: [Project Wiki](https://github.com/your-username/mkv_compressor/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/mkv_compressor/discussions)

## Changelog

### v1.1.0
- Modern dark theme GUI with advanced styling
- Improved progress monitoring with dynamic visual feedback
- Enhanced error handling and user experience
- Fixed compression progress callback issues
- Added glass morphism effects and modern UI components
- Better file overwrite handling

### v1.0.0
- Initial release
- GUI and CLI interfaces
- Multiple compression presets
- Batch processing support
- Progress monitoring
- Configuration management

## Acknowledgments

- **FFmpeg** team for the excellent video processing library
- **Python** community for the amazing ecosystem
- Contributors and testers who helped improve this tool