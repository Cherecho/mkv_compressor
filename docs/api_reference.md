# API Documentation

## Core Classes

### VideoCompressor

Main class for video compression operations.

```python
from mkv_compressor.core import VideoCompressor, CompressionSettings

# Initialize compressor
compressor = VideoCompressor(ffmpeg_path="/path/to/ffmpeg")

# Get video information
info = compressor.get_video_info("input.mp4")

# Compress video
settings = CompressionSettings(crf=23, preset="medium")
success = compressor.compress_video("input.mp4", "output.mkv", settings)
```

#### Methods

##### `__init__(ffmpeg_path=None)`
Initialize the video compressor.

**Parameters:**
- `ffmpeg_path` (str, optional): Path to FFmpeg executable

**Raises:**
- `RuntimeError`: If FFmpeg is not found or not working

##### `get_video_info(input_path)`
Get detailed information about a video file.

**Parameters:**
- `input_path` (str): Path to the video file

**Returns:**
- `VideoInfo`: Object containing video details

**Raises:**
- `RuntimeError`: If failed to get video info

##### `compress_video(input_path, output_path, settings, progress_callback=None, overwrite=False)`
Compress a video file to MKV format.

**Parameters:**
- `input_path` (str): Path to input video file
- `output_path` (str): Path to output MKV file
- `settings` (CompressionSettings): Compression settings
- `progress_callback` (callable, optional): Callback for progress updates
- `overwrite` (bool): Whether to overwrite existing output file

**Returns:**
- `bool`: True if compression successful

##### `batch_compress(input_files, output_dir, settings, progress_callback=None)`
Compress multiple video files in batch.

**Parameters:**
- `input_files` (List[str]): List of input file paths
- `output_dir` (str): Output directory
- `settings` (CompressionSettings): Compression settings
- `progress_callback` (callable, optional): Callback for batch progress

**Returns:**
- `Dict[str, bool]`: Dictionary mapping input files to success status

##### `get_compression_presets()`
Get predefined compression presets.

**Returns:**
- `Dict[str, CompressionSettings]`: Dictionary of preset names to settings

### CompressionSettings

Configuration class for compression parameters.

```python
from mkv_compressor.core import CompressionSettings

# Default settings
settings = CompressionSettings()

# Custom settings
settings = CompressionSettings(
    crf=20,
    preset="slow",
    audio_bitrate="192k",
    two_pass=True
)
```

#### Attributes

- `video_codec` (str): Video codec (default: "libx264")
- `crf` (int): Constant Rate Factor, 0-51 (default: 23)
- `preset` (str): Encoding speed preset (default: "medium")
- `audio_codec` (str): Audio codec (default: "aac")
- `audio_bitrate` (str): Audio bitrate (default: "128k")
- `width` (int, optional): Output width
- `height` (int, optional): Output height
- `scale_filter` (str, optional): FFmpeg scale filter
- `two_pass` (bool): Use two-pass encoding (default: False)
- `target_size` (str, optional): Target file size
- `max_bitrate` (str, optional): Maximum bitrate
- `container_format` (str): Output container format (default: "matroska")

#### Methods

##### `to_dict()`
Convert settings to dictionary.

**Returns:**
- `Dict[str, Any]`: Settings as dictionary

##### `from_dict(data)`
Create settings from dictionary.

**Parameters:**
- `data` (Dict[str, Any]): Settings dictionary

**Returns:**
- `CompressionSettings`: New settings instance

### VideoInfo

Container for video file information.

#### Attributes

- `filename` (str): File name
- `duration` (float): Duration in seconds
- `width` (int): Video width
- `height` (int): Video height
- `fps` (float): Frame rate
- `file_size` (int): File size in bytes
- `video_codec` (str): Video codec
- `audio_codec` (str): Audio codec
- `bitrate` (int): Bitrate

#### Properties

##### `size_mb`
File size in megabytes.

**Returns:**
- `float`: Size in MB

##### `resolution`
Video resolution as string.

**Returns:**
- `str`: Resolution (e.g., "1920x1080")

### CompressionProgress

Progress tracking for video compression.

```python
from mkv_compressor.core import CompressionProgress

# Create progress tracker
progress = CompressionProgress(total_duration=120.0)

# Set progress callback
progress.set_callback(lambda p: print(f"Progress: {p:.1f}%"))

# Update progress
progress.update(current_time=60.0, speed=2.0)
```

#### Methods

##### `__init__(total_duration)`
Initialize progress tracker.

**Parameters:**
- `total_duration` (float): Total duration in seconds

##### `update(current_time, speed=0.0)`
Update compression progress.

**Parameters:**
- `current_time` (float): Current time processed
- `speed` (float): Processing speed

##### `set_callback(callback)`
Set progress callback function.

**Parameters:**
- `callback` (callable): Function called with progress percentage

#### Properties

##### `percentage`
Current progress as percentage.

**Returns:**
- `float`: Progress percentage (0-100)

## Utility Classes

### ConfigManager

Configuration management for application settings.

```python
from mkv_compressor.utils import ConfigManager

# Initialize config manager
config = ConfigManager()

# Get/set values
config.set('output_dir', '/path/to/output')
output_dir = config.get('output_dir')

# Save configuration
config.save()
```

#### Methods

##### `__init__(config_file=None)`
Initialize configuration manager.

**Parameters:**
- `config_file` (str, optional): Path to config file

##### `get(key, default=None)`
Get a setting value.

**Parameters:**
- `key` (str): Setting key (supports dot notation)
- `default` (Any): Default value if key not found

**Returns:**
- `Any`: Setting value or default

##### `set(key, value)`
Set a setting value.

**Parameters:**
- `key` (str): Setting key (supports dot notation)
- `value` (Any): Value to set

##### `save()`
Save current settings to file.

##### `load()`
Load settings from file.

##### `get_default_settings()`
Get default configuration settings.

**Returns:**
- `Dict[str, Any]`: Default settings

## Utility Functions

### File Operations

```python
from mkv_compressor.utils import (
    format_file_size, format_duration, is_video_file,
    get_unique_filename, find_ffmpeg
)

# Format file size
size_str = format_file_size(1024 * 1024)  # "1.0 MB"

# Format duration
duration_str = format_duration(3661)  # "01:01:01"

# Check if file is video
is_video = is_video_file("movie.mp4")  # True

# Get unique filename
unique_path = get_unique_filename("output.mkv")

# Find FFmpeg executable
ffmpeg_path = find_ffmpeg()
```

### System Information

```python
from mkv_compressor.utils import (
    get_system_info, get_available_disk_space,
    validate_ffmpeg
)

# Get system information
sys_info = get_system_info()

# Check disk space
free_space = get_available_disk_space("/path/to/check")

# Validate FFmpeg
is_valid, message = validate_ffmpeg("/usr/bin/ffmpeg")
```

### Logging

```python
from mkv_compressor.utils import setup_logger, ProgressLogger

# Setup logger
logger = setup_logger(
    name='my_app',
    level=logging.INFO,
    log_file='app.log'
)

# Progress logger
progress_logger = ProgressLogger(logger, "Video Compression")
progress_logger.log_start("Starting compression")
progress_logger.log_progress(50.0, "Half complete")
progress_logger.log_complete(True, "Compression successful")
```

## CLI Integration

### Using as Library

```python
from mkv_compressor.cli import create_parser, main

# Parse command line arguments
parser = create_parser()
args = parser.parse_args(['input.mp4', '-o', 'output.mkv'])

# Run CLI main function
main()  # Uses sys.argv
```

### Custom CLI Scripts

```python
import sys
from mkv_compressor.core import VideoCompressor, CompressionSettings
from mkv_compressor.utils import setup_logger

def my_compression_script(input_file, output_file):
    """Custom compression script."""
    
    # Setup logging
    logger = setup_logger()
    
    try:
        # Initialize compressor
        compressor = VideoCompressor()
        
        # Create settings
        settings = CompressionSettings(crf=20, preset="slow")
        
        # Progress callback
        def progress(percentage):
            print(f"Progress: {percentage:.1f}%", end='\r')
        
        # Compress video
        success = compressor.compress_video(
            input_file, output_file, settings,
            progress_callback=progress
        )
        
        if success:
            print(f"\nCompression successful: {output_file}")
            return 0
        else:
            print(f"\nCompression failed")
            return 1
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: script.py input.mp4 output.mkv")
        sys.exit(1)
    
    sys.exit(my_compression_script(sys.argv[1], sys.argv[2]))
```

## Error Handling

### Common Exceptions

```python
from mkv_compressor.core import VideoCompressor
from mkv_compressor.utils import ConfigManager

try:
    compressor = VideoCompressor()
except RuntimeError as e:
    print(f"FFmpeg error: {e}")

try:
    info = compressor.get_video_info("invalid.mp4")
except RuntimeError as e:
    print(f"Cannot read video file: {e}")

try:
    config = ConfigManager()
    config.load()
except Exception as e:
    print(f"Configuration error: {e}")
```

### Best Practices

1. **Always handle exceptions** when calling compression methods
2. **Validate input files** before processing
3. **Check available disk space** before compression
4. **Use progress callbacks** for long operations
5. **Log errors** for debugging purposes

## Examples

### Basic Compression

```python
from mkv_compressor.core import VideoCompressor, CompressionSettings

def compress_video_basic(input_path, output_path):
    """Basic video compression example."""
    
    compressor = VideoCompressor()
    settings = CompressionSettings(crf=23, preset="medium")
    
    def progress_callback(percentage):
        print(f"Progress: {percentage:.1f}%")
    
    success = compressor.compress_video(
        input_path, output_path, settings,
        progress_callback=progress_callback,
        overwrite=True
    )
    
    return success
```

### Batch Processing

```python
import os
from mkv_compressor.core import VideoCompressor, CompressionSettings
from mkv_compressor.utils import is_video_file

def batch_compress_directory(input_dir, output_dir, preset_name="Balanced"):
    """Batch compress all videos in a directory."""
    
    compressor = VideoCompressor()
    presets = compressor.get_compression_presets()
    settings = presets[preset_name]
    
    # Find all video files
    video_files = []
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath) and is_video_file(filepath):
            video_files.append(filepath)
    
    if not video_files:
        print("No video files found")
        return
    
    # Batch progress callback
    def batch_progress(current, total, filename):
        print(f"Processing {current}/{total}: {filename}")
    
    # Process files
    results = compressor.batch_compress(
        video_files, output_dir, settings,
        progress_callback=batch_progress
    )
    
    # Print results
    successful = sum(results.values())
    print(f"Completed: {successful}/{len(video_files)} files")
    
    return results
```

### Custom Preset Management

```python
from mkv_compressor.utils import ConfigManager
from mkv_compressor.core import CompressionSettings

def create_custom_preset(name, crf, preset_speed, audio_bitrate):
    """Create and save a custom compression preset."""
    
    config = ConfigManager()
    
    # Create settings
    settings = CompressionSettings(
        crf=crf,
        preset=preset_speed,
        audio_bitrate=audio_bitrate
    )
    
    # Save as custom preset
    config.save_custom_preset(name, settings.to_dict())
    config.save()
    
    print(f"Custom preset '{name}' saved")

def use_custom_preset(preset_name, input_file, output_file):
    """Use a custom preset for compression."""
    
    config = ConfigManager()
    custom_presets = config.get_custom_presets()
    
    if preset_name not in custom_presets:
        print(f"Custom preset '{preset_name}' not found")
        return False
    
    # Load settings
    settings_dict = custom_presets[preset_name]
    settings = CompressionSettings.from_dict(settings_dict)
    
    # Compress
    compressor = VideoCompressor()
    return compressor.compress_video(input_file, output_file, settings)
```

This API documentation provides comprehensive coverage of all public classes, methods, and functions available in the MKV Video Compressor library.