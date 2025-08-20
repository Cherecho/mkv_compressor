# MKV Video Compressor User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [GUI Interface](#gui-interface)
3. [Command Line Interface](#command-line-interface)
4. [Compression Settings](#compression-settings)
5. [Tips and Best Practices](#tips-and-best-practices)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **FFmpeg**: Must be installed and available in system PATH
- **RAM**: At least 4GB recommended (8GB+ for large files)
- **Storage**: Sufficient free space for output files

### Installing FFmpeg

#### Windows
1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg\`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Verify installation: open Command Prompt and type `ffmpeg -version`

#### macOS
```bash
# Using Homebrew
brew install ffmpeg

# Using MacPorts
sudo port install ffmpeg
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL/Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

### First Time Setup

1. **Install the application** following the README instructions
2. **Launch the GUI** or use the CLI
3. **Configure FFmpeg path** in settings if not automatically detected
4. **Set default output directory** for convenience
5. **Test with a small video file** to ensure everything works

## GUI Interface

### Main Window Overview

The GUI consists of several key areas:

#### Input Files Section
- **File List**: Shows selected video files
- **Add Files**: Select individual video files
- **Add Folder**: Add all video files from a directory
- **Remove Selected**: Remove files from the list
- **Clear All**: Remove all files
- **Drag & Drop**: Drag files directly into the list area

#### Output Directory Section
- **Output Path**: Shows where compressed files will be saved
- **Browse**: Select output directory

#### Compression Settings Section
- **Preset Dropdown**: Choose from predefined compression settings
- **Custom Settings**: Advanced options for fine-tuning
- **Preset Info**: Brief description of selected preset

#### Control Buttons
- **Preview Settings**: See what settings will be applied
- **Start Compression**: Begin the compression process

### Using the GUI

#### Basic Workflow

1. **Add Video Files**
   - Click "Add Files" and select video files, OR
   - Click "Add Folder" to add all videos from a directory, OR
   - Drag and drop files directly into the application

2. **Choose Output Directory**
   - Click "Browse" next to the output directory field
   - Select where you want compressed files saved

3. **Select Compression Preset**
   - Choose from the dropdown menu:
     - **High Quality**: Best quality, larger files
     - **Balanced**: Good compromise (recommended)
     - **Small Size**: Smaller files, lower quality
     - **Mobile**: Optimized for mobile devices
     - **Web Optimized**: Good for web streaming

4. **Start Compression**
   - Click "Start Compression"
   - Monitor progress in the progress window
   - Wait for completion notification

#### Progress Window

When compression starts, a progress window shows:

- **Current File**: Which file is being processed
- **Progress Bar**: Overall completion percentage
- **Log Area**: Detailed progress information
- **Cancel Button**: Stop compression if needed
- **Close Button**: Close window when finished

#### Settings Tab

Configure application preferences:

- **FFmpeg Path**: Location of FFmpeg executable
- **Default Output Directory**: Where files are saved by default
- **Overwrite Files**: Whether to overwrite existing files
- **Show Notifications**: Desktop notifications on completion
- **Auto-open Output**: Open output folder when done

### Advanced GUI Features

#### Custom Settings Dialog
Access advanced compression options:
- **Video Codec**: Choose encoding algorithm
- **CRF**: Quality setting (0-51, lower = better)
- **Preset Speed**: Encoding speed vs. quality
- **Audio Settings**: Codec and bitrate options
- **Resolution**: Output video dimensions
- **Two-pass Encoding**: Better quality option

#### Batch Processing
- Add multiple files or entire folders
- Monitor progress for each file individually
- View success/failure status for each file
- Automatic retry on failure (optional)

## Command Line Interface

### Basic Usage

```bash
# Compress single file
mkv-compressor input.mp4 -o output.mkv

# Compress multiple files
mkv-compressor file1.mp4 file2.avi -d output_folder/

# Use glob patterns
mkv-compressor *.mp4 -d compressed/
```

### Command Line Options

#### Input/Output Options
```bash
-o, --output FILE           Output file (single file mode)
-d, --output-dir DIR        Output directory (multiple files)
```

#### Preset Options
```bash
--preset PRESET            Compression preset
--list-presets             Show available presets
```

#### Custom Compression Settings
```bash
--crf CRF                   Quality (0-51, lower=better)
--preset-speed SPEED        Encoding speed
--video-codec CODEC         Video codec
--audio-codec CODEC         Audio codec
--audio-bitrate RATE        Audio bitrate
--resolution WIDTHxHEIGHT   Output resolution
--two-pass                  Use two-pass encoding
```

#### Processing Options
```bash
--overwrite                 Overwrite existing files
--recursive                 Process directories recursively
--dry-run                   Show what would be done
```

#### Information Commands
```bash
--info FILE                 Show video file information
--list-presets              Show compression presets
```

#### Logging Options
```bash
-v, --verbose               Verbose output
-q, --quiet                 Suppress output except errors
--log-file FILE             Write log to file
```

### CLI Examples

#### Basic Compression
```bash
# Simple compression with default settings
mkv-compressor movie.mp4 -o movie_compressed.mkv

# Use high quality preset
mkv-compressor movie.mp4 -o movie_hq.mkv --preset "High Quality"
```

#### Batch Processing
```bash
# Compress all MP4 files in current directory
mkv-compressor *.mp4 -d ./compressed/

# Process directory recursively
mkv-compressor /path/to/videos/ -d /path/to/output/ --recursive

# Mix of files and patterns
mkv-compressor video1.mp4 *.avi videos/*.mov -d output/
```

#### Custom Settings
```bash
# Custom quality and speed
mkv-compressor input.mp4 -o output.mkv --crf 20 --preset slow

# Change resolution
mkv-compressor input.mp4 -o output.mkv --resolution 1280x720

# Two-pass encoding for best quality
mkv-compressor input.mp4 -o output.mkv --two-pass --crf 18

# Custom audio settings
mkv-compressor input.mp4 -o output.mkv --audio-codec aac --audio-bitrate 192k
```

#### Information and Analysis
```bash
# Get detailed video information
mkv-compressor --info video.mp4

# List all available presets
mkv-compressor --list-presets

# Dry run to see what would be processed
mkv-compressor *.mp4 -d output/ --dry-run
```

## Compression Settings

### Understanding CRF (Constant Rate Factor)

CRF controls the quality-to-size ratio:

- **0-17**: Visually lossless (very large files)
- **18-23**: High quality (recommended range)
- **24-28**: Medium quality (good for most uses)
- **29-51**: Lower quality (smaller files)

**Recommendation**: Start with CRF 23 and adjust based on results.

### Preset Speeds

Encoding speed presets (from fastest to slowest):

1. **ultrafast**: Fastest encoding, lowest compression efficiency
2. **superfast**: Very fast encoding
3. **veryfast**: Fast encoding
4. **faster**: Faster than default
5. **fast**: Fast encoding
6. **medium**: Default speed/efficiency balance
7. **slow**: Slower but better compression
8. **slower**: Much slower, better compression
9. **veryslow**: Slowest, best compression efficiency

**Trade-off**: Slower presets produce smaller files with better quality but take much longer to encode.

### Audio Settings

#### Audio Codecs
- **AAC**: Best compatibility and quality (recommended)
- **MP3**: Wide compatibility, slightly larger files
- **Vorbis**: Open source, good quality
- **Copy**: Keep original audio unchanged

#### Audio Bitrates
- **96k**: Low quality, very small files
- **128k**: Standard quality (default)
- **192k**: High quality
- **256k**: Very high quality
- **320k**: Maximum quality for most codecs

### Video Codecs

#### H.264 (libx264)
- **Pros**: Excellent compatibility, good quality/size ratio
- **Cons**: Older standard, larger files than newer codecs
- **Use for**: Maximum compatibility

#### H.265 (libx265)
- **Pros**: 25-50% smaller files than H.264 at same quality
- **Cons**: Slower encoding, less compatibility
- **Use for**: Modern devices, when file size is critical

#### VP9 (libvpx-vp9)
- **Pros**: Open source, good compression
- **Cons**: Very slow encoding, limited hardware support
- **Use for**: Web streaming, when encoding time is not critical

### Resolution and Scaling

#### Common Resolutions
- **4K UHD**: 3840x2160
- **1440p**: 2560x1440  
- **1080p**: 1920x1080 (Full HD)
- **720p**: 1280x720 (HD)
- **480p**: 854x480 (SD)

#### When to Scale Down
- Target device has limited resolution
- Need smaller file sizes
- Bandwidth limitations
- Storage constraints

## Tips and Best Practices

### Quality Optimization

1. **Start with balanced preset** and adjust if needed
2. **Use CRF 18-23** for high quality
3. **Test with short clips** before processing long videos
4. **Consider two-pass encoding** for best quality
5. **Keep original files** until satisfied with results

### Performance Optimization

1. **Close unnecessary applications** during compression
2. **Use SSD storage** for input and output files
3. **Ensure adequate free space** (2x input file size recommended)
4. **Monitor system temperature** during long compressions
5. **Use faster presets** for quick previews

### File Management

1. **Organize input and output directories** clearly
2. **Use descriptive output filenames** (include preset/settings)
3. **Backup original files** before compression
4. **Verify compressed files** play correctly
5. **Clean up temporary files** periodically

### Batch Processing

1. **Group similar files** for consistent settings
2. **Process overnight** for large batches
3. **Monitor disk space** during processing
4. **Use dry-run mode** to verify file selection
5. **Save successful settings** as custom presets

### Quality Control

1. **Compare before/after** file sizes and quality
2. **Test playback** on target devices
3. **Check audio synchronization**
4. **Verify subtitle preservation** if applicable
5. **Document successful settings** for future use

## Troubleshooting

### Common Issues

#### FFmpeg Not Found
**Symptoms**: "FFmpeg not found" error on startup

**Solutions**:
1. Install FFmpeg from official website
2. Add FFmpeg to system PATH
3. Specify FFmpeg path in application settings
4. Verify installation with `ffmpeg -version`

#### Out of Memory Errors
**Symptoms**: Application crashes or "out of memory" errors

**Solutions**:
1. Close other applications
2. Restart computer to free memory
3. Process smaller batches
4. Use faster presets
5. Reduce output resolution

#### Slow Compression Speed
**Symptoms**: Very slow processing, long estimated times

**Solutions**:
1. Use faster presets (fast, veryfast, ultrafast)
2. Increase CRF value (lower quality, faster processing)
3. Close background applications
4. Check system temperature (thermal throttling)
5. Use hardware acceleration if available

#### Large Output Files
**Symptoms**: Compressed files larger than expected

**Solutions**:
1. Increase CRF value (higher = smaller files)
2. Use slower presets for better compression
3. Reduce output resolution
4. Use two-pass encoding
5. Check if input is already compressed

#### Poor Quality Output
**Symptoms**: Visible artifacts, pixelation, or quality loss

**Solutions**:
1. Decrease CRF value (lower = better quality)
2. Use slower presets
3. Ensure input file is high quality
4. Use two-pass encoding
5. Check if extreme resolution scaling is applied

#### Audio/Video Sync Issues
**Symptoms**: Audio and video out of sync

**Solutions**:
1. Use "copy" audio codec to preserve original
2. Update FFmpeg to latest version
3. Check input file for existing sync issues
4. Try different audio codec/bitrate
5. Report as bug if issue persists

#### Permission Errors
**Symptoms**: "Access denied" or permission errors

**Solutions**:
1. Run application as administrator
2. Check file/folder permissions
3. Ensure input files are not in use
4. Choose different output directory
5. Close other applications using the files

### Getting Help

#### Log Files
Enable verbose logging to help diagnose issues:
- GUI: Enable in Settings tab
- CLI: Use `--verbose` flag
- Log files location varies by OS (see Configuration section)

#### System Information
Gather system info for support:
- OS version and architecture
- Python version
- FFmpeg version
- Available RAM and storage
- CPU model and core count

#### Reporting Issues
When reporting problems, include:
1. Operating system and version
2. Application version
3. FFmpeg version
4. Input file details (format, size, resolution)
5. Settings used
6. Error messages or log output
7. Steps to reproduce the issue

### Performance Monitoring

#### Resource Usage
Monitor during compression:
- **CPU usage**: Should be near 100% for efficient encoding
- **Memory usage**: Watch for excessive RAM consumption
- **Disk I/O**: Ensure fast read/write speeds
- **Temperature**: Prevent thermal throttling

#### Progress Indicators
- **Processing speed**: FPS or time processed per second
- **ETA**: Estimated time to completion
- **File progress**: Current file in batch
- **Overall progress**: Total batch completion

By following this guide, you should be able to effectively use the MKV Video Compressor for all your video compression needs. For additional help, consult the README file or project documentation.