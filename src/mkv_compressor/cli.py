"""
Command-line interface for MKV Video Compressor.
"""

import argparse
import sys
import os
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from tqdm import tqdm

from ..core import VideoCompressor, CompressionSettings
from ..utils.logger import setup_logger
from ..utils.config import ConfigManager


class CLIProgressHandler:
    """Progress handler for CLI operations."""

    def __init__(self, total_files: int = 1):
        self.total_files = total_files
        self.current_file = 0
        self.current_progress = None

    def start_file(self, filename: str):
        """Start processing a new file."""
        self.current_file += 1
        print(f"\n[{self.current_file}/{self.total_files}] Processing: {filename}")

        # Create progress bar for current file
        self.current_progress = tqdm(
            total=100,
            desc="Compressing",
            unit="%",
            bar_format="{l_bar}{bar}| {n:.1f}% [{elapsed}<{remaining}]",
        )

    def update_progress(self, percentage: float):
        """Update progress for current file."""
        if self.current_progress:
            # Update to current percentage
            current = self.current_progress.n
            self.current_progress.update(percentage - current)

    def finish_file(self, success: bool = True):
        """Finish processing current file."""
        if self.current_progress:
            self.current_progress.close()
            self.current_progress = None

        status = "✓ Success" if success else "✗ Failed"
        print(f"Status: {status}")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Professional MKV Video Compressor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compress a single file with default settings
  mkv-compressor input.mp4 -o output.mkv
  
  # Compress multiple files to a directory
  mkv-compressor *.mp4 -d /path/to/output/
  
  # Use a specific preset
  mkv-compressor input.mp4 -o output.mkv --preset "High Quality"
  
  # Custom compression settings
  mkv-compressor input.mp4 -o output.mkv --crf 20 --preset slow
  
  # Batch process with custom settings
  mkv-compressor /path/to/videos/*.mp4 -d /output/ --crf 25 --preset fast
  
  # List available presets
  mkv-compressor --list-presets
        """,
    )

    # Input files
    parser.add_argument(
        "input", nargs="*", help="Input video file(s) or pattern (e.g., *.mp4)"
    )

    # Output options
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-o", "--output", help="Output file path (for single file input)"
    )
    output_group.add_argument(
        "-d", "--output-dir", help="Output directory (for multiple files)"
    )

    # Compression presets
    parser.add_argument(
        "--preset",
        choices=["High Quality", "Balanced", "Small Size", "Mobile", "Web Optimized"],
        default="Balanced",
        help="Compression preset (default: Balanced)",
    )

    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available compression presets and exit",
    )

    # Custom compression settings
    compression_group = parser.add_argument_group("Custom Compression Settings")
    compression_group.add_argument(
        "--crf",
        type=int,
        choices=range(0, 52),
        metavar="[0-51]",
        help="Constant Rate Factor (0-51, lower=better quality)",
    )
    compression_group.add_argument(
        "--preset-speed",
        choices=[
            "ultrafast",
            "superfast",
            "veryfast",
            "faster",
            "fast",
            "medium",
            "slow",
            "slower",
            "veryslow",
        ],
        help="Encoding speed preset",
    )
    compression_group.add_argument(
        "--video-codec",
        choices=["libx264", "libx265", "libvpx-vp9"],
        help="Video codec to use",
    )
    compression_group.add_argument(
        "--audio-codec",
        choices=["aac", "libmp3lame", "libvorbis", "copy"],
        help="Audio codec to use",
    )
    compression_group.add_argument(
        "--audio-bitrate", help="Audio bitrate (e.g., 128k, 192k)"
    )
    compression_group.add_argument(
        "--resolution", help="Output resolution (e.g., 1920x1080, 1280x720)"
    )
    compression_group.add_argument(
        "--two-pass",
        action="store_true",
        help="Use two-pass encoding for better quality",
    )

    # Processing options
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing output files"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively search directories for video files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually processing",
    )

    # FFmpeg options
    parser.add_argument("--ffmpeg-path", help="Path to FFmpeg executable")

    # Logging and verbosity
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress all output except errors"
    )
    parser.add_argument("--log-file", help="Write log output to file")

    # Information commands
    parser.add_argument("--info", help="Show information about a video file and exit")

    return parser


def find_video_files(paths: List[str], recursive: bool = False) -> List[str]:
    """Find video files from input paths."""
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".m4v"}
    video_files = []

    for path in paths:
        path_obj = Path(path)

        if path_obj.is_file():
            if path_obj.suffix.lower() in video_extensions:
                video_files.append(str(path_obj.absolute()))
        elif path_obj.is_dir():
            if recursive:
                pattern = "**/*"
            else:
                pattern = "*"

            for file_path in path_obj.glob(pattern):
                if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                    video_files.append(str(file_path.absolute()))
        else:
            # Try glob pattern
            import glob

            matches = glob.glob(path, recursive=recursive)
            for match in matches:
                match_path = Path(match)
                if (
                    match_path.is_file()
                    and match_path.suffix.lower() in video_extensions
                ):
                    video_files.append(str(match_path.absolute()))

    return sorted(list(set(video_files)))  # Remove duplicates and sort


def create_compression_settings(args) -> CompressionSettings:
    """Create compression settings from CLI arguments."""
    # Start with preset if specified
    compressor = VideoCompressor()
    presets = compressor.get_compression_presets()

    if args.preset in presets:
        settings = presets[args.preset]
    else:
        settings = CompressionSettings()

    # Override with custom settings
    if args.crf is not None:
        settings.crf = args.crf
    if args.preset_speed:
        settings.preset = args.preset_speed
    if args.video_codec:
        settings.video_codec = args.video_codec
    if args.audio_codec:
        settings.audio_codec = args.audio_codec
    if args.audio_bitrate:
        settings.audio_bitrate = args.audio_bitrate
    if args.resolution:
        try:
            width, height = map(int, args.resolution.split("x"))
            settings.width = width
            settings.height = height
        except ValueError:
            raise ValueError(f"Invalid resolution format: {args.resolution}")
    if args.two_pass:
        settings.two_pass = True

    return settings


def show_presets():
    """Display available compression presets."""
    compressor = VideoCompressor()
    presets = compressor.get_compression_presets()

    print("Available Compression Presets:\n")

    for name, settings in presets.items():
        print(f"• {name}")
        print(f"  CRF: {settings.crf} (Quality)")
        print(f"  Speed: {settings.preset}")
        print(f"  Audio: {settings.audio_codec} @ {settings.audio_bitrate}")
        if settings.width and settings.height:
            print(f"  Resolution: {settings.width}x{settings.height}")
        if settings.max_bitrate:
            print(f"  Max Bitrate: {settings.max_bitrate}")
        print()


def show_video_info(filepath: str):
    """Display detailed information about a video file."""
    try:
        compressor = VideoCompressor()
        info = compressor.get_video_info(filepath)

        print(f"Video Information: {info.filename}\n")
        print(f"File Size: {info.size_mb:.1f} MB")
        print(f"Duration: {info.duration:.1f} seconds")
        print(f"Resolution: {info.resolution}")
        print(f"Frame Rate: {info.fps:.2f} fps")
        print(f"Video Codec: {info.video_codec}")
        print(f"Audio Codec: {info.audio_codec}")
        print(f"Bitrate: {info.bitrate} bps")

    except Exception as e:
        print(f"Error reading video file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    if args.quiet:
        log_level = logging.ERROR
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger = setup_logger(
        level=log_level, log_file=args.log_file, console_output=not args.quiet
    )

    try:
        # Handle special commands
        if args.list_presets:
            show_presets()
            return

        if args.info:
            show_video_info(args.info)
            return

        # Validate input files
        if not args.input:
            parser.print_help()
            print("\nError: No input files specified.", file=sys.stderr)
            sys.exit(1)

        # Find video files
        video_files = find_video_files(args.input, args.recursive)

        if not video_files:
            print("Error: No video files found.", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(video_files)} video file(s)")

        # Determine output configuration
        if len(video_files) == 1 and args.output:
            # Single file output
            output_mode = "single"
            output_path = args.output
        elif args.output_dir:
            # Directory output
            output_mode = "directory"
            output_path = args.output_dir
            os.makedirs(output_path, exist_ok=True)
        else:
            # Use current directory as default
            output_mode = "directory"
            output_path = "."

        # Create compression settings
        settings = create_compression_settings(args)

        # Show what will be processed
        print(f"\nCompression Settings:")
        print(f"  Preset: {args.preset}")
        print(f"  CRF: {settings.crf}")
        print(f"  Speed: {settings.preset}")
        print(f"  Video Codec: {settings.video_codec}")
        print(f"  Audio: {settings.audio_codec} @ {settings.audio_bitrate}")
        if settings.width and settings.height:
            print(f"  Resolution: {settings.width}x{settings.height}")
        print(f"  Two-pass: {'Yes' if settings.two_pass else 'No'}")
        print()

        if args.dry_run:
            print("DRY RUN - No files will be processed\n")
            for i, input_file in enumerate(video_files, 1):
                filename = os.path.basename(input_file)
                if output_mode == "single":
                    output_file = output_path
                else:
                    name, _ = os.path.splitext(filename)
                    output_file = os.path.join(output_path, f"{name}_compressed.mkv")

                print(f"{i}. {input_file} -> {output_file}")
            return

        # Initialize compressor
        compressor = VideoCompressor(ffmpeg_path=args.ffmpeg_path)

        # Setup progress handler
        progress_handler = CLIProgressHandler(len(video_files))

        # Process files
        successful = 0
        for input_file in video_files:
            filename = os.path.basename(input_file)

            try:
                # Determine output file
                if output_mode == "single":
                    output_file = output_path
                else:
                    name, _ = os.path.splitext(filename)
                    output_file = os.path.join(output_path, f"{name}_compressed.mkv")

                # Check if output exists
                if os.path.exists(output_file) and not args.overwrite:
                    print(
                        f"Skipping {filename} - output exists (use --overwrite to replace)"
                    )
                    continue

                # Start processing
                progress_handler.start_file(filename)

                # Compress video
                success = compressor.compress_video(
                    input_file,
                    output_file,
                    settings,
                    progress_callback=progress_handler.update_progress,
                    overwrite=args.overwrite,
                )

                progress_handler.finish_file(success)

                if success:
                    successful += 1
                    logger.info(f"Successfully compressed: {filename}")
                else:
                    logger.error(f"Failed to compress: {filename}")

            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                break
            except Exception as e:
                progress_handler.finish_file(False)
                logger.error(f"Error processing {filename}: {e}")

        # Summary
        print(f"\nProcessing complete!")
        print(f"Successfully compressed: {successful}/{len(video_files)} files")

        if successful < len(video_files):
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
