"""
Core video compression functionality for MKV files.
"""

import os
import subprocess
import logging
import tempfile
import re
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
import json
import time

import ffmpeg
import psutil
from tqdm import tqdm


@dataclass
class CompressionSettings:
    """Video compression settings configuration."""

    # Video codec settings
    video_codec: str = "libx264"
    crf: int = 23  # Constant Rate Factor (0-51, lower = better quality)
    preset: str = "medium"  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow

    # Audio settings
    audio_codec: str = "aac"
    audio_bitrate: str = "128k"

    # Resolution and scaling
    width: Optional[int] = None
    height: Optional[int] = None
    scale_filter: Optional[str] = None

    # Advanced settings
    two_pass: bool = False
    target_size: Optional[str] = None  # e.g., "500MB"
    max_bitrate: Optional[str] = None

    # Output settings
    container_format: str = "matroska"  # MKV container

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "video_codec": self.video_codec,
            "crf": self.crf,
            "preset": self.preset,
            "audio_codec": self.audio_codec,
            "audio_bitrate": self.audio_bitrate,
            "width": self.width,
            "height": self.height,
            "scale_filter": self.scale_filter,
            "two_pass": self.two_pass,
            "target_size": self.target_size,
            "max_bitrate": self.max_bitrate,
            "container_format": self.container_format,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompressionSettings":
        """Create settings from dictionary."""
        return cls(**data)


@dataclass
class VideoInfo:
    """Video file information."""

    filename: str
    duration: float
    width: int
    height: int
    fps: float
    file_size: int
    video_codec: str
    audio_codec: str
    bitrate: int

    @property
    def size_mb(self) -> float:
        """File size in megabytes."""
        return self.file_size / (1024 * 1024)

    @property
    def resolution(self) -> str:
        """Video resolution as string."""
        return f"{self.width}x{self.height}"


class CompressionProgress:
    """Progress tracking for video compression."""

    def __init__(self, total_duration: float):
        self.total_duration = total_duration
        self.current_time = 0.0
        self.progress_callback: Optional[Callable[[float], None]] = None
        self.speed = 0.0
        self.eta = 0.0
        self.is_two_pass = False

    def update(self, current_time: float, speed: float = 0.0):
        """Update compression progress."""
        self.current_time = current_time
        self.speed = speed

        if self.total_duration > 0:
            progress = min(current_time / self.total_duration, 1.0)

            # Calculate ETA
            if speed > 0 and progress > 0:
                remaining_time = self.total_duration - current_time
                self.eta = remaining_time / speed

            if self.progress_callback:
                self.progress_callback(progress)

    def set_callback(self, callback: Callable[[float], None]):
        """Set progress callback function."""
        self.progress_callback = callback

    @property
    def percentage(self) -> float:
        """Current progress as percentage."""
        if self.total_duration > 0:
            return min((self.current_time / self.total_duration) * 100, 100.0)
        return 0.0


class VideoCompressor:
    """Professional MKV video compressor using FFmpeg."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        """
        Initialize the video compressor.

        Args:
            ffmpeg_path: Path to FFmpeg executable. If None, assumes it's in PATH.
        """
        self.ffmpeg_path = ffmpeg_path or "ffmpeg"
        self.logger = logging.getLogger(__name__)
        self._verify_ffmpeg()

    def _verify_ffmpeg(self):
        """Verify that FFmpeg is available."""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                raise RuntimeError("FFmpeg not found or not working properly")

            self.logger.info("FFmpeg verified successfully")

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"FFmpeg not found: {e}")

    def get_video_info(self, input_path: str) -> VideoInfo:
        """
        Get detailed information about a video file.

        Args:
            input_path: Path to the video file

        Returns:
            VideoInfo object with file details
        """
        try:
            probe = ffmpeg.probe(input_path)

            # Get video stream info
            video_stream = next(
                (
                    stream
                    for stream in probe["streams"]
                    if stream["codec_type"] == "video"
                ),
                None,
            )

            # Get audio stream info
            audio_stream = next(
                (
                    stream
                    for stream in probe["streams"]
                    if stream["codec_type"] == "audio"
                ),
                None,
            )

            if not video_stream:
                raise ValueError("No video stream found in file")

            # Extract video information
            duration = float(probe["format"]["duration"])
            file_size = int(probe["format"]["size"])

            width = int(video_stream["width"])
            height = int(video_stream["height"])

            # Calculate FPS
            fps_str = video_stream.get("r_frame_rate", "25/1")
            fps_parts = fps_str.split("/")
            fps = float(fps_parts[0]) / float(fps_parts[1])

            video_codec = video_stream.get("codec_name", "unknown")
            audio_codec = (
                audio_stream.get("codec_name", "unknown") if audio_stream else "none"
            )

            # Calculate bitrate
            bitrate = int(probe["format"].get("bit_rate", 0))

            return VideoInfo(
                filename=os.path.basename(input_path),
                duration=duration,
                width=width,
                height=height,
                fps=fps,
                file_size=file_size,
                video_codec=video_codec,
                audio_codec=audio_codec,
                bitrate=bitrate,
            )

        except Exception as e:
            raise RuntimeError(f"Failed to get video info: {e}")

    def compress_video(
        self,
        input_path: str,
        output_path: str,
        settings: CompressionSettings,
        progress_callback: Optional[Callable[[float], None]] = None,
        overwrite: bool = False,
    ) -> bool:
        """
        Compress a video file to MKV format.

        Args:
            input_path: Path to input video file
            output_path: Path to output MKV file
            settings: Compression settings
            progress_callback: Optional callback for progress updates
            overwrite: Whether to overwrite existing output file

        Returns:
            True if compression successful, False otherwise
        """
        try:
            # Validate input file
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")

            # Check if output file exists
            if os.path.exists(output_path) and not overwrite:
                raise FileExistsError(f"Output file already exists: {output_path}")

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Get video info for progress tracking
            video_info = self.get_video_info(input_path)
            progress = CompressionProgress(video_info.duration)
            if progress_callback:
                progress.set_callback(progress_callback)

            self.logger.info(f"Starting compression: {input_path} -> {output_path}")
            self.logger.info(
                f"Input video: {video_info.resolution}, {video_info.duration:.1f}s, {video_info.size_mb:.1f}MB"
            )

            # Build FFmpeg command
            input_stream = ffmpeg.input(input_path)

            # Video processing
            video_args = {
                "vcodec": settings.video_codec,
                "crf": settings.crf,
                "preset": settings.preset,
            }

            # Handle scaling if specified
            if settings.width and settings.height:
                video_stream = input_stream.video.filter(
                    "scale", settings.width, settings.height
                )
            elif settings.scale_filter:
                video_stream = input_stream.video.filter("scale", settings.scale_filter)
            else:
                video_stream = input_stream.video

            # Audio processing
            audio_args = {
                "acodec": settings.audio_codec,
                "audio_bitrate": settings.audio_bitrate,
            }

            # Additional video arguments
            if settings.max_bitrate:
                video_args["maxrate"] = settings.max_bitrate
                video_args["bufsize"] = settings.max_bitrate

            # Create output stream
            output_stream = ffmpeg.output(
                video_stream,
                input_stream.audio,
                output_path,
                format=settings.container_format,
                **video_args,
                **audio_args,
            )

            # Handle two-pass encoding
            if settings.two_pass:
                progress.is_two_pass = True
                return self._two_pass_encode(
                    input_path, output_path, settings, progress
                )
            else:
                progress.is_two_pass = False
                return self._single_pass_encode(output_stream, progress)

        except Exception as e:
            self.logger.error(f"Compression failed: {e}")
            return False

    def _single_pass_encode(self, output_stream, progress: CompressionProgress) -> bool:
        """Perform single-pass encoding."""
        try:
            # Run FFmpeg with progress monitoring
            process = output_stream.overwrite_output().run_async(
                pipe_stdout=True, pipe_stderr=True
            )

            # Monitor progress
            self._monitor_progress(process, progress)

            # Wait for completion
            process.wait()

            if process.returncode == 0:
                self.logger.info("Compression completed successfully")
                # Ensure progress reaches 100%
                if progress.progress_callback:
                    progress.progress_callback(100)
                return True
            else:
                self.logger.error(
                    f"FFmpeg process failed with return code: {process.returncode}"
                )
                return False

        except Exception as e:
            self.logger.error(f"Single-pass encoding failed: {e}")
            return False

    def _two_pass_encode(
        self,
        input_path: str,
        output_path: str,
        settings: CompressionSettings,
        progress: CompressionProgress,
    ) -> bool:
        """Perform two-pass encoding for better quality."""
        try:
            self.logger.info("Starting two-pass encoding")

            # First pass
            self.logger.info("First pass...")
            pass1_cmd = self._build_pass1_command(input_path, settings)

            process1 = subprocess.Popen(
                pass1_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            self._monitor_progress(process1, progress, pass_number=1)
            process1.wait()

            if process1.returncode != 0:
                self.logger.error("First pass failed")
                return False

            # Second pass
            self.logger.info("Second pass...")
            pass2_cmd = self._build_pass2_command(input_path, output_path, settings)

            process2 = subprocess.Popen(
                pass2_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            self._monitor_progress(process2, progress, pass_number=2)
            process2.wait()

            # Clean up pass files
            self._cleanup_pass_files()

            if process2.returncode == 0:
                self.logger.info("Two-pass encoding completed successfully")
                # Ensure progress reaches 100%
                if progress.progress_callback:
                    progress.progress_callback(100)
                return True
            else:
                self.logger.error("Second pass failed")
                return False

        except Exception as e:
            self.logger.error(f"Two-pass encoding failed: {e}")
            return False

    def _build_pass1_command(
        self, input_path: str, settings: CompressionSettings
    ) -> List[str]:
        """Build FFmpeg command for first pass."""
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i",
            input_path,
            "-c:v",
            settings.video_codec,
            "-preset",
            settings.preset,
            "-crf",
            str(settings.crf),
            "-pass",
            "1",
            "-f",
            "null",
            "-",
        ]
        return cmd

    def _build_pass2_command(
        self, input_path: str, output_path: str, settings: CompressionSettings
    ) -> List[str]:
        """Build FFmpeg command for second pass."""
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i",
            input_path,
            "-c:v",
            settings.video_codec,
            "-preset",
            settings.preset,
            "-crf",
            str(settings.crf),
            "-pass",
            "2",
            "-c:a",
            settings.audio_codec,
            "-b:a",
            settings.audio_bitrate,
            "-f",
            settings.container_format,
            output_path,
        ]
        return cmd

    def _monitor_progress(
        self,
        process: subprocess.Popen,
        progress: CompressionProgress,
        pass_number: int = 1,
    ):
        """Monitor FFmpeg process progress with improved real-time updates."""
        import time

        try:
            buffer = b""
            last_update = time.time()

            while True:
                # Check if process has terminated
                if process.poll() is not None:
                    # Process any remaining data in buffer
                    if buffer:
                        self._parse_ffmpeg_output(
                            buffer.decode("utf-8", errors="ignore"),
                            progress,
                            pass_number,
                        )
                    break

                # Read data from stderr
                if process.stderr:
                    try:
                        # Use non-blocking read with select on Windows
                        import select

                        ready, _, _ = select.select([process.stderr], [], [], 0.1)
                        if ready:
                            chunk = process.stderr.read(8192)
                            if chunk:
                                buffer += chunk
                    except (OSError, ImportError):
                        # Fallback for Windows without select support
                        try:
                            chunk = process.stderr.read(1024)
                            if chunk:
                                buffer += chunk
                        except:
                            pass

                # Process complete lines from buffer
                while b"\n" in buffer or b"\r" in buffer:
                    if b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                    else:
                        line, buffer = buffer.split(b"\r", 1)

                    try:
                        line_str = line.decode("utf-8", errors="ignore").strip()
                        if line_str:
                            self._parse_ffmpeg_output(line_str, progress, pass_number)
                    except Exception as e:
                        self.logger.debug(f"Error parsing output line: {e}")

                # Update at least every 0.5 seconds for responsiveness
                current_time = time.time()
                if current_time - last_update > 0.5:
                    last_update = current_time
                    time.sleep(0.1)  # Small delay to prevent excessive CPU usage

        except Exception as e:
            self.logger.warning(f"Progress monitoring error: {e}")

    def _parse_ffmpeg_output(
        self, line: str, progress: CompressionProgress, pass_number: int
    ):
        """Parse FFmpeg output line for progress information."""
        if not line or not progress.progress_callback:
            return

        # Look for time information in various formats
        if "time=" in line:
            try:
                # Extract time from line like "time=00:01:23.45"
                time_match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                if time_match:
                    hours = int(time_match.group(1))
                    minutes = int(time_match.group(2))
                    seconds = float(time_match.group(3))
                    current_time = hours * 3600 + minutes * 60 + seconds

                    if progress.total_duration > 0:
                        # Calculate base progress percentage
                        base_progress = (current_time / progress.total_duration) * 100

                        # Adjust for two-pass encoding
                        if progress.is_two_pass:
                            if pass_number == 1:
                                final_progress = (
                                    base_progress * 0.5
                                )  # First pass: 0-50%
                            else:
                                final_progress = 50 + (
                                    base_progress * 0.5
                                )  # Second pass: 50-100%
                        else:
                            final_progress = base_progress

                        # Clamp to reasonable range and update
                        final_progress = max(
                            0, min(99, final_progress)
                        )  # Keep below 100% until truly done
                        progress.progress_callback(final_progress)

                        # Log speed information if available
                        if "speed=" in line:
                            speed_match = re.search(r"speed=\s*([0-9.]+)x", line)
                            if speed_match:
                                speed = float(speed_match.group(1))
                                self.logger.debug(
                                    f"Compression speed: {speed}x (Progress: {final_progress:.1f}%)"
                                )

            except (ValueError, AttributeError) as e:
                self.logger.debug(f"Error parsing time from line: {line}, error: {e}")

        # Check for completion indicators
        elif "video:" in line and ("audio:" in line or "subtitle:" in line):
            # FFmpeg final summary line indicates completion
            self.logger.info(f"FFmpeg completion summary: {line}")
        elif "error" in line.lower() or "failed" in line.lower():
            self.logger.warning(f"Potential error in FFmpeg output: {line}")

    def _cleanup_pass_files(self):
        """Clean up temporary files from two-pass encoding."""
        try:
            # Remove pass log files
            for file in os.listdir("."):
                if file.startswith("ffmpeg2pass"):
                    os.remove(file)
        except Exception as e:
            self.logger.warning(f"Failed to cleanup pass files: {e}")

    def batch_compress(
        self,
        input_files: List[str],
        output_dir: str,
        settings: CompressionSettings,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> Dict[str, bool]:
        """
        Compress multiple video files in batch.

        Args:
            input_files: List of input file paths
            output_dir: Output directory
            settings: Compression settings
            progress_callback: Callback for batch progress (current, total, filename)

        Returns:
            Dictionary mapping input files to success status
        """
        results = {}

        os.makedirs(output_dir, exist_ok=True)

        for i, input_file in enumerate(input_files):
            try:
                filename = os.path.basename(input_file)
                name, _ = os.path.splitext(filename)
                output_file = os.path.join(output_dir, f"{name}_compressed.mkv")

                if progress_callback:
                    progress_callback(i + 1, len(input_files), filename)

                self.logger.info(f"Processing {i+1}/{len(input_files)}: {filename}")

                success = self.compress_video(
                    input_file, output_file, settings, overwrite=True
                )

                results[input_file] = success

            except Exception as e:
                self.logger.error(f"Failed to process {input_file}: {e}")
                results[input_file] = False

        return results

    def get_compression_presets(self) -> Dict[str, CompressionSettings]:
        """Get predefined compression presets."""
        return {
            "High Quality": CompressionSettings(
                crf=18, preset="slow", audio_bitrate="192k"
            ),
            "Balanced": CompressionSettings(
                crf=23, preset="medium", audio_bitrate="128k"
            ),
            "Small Size": CompressionSettings(
                crf=28, preset="fast", audio_bitrate="96k"
            ),
            "Mobile": CompressionSettings(
                crf=26, preset="fast", width=1280, height=720, audio_bitrate="96k"
            ),
            "Web Optimized": CompressionSettings(
                crf=24, preset="medium", max_bitrate="2000k", audio_bitrate="128k"
            ),
        }
