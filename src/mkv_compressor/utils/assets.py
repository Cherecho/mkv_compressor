"""
Asset management utilities for loading logos, icons, and other resources.
"""

import os
import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class AssetManager:
    """Manages application assets including logos, icons, and images."""

    def __init__(self):
        """Initialize asset manager with project paths."""
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.assets_dir = self.project_root / "assets"
        self.images_dir = self.assets_dir / "images"
        self.demo_dir = self.assets_dir / "demo"

        # Ensure asset directories exist
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.demo_dir.mkdir(parents=True, exist_ok=True)

        # Cache for loaded images
        self._image_cache = {}

    def get_logo(self, size: Optional[Tuple[int, int]] = None) -> Optional[PhotoImage]:
        """
        Load the main application logo.

        Args:
            size: Optional tuple of (width, height) to resize logo

        Returns:
            PhotoImage object or None if logo not found
        """
        logo_paths = [
            self.images_dir / "logo.png",
            self.images_dir / "logo.jpg",
            self.images_dir / "logo.jpeg",
            self.images_dir / "logo.gif",
        ]

        for logo_path in logo_paths:
            if logo_path.exists():
                try:
                    cache_key = f"logo_{size}"
                    if cache_key in self._image_cache:
                        return self._image_cache[cache_key]

                    # Check if we have a root window available
                    try:
                        import tkinter as tk
                        root = tk._default_root
                        if root is None:
                            # If no root window exists, we can't load images yet
                            logger.warning(f"No tkinter root window available, cannot load {logo_path}")
                            continue
                    except:
                        logger.warning("Tkinter not properly initialized")
                        continue

                    image = PhotoImage(file=str(logo_path))

                    # Resize if requested
                    if size:
                        width, height = size
                        # Simple subsample for resizing (basic approach)
                        original_width = image.width()
                        original_height = image.height()

                        if original_width > width or original_height > height:
                            x_factor = max(1, original_width // width)
                            y_factor = max(1, original_height // height)
                            factor = max(x_factor, y_factor)
                            image = image.subsample(factor, factor)

                    self._image_cache[cache_key] = image
                    logger.info(f"Loaded logo from {logo_path}")
                    return image

                except Exception as e:
                    logger.warning(f"Failed to load logo from {logo_path}: {e}")
                    continue

        logger.info("No logo file found, using default")
        return None

    def get_window_icon(self) -> Optional[str]:
        """
        Get path to window icon file.

        Returns:
            Path to icon file or None if not found
        """
        icon_paths = [
            self.images_dir / "icon.ico",
            self.images_dir / "logo.ico",
            self.images_dir / "app.ico",
        ]

        for icon_path in icon_paths:
            if icon_path.exists():
                logger.info(f"Found window icon at {icon_path}")
                return str(icon_path)

        logger.info("No window icon found")
        return None

    def get_large_logo(self) -> Optional[PhotoImage]:
        """
        Load large logo for about dialog.

        Returns:
            PhotoImage object or None if not found
        """
        logo_paths = [
            self.images_dir / "logo_large.png",
            self.images_dir / "logo_banner.png",
            self.images_dir / "logo.png",
        ]

        for logo_path in logo_paths:
            if logo_path.exists():
                try:
                    if "large_logo" in self._image_cache:
                        return self._image_cache["large_logo"]

                    image = PhotoImage(file=str(logo_path))
                    self._image_cache["large_logo"] = image
                    logger.info(f"Loaded large logo from {logo_path}")
                    return image

                except Exception as e:
                    logger.warning(f"Failed to load large logo from {logo_path}: {e}")
                    continue

        return None

    def create_placeholder_logo(self, size: Tuple[int, int] = (64, 64)) -> PhotoImage:
        """
        Create a placeholder logo when no logo file is available.

        Args:
            size: Tuple of (width, height) for the placeholder

        Returns:
            PhotoImage with placeholder design
        """
        width, height = size

        # Create a simple placeholder with modern design
        # This is a basic implementation - for a real placeholder,
        # you might want to use PIL to create a more sophisticated design
        placeholder = PhotoImage(width=width, height=height)

        # Fill with gradient-like pattern (simplified)
        for y in range(height):
            for x in range(width):
                # Simple gradient effect
                intensity = int(255 * (1 - y / height) * 0.3 + 100)
                color = f"#{intensity:02x}{intensity:02x}{intensity + 50:02x}"
                placeholder.put(color, (x, y))

        return placeholder

    def get_demo_gif_path(self) -> Optional[str]:
        """
        Get path to demo GIF for README.

        Returns:
            Path to demo GIF or None if not found
        """
        gif_paths = [
            self.demo_dir / "app_preview.gif",
            self.demo_dir / "demo.gif",
            self.demo_dir / "preview.gif",
        ]

        for gif_path in gif_paths:
            if gif_path.exists():
                return str(gif_path)

        return None


# Global asset manager instance
asset_manager = AssetManager()


def get_logo(size: Optional[Tuple[int, int]] = None) -> Optional[PhotoImage]:
    """Convenience function to get logo."""
    return asset_manager.get_logo(size)


def get_window_icon() -> Optional[str]:
    """Convenience function to get window icon path."""
    return asset_manager.get_window_icon()


def get_large_logo() -> Optional[PhotoImage]:
    """Convenience function to get large logo."""
    return asset_manager.get_large_logo()
