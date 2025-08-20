"""
Configuration management for MKV Video Compressor.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging


class ConfigManager:
    """Manages application configuration settings."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        self.logger = logging.getLogger(__name__)

        if config_file:
            self.config_file = Path(config_file)
        else:
            # Use default config location
            config_dir = self._get_config_directory()
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_file = config_dir / "settings.json"

        self.settings: Dict[str, Any] = {}
        self.load()

    def _get_config_directory(self) -> Path:
        """Get the application configuration directory."""
        if os.name == "nt":  # Windows
            config_dir = Path.home() / "AppData" / "Local" / "MKV Compressor"
        else:  # Unix/Linux/macOS
            config_dir = Path.home() / ".config" / "mkv-compressor"

        return config_dir

    def get_default_settings(self) -> Dict[str, Any]:
        """Get default configuration settings."""
        return {
            "ffmpeg_path": "",
            "default_output_dir": str(Path.home() / "Videos" / "Compressed"),
            "overwrite_files": False,
            "show_notifications": True,
            "auto_open_output": False,
            "last_used_preset": "Balanced",
            "window_geometry": "900x700",
            "remember_window_position": True,
            "log_level": "INFO",
            "max_log_files": 10,
            "compression_history": [],
            "recent_input_directories": [],
            "recent_output_directories": [],
            "custom_presets": {},
            "advanced_settings": {
                "thread_count": 0,  # 0 = auto
                "memory_limit": 0,  # 0 = no limit
                "temp_directory": "",  # '' = system temp
                "cleanup_temp_files": True,
            },
        }

    def load(self):
        """Load settings from configuration file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)

                # Merge with defaults
                self.settings = self.get_default_settings()
                self.settings.update(loaded_settings)

                self.logger.info(f"Configuration loaded from {self.config_file}")
            else:
                # Use defaults
                self.settings = self.get_default_settings()
                self.logger.info("Using default configuration")

        except Exception as e:
            self.logger.warning(f"Failed to load configuration: {e}")
            self.settings = self.get_default_settings()

    def save(self):
        """Save current settings to configuration file."""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Configuration saved to {self.config_file}")

        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value.

        Args:
            key: Setting key (supports dot notation for nested keys)
            default: Default value if key not found

        Returns:
            Setting value or default
        """
        keys = key.split(".")
        value = self.settings

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """
        Set a setting value.

        Args:
            key: Setting key (supports dot notation for nested keys)
            value: Value to set
        """
        keys = key.split(".")
        target = self.settings

        # Navigate to parent of target key
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]

        # Set final value
        target[keys[-1]] = value

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = self.get_default_settings()
        self.logger.info("Configuration reset to defaults")

    def add_to_history(
        self, input_file: str, output_file: str, preset: str, success: bool
    ):
        """Add compression operation to history."""
        history = self.get("compression_history", [])

        entry = {
            "timestamp": str(Path().cwd()),  # Using current time would be better
            "input_file": input_file,
            "output_file": output_file,
            "preset": preset,
            "success": success,
        }

        history.append(entry)

        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]

        self.set("compression_history", history)

    def add_recent_directory(self, directory: str, directory_type: str):
        """
        Add directory to recent list.

        Args:
            directory: Directory path
            directory_type: 'input' or 'output'
        """
        key = f"recent_{directory_type}_directories"
        recent = self.get(key, [])

        # Remove if already exists
        if directory in recent:
            recent.remove(directory)

        # Add to front
        recent.insert(0, directory)

        # Keep only last 10
        if len(recent) > 10:
            recent = recent[:10]

        self.set(key, recent)

    def get_recent_directories(self, directory_type: str) -> list:
        """Get list of recent directories."""
        key = f"recent_{directory_type}_directories"
        return self.get(key, [])

    def save_custom_preset(self, name: str, settings: Dict[str, Any]):
        """Save a custom compression preset."""
        custom_presets = self.get("custom_presets", {})
        custom_presets[name] = settings
        self.set("custom_presets", custom_presets)

    def get_custom_presets(self) -> Dict[str, Any]:
        """Get all custom presets."""
        return self.get("custom_presets", {})

    def delete_custom_preset(self, name: str):
        """Delete a custom preset."""
        custom_presets = self.get("custom_presets", {})
        if name in custom_presets:
            del custom_presets[name]
            self.set("custom_presets", custom_presets)

    def get_config_file_path(self) -> str:
        """Get the configuration file path."""
        return str(self.config_file)

    def backup_config(self, backup_path: Optional[str] = None) -> str:
        """
        Create a backup of the configuration file.

        Args:
            backup_path: Path for backup file. If None, creates in same directory.

        Returns:
            Path to backup file
        """
        if backup_path:
            backup_file = Path(backup_path)
        else:
            backup_file = self.config_file.with_suffix(".json.backup")

        try:
            backup_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, "r", encoding="utf-8") as src:
                with open(backup_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

            self.logger.info(f"Configuration backed up to {backup_file}")
            return str(backup_file)

        except Exception as e:
            self.logger.error(f"Failed to backup configuration: {e}")
            raise

    def restore_config(self, backup_path: str):
        """
        Restore configuration from backup.

        Args:
            backup_path: Path to backup file
        """
        backup_file = Path(backup_path)

        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        try:
            with open(backup_file, "r", encoding="utf-8") as src:
                with open(self.config_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

            # Reload settings
            self.load()

            self.logger.info(f"Configuration restored from {backup_path}")

        except Exception as e:
            self.logger.error(f"Failed to restore configuration: {e}")
            raise


# Global config instance
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
