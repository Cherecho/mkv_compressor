"""
Modern GUI application for MKV Video Compressor with improved styling.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD

    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

from ..core import VideoCompressor, CompressionSettings, VideoInfo
from ..utils.logger import setup_logger
from ..utils.config import ConfigManager


class ModernStyle:
    """Modern dark theme with advanced styling."""

    # Dark theme color palette
    PRIMARY_BG = "#1e1e1e"  # Main background
    SECONDARY_BG = "#2d2d2d"  # Secondary panels
    TERTIARY_BG = "#3c3c3c"  # Input fields, buttons
    SURFACE_BG = "#404040"  # Cards, elevated surfaces
    ACCENT_PRIMARY = "#0045A0"  # Primary accent (blue)
    ACCENT_SECONDARY = "#00D4AA"  # Secondary accent (teal)
    ACCENT_HOVER = "#005a9e"  # Hover states
    SUCCESS = "#4CAF50"  # Success green
    WARNING = "#FF9800"  # Warning orange
    ERROR = "#F44336"  # Error red
    TEXT_PRIMARY = "#FFFFFF"  # Primary text
    TEXT_SECONDARY = "#B0B0B0"  # Secondary text
    TEXT_DISABLED = "#666666"  # Disabled text
    BORDER_COLOR = "#555555"  # Borders
    BORDER_FOCUS = "#007ACC"  # Focus borders
    SHADOW_COLOR = "#000000"  # Drop shadows

    @staticmethod
    def configure_styles():
        """Configure modern dark theme styles with advanced effects."""
        style = ttk.Style()

        # Use a modern theme as base
        try:
            style.theme_use("clam")
        except:
            style.theme_use("alt")

        # Configure modern frame styles
        style.configure(
            "Modern.TFrame",
            background=ModernStyle.PRIMARY_BG,
            relief="flat",
            borderwidth=0,
        )

        style.configure(
            "Card.TFrame",
            background=ModernStyle.SURFACE_BG,
            relief="solid",
            borderwidth=1,
            bordercolor=ModernStyle.BORDER_COLOR,
        )

        style.configure(
            "Header.TFrame",
            background=ModernStyle.ACCENT_PRIMARY,
            relief="flat",
            borderwidth=0,
        )

        # Label styles with modern typography
        style.configure(
            "Modern.TLabel",
            background=ModernStyle.PRIMARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9),
        )

        style.configure(
            "Header.TLabel",
            background=ModernStyle.ACCENT_PRIMARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        )

        style.configure(
            "Title.TLabel",
            background=ModernStyle.PRIMARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            background=ModernStyle.PRIMARY_BG,
            foreground=ModernStyle.TEXT_SECONDARY,
            font=("Segoe UI", 9),
        )

        # Modern button styles with hover effects
        style.configure(
            "Modern.TButton",
            background=ModernStyle.TERTIARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            relief="solid",
            bordercolor=ModernStyle.BORDER_COLOR,
            focuscolor="none",
            font=("Segoe UI", 9),
            padding=(12, 8),
        )

        style.map(
            "Modern.TButton",
            background=[
                ("active", ModernStyle.SURFACE_BG),
                ("pressed", ModernStyle.BORDER_COLOR),
            ],
        )

        style.configure(
            "Accent.TButton",
            background=ModernStyle.ACCENT_PRIMARY,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=0,
            relief="flat",
            focuscolor="none",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 10),
        )

        style.map(
            "Accent.TButton",
            background=[
                ("active", ModernStyle.ACCENT_HOVER),
                ("pressed", ModernStyle.ACCENT_HOVER),
            ],
        )

        style.configure(
            "Success.TButton",
            background=ModernStyle.SUCCESS,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=0,
            relief="flat",
            focuscolor="none",
            font=("Segoe UI", 9, "bold"),
            padding=(12, 8),
        )

        # Modern entry styles
        style.configure(
            "Modern.TEntry",
            fieldbackground=ModernStyle.TERTIARY_BG,
            background=ModernStyle.TERTIARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            relief="solid",
            bordercolor=ModernStyle.BORDER_COLOR,
            insertcolor=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9),
            padding=(8, 6),
        )

        style.map(
            "Modern.TEntry",
            bordercolor=[("focus", ModernStyle.BORDER_FOCUS)],
            fieldbackground=[("focus", ModernStyle.SURFACE_BG)],
        )

        # Modern combobox styles
        style.configure(
            "Modern.TCombobox",
            fieldbackground=ModernStyle.TERTIARY_BG,
            background=ModernStyle.TERTIARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            relief="solid",
            bordercolor=ModernStyle.BORDER_COLOR,
            arrowcolor=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9),
            padding=(8, 6),
        )

        style.map(
            "Modern.TCombobox",
            bordercolor=[("focus", ModernStyle.BORDER_FOCUS)],
            fieldbackground=[("focus", ModernStyle.SURFACE_BG)],
        )

        # Modern labelframe styles
        style.configure(
            "Modern.TLabelframe",
            background=ModernStyle.PRIMARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=1,
            relief="solid",
            bordercolor=ModernStyle.BORDER_COLOR,
            labeloutside=False,
        )

        style.configure(
            "Modern.TLabelframe.Label",
            background=ModernStyle.PRIMARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )

        # Modern checkbutton styles
        style.configure(
            "Modern.TCheckbutton",
            background=ModernStyle.PRIMARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            focuscolor="none",
            font=("Segoe UI", 9),
        )

        # Modern treeview styles
        style.configure(
            "Modern.Treeview",
            background=ModernStyle.TERTIARY_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            fieldbackground=ModernStyle.TERTIARY_BG,
            borderwidth=1,
            relief="solid",
            bordercolor=ModernStyle.BORDER_COLOR,
            font=("Segoe UI", 9),
            rowheight=28,
        )

        style.configure(
            "Modern.Treeview.Heading",
            background=ModernStyle.SURFACE_BG,
            foreground=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
        )

        style.map(
            "Modern.Treeview",
            background=[("selected", ModernStyle.ACCENT_PRIMARY)],
            foreground=[("selected", ModernStyle.TEXT_PRIMARY)],
        )

        # Modern progress bar with gradient effect
        style.configure(
            "Modern.Horizontal.TProgressbar",
            background=ModernStyle.ACCENT_PRIMARY,
            troughcolor=ModernStyle.TERTIARY_BG,
            borderwidth=1,
            relief="solid",
            bordercolor=ModernStyle.BORDER_COLOR,
            lightcolor=ModernStyle.ACCENT_PRIMARY,
            darkcolor=ModernStyle.ACCENT_SECONDARY,
        )

        # Modern notebook styles
        style.configure(
            "Modern.TNotebook", background=ModernStyle.PRIMARY_BG, borderwidth=0
        )

        style.configure(
            "Modern.TNotebook.Tab",
            background=ModernStyle.SECONDARY_BG,
            foreground=ModernStyle.TEXT_SECONDARY,
            borderwidth=1,
            relief="solid",
            bordercolor=ModernStyle.BORDER_COLOR,
            font=("Segoe UI", 9),
            padding=(16, 10),
        )

        style.map(
            "Modern.TNotebook.Tab",
            background=[
                ("selected", ModernStyle.ACCENT_PRIMARY),
                ("active", ModernStyle.SURFACE_BG),
            ],
            foreground=[
                ("selected", ModernStyle.TEXT_PRIMARY),
                ("active", ModernStyle.TEXT_PRIMARY),
            ],
        )

        # Modern scrollbar styles
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=ModernStyle.TERTIARY_BG,
            troughcolor=ModernStyle.SECONDARY_BG,
            borderwidth=0,
            arrowcolor=ModernStyle.TEXT_SECONDARY,
            relief="flat",
        )

        style.map(
            "Modern.Vertical.TScrollbar",
            background=[("active", ModernStyle.SURFACE_BG)],
        )


class GlassEffect:
    """Glass morphism effects for modern UI."""

    @staticmethod
    def create_glass_frame(parent, **kwargs):
        """Create a frame with glass morphism effect."""
        frame = tk.Frame(
            parent,
            bg=ModernStyle.SURFACE_BG,
            relief="flat",
            bd=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1,
            **kwargs,
        )
        return frame

    @staticmethod
    def create_gradient_label(parent, text, **kwargs):
        """Create a label with gradient-like effect using color transition."""
        label = tk.Label(
            parent,
            text=text,
            bg=ModernStyle.PRIMARY_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9),
            **kwargs,
        )
        return label


class ProgressWindow:
    """Modern progress window with improved styling."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("🎬 Compression Progress")
        self.window.geometry("750x550")
        self.window.resizable(True, True)
        self.window.configure(bg=ModernStyle.PRIMARY_BG)

        # Modern window effects
        try:
            self.window.wm_attributes("-alpha", 0.97)  # Slight transparency
        except:
            pass

        # Center window and make it modal
        self.window.transient(parent)
        self.window.grab_set()
        self._center_window()

        self.setup_ui()
        self.is_cancelled = False

    def _center_window(self):
        """Center the window on the screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        """Setup modern dark-themed progress window UI."""
        # Header section with gradient-like effect
        header_frame = GlassEffect.create_glass_frame(self.window)
        header_frame.configure(bg=ModernStyle.ACCENT_PRIMARY, bd=0)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=0, pady=0)
        header_frame.columnconfigure(1, weight=1)

        # Modern title with icon
        title_label = tk.Label(
            header_frame,
            text="🎬 Video Compression",
            bg=ModernStyle.ACCENT_PRIMARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky=tk.W, padx=20, pady=15)

        # Status indicator
        self.status_indicator = tk.Label(
            header_frame,
            text="●",
            bg=ModernStyle.ACCENT_PRIMARY,
            fg=ModernStyle.SUCCESS,
            font=("Segoe UI", 14),
        )
        self.status_indicator.grid(row=0, column=1, sticky=tk.E, padx=20, pady=15)

        # Main content area with modern styling
        main_frame = GlassEffect.create_glass_frame(self.window)
        main_frame.configure(bg=ModernStyle.PRIMARY_BG, bd=0)
        main_frame.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20
        )

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Current file info with modern card design
        info_card = GlassEffect.create_glass_frame(main_frame)
        info_card.configure(
            bg=ModernStyle.SURFACE_BG,
            relief="flat",
            bd=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1,
        )
        info_card.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        info_card.columnconfigure(1, weight=1)

        file_icon = tk.Label(
            info_card,
            text="📁",
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.ACCENT_SECONDARY,
            font=("Segoe UI", 12),
        )
        file_icon.grid(row=0, column=0, sticky=tk.W, padx=15, pady=15)

        file_info_frame = tk.Frame(info_card, bg=ModernStyle.SURFACE_BG)
        file_info_frame.grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15), pady=15
        )
        file_info_frame.columnconfigure(0, weight=1)

        file_label = tk.Label(
            file_info_frame,
            text="Processing File:",
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.TEXT_SECONDARY,
            font=("Segoe UI", 9),
        )
        file_label.grid(row=0, column=0, sticky=tk.W)

        self.current_file_var = tk.StringVar(value="Preparing...")
        current_file_label = tk.Label(
            file_info_frame,
            textvariable=self.current_file_var,
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )
        current_file_label.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Progress section with modern design
        progress_card = GlassEffect.create_glass_frame(main_frame)
        progress_card.configure(
            bg=ModernStyle.SURFACE_BG,
            relief="flat",
            bd=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1,
        )
        progress_card.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_card.columnconfigure(0, weight=1)

        # Progress header
        progress_header = tk.Frame(progress_card, bg=ModernStyle.SURFACE_BG)
        progress_header.grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=15, pady=(15, 5)
        )
        progress_header.columnconfigure(1, weight=1)

        progress_icon = tk.Label(
            progress_header,
            text="⚡",
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.ACCENT_SECONDARY,
            font=("Segoe UI", 12),
        )
        progress_icon.grid(row=0, column=0, sticky=tk.W)

        progress_title = tk.Label(
            progress_header,
            text="Compression Progress",
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
        )
        progress_title.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        # Modern progress bar with custom styling
        progress_container = tk.Frame(progress_card, bg=ModernStyle.SURFACE_BG)
        progress_container.grid(
            row=1, column=0, sticky=(tk.W, tk.E), padx=15, pady=(0, 10)
        )
        progress_container.columnconfigure(0, weight=1)

        # Create custom progress bar background
        self.progress_bg = tk.Frame(
            progress_container,
            bg=ModernStyle.TERTIARY_BG,
            height=8,
            relief="flat",
            bd=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1,
        )
        self.progress_bg.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        self.progress_bg.grid_propagate(False)

        # Progress fill
        self.progress_fill = tk.Frame(
            self.progress_bg, bg=ModernStyle.ACCENT_PRIMARY, height=6, relief="flat"
        )
        self.progress_fill.place(x=1, y=1, height=6, width=1)

        # Progress text with modern typography
        self.progress_text_var = tk.StringVar(value="0% - Starting...")
        progress_label = tk.Label(
            progress_container,
            textvariable=self.progress_text_var,
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )
        progress_label.grid(row=1, column=0, sticky=tk.W)

        # Activity log section with modern card design
        log_card = GlassEffect.create_glass_frame(main_frame)
        log_card.configure(
            bg=ModernStyle.SURFACE_BG,
            relief="flat",
            bd=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1,
        )
        log_card.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        log_card.columnconfigure(0, weight=1)
        log_card.rowconfigure(1, weight=1)

        # Log header
        log_header = tk.Frame(log_card, bg=ModernStyle.SURFACE_BG)
        log_header.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=15, pady=(15, 10))

        log_icon = tk.Label(
            log_header,
            text="📋",
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.ACCENT_SECONDARY,
            font=("Segoe UI", 12),
        )
        log_icon.grid(row=0, column=0, sticky=tk.W)

        log_title = tk.Label(
            log_header,
            text="Activity Log",
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
        )
        log_title.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        # Modern log text area
        log_container = tk.Frame(
            log_card,
            bg=ModernStyle.TERTIARY_BG,
            relief="flat",
            bd=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1,
        )
        log_container.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=(0, 15)
        )
        log_container.columnconfigure(0, weight=1)
        log_container.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_container,
            height=8,
            width=70,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg=ModernStyle.TERTIARY_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            selectbackground=ModernStyle.ACCENT_PRIMARY,
            selectforeground=ModernStyle.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            padx=12,
            pady=8,
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Modern button section
        button_card = GlassEffect.create_glass_frame(main_frame)
        button_card.configure(
            bg=ModernStyle.SURFACE_BG,
            relief="flat",
            bd=1,
            highlightbackground=ModernStyle.BORDER_COLOR,
            highlightthickness=1,
        )
        button_card.grid(row=3, column=0, sticky=(tk.W, tk.E))
        button_card.columnconfigure(0, weight=1)

        button_container = tk.Frame(button_card, bg=ModernStyle.SURFACE_BG)
        button_container.grid(row=0, column=0, sticky=tk.E, padx=15, pady=15)

        # Modern styled buttons
        self.cancel_button = tk.Button(
            button_container,
            text="❌ Cancel",
            command=self.cancel_compression,
            bg=ModernStyle.ERROR,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.cancel_button.grid(row=0, column=0, padx=(0, 10))

        self.close_button = tk.Button(
            button_container,
            text="✅ Close",
            command=self.close_window,
            state=tk.DISABLED,
            bg=ModernStyle.SUCCESS,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.close_button.grid(row=0, column=1)

    def update_progress(self, percentage: float, message: str = ""):
        """Update custom progress bar and text with modern animations."""
        # Update custom progress bar fill
        try:
            # Calculate progress bar width based on container width
            self.progress_bg.update_idletasks()
            container_width = self.progress_bg.winfo_width()
            if container_width > 2:  # Ensure container is rendered
                progress_width = max(1, int((container_width - 2) * (percentage / 100)))
                self.progress_fill.place(x=1, y=1, height=6, width=progress_width)

                # Color transition based on progress
                if percentage < 30:
                    color = ModernStyle.WARNING
                elif percentage < 70:
                    color = ModernStyle.ACCENT_SECONDARY
                else:
                    color = ModernStyle.SUCCESS

                self.progress_fill.configure(bg=color)
        except:
            pass

        # Update status indicator
        if percentage < 100:
            self.status_indicator.configure(fg=ModernStyle.WARNING, text="●")
        else:
            self.status_indicator.configure(fg=ModernStyle.SUCCESS, text="●")

        # Update progress text
        if message:
            self.progress_text_var.set(f"{percentage:.1f}% - {message}")
        else:
            self.progress_text_var.set(f"{percentage:.1f}%")
        self.window.update_idletasks()

    def update_current_file(self, filename: str):
        """Update current file being processed."""
        self.current_file_var.set(f"Processing: {filename}")
        self.window.update_idletasks()

    def add_log(self, message: str):
        """Add message to log area with modern styling."""
        self.log_text.config(state=tk.NORMAL)

        # Add timestamp
        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        # Style different message types
        if "✓" in message or "Completed" in message:
            color_tag = "success"
        elif "✗" in message or "Failed" in message or "Error" in message:
            color_tag = "error"
        elif "⚠" in message or "Warning" in message:
            color_tag = "warning"
        else:
            color_tag = "info"

        # Configure text tags for colors
        self.log_text.tag_configure("success", foreground=ModernStyle.SUCCESS)
        self.log_text.tag_configure("error", foreground=ModernStyle.ERROR)
        self.log_text.tag_configure("warning", foreground=ModernStyle.WARNING)
        self.log_text.tag_configure("info", foreground=ModernStyle.TEXT_SECONDARY)
        self.log_text.tag_configure("timestamp", foreground=ModernStyle.TEXT_DISABLED)

        # Insert timestamp
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        # Insert message with appropriate color
        self.log_text.insert(tk.END, f"{message}\n", color_tag)

        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.window.update_idletasks()

    def compression_finished(self, success: bool = True):
        """Mark compression as finished with modern styling updates."""
        # Update button states for tk.Button
        self.cancel_button.configure(state=tk.DISABLED, bg=ModernStyle.BORDER_COLOR)
        self.close_button.configure(state=tk.NORMAL, bg=ModernStyle.SUCCESS)

        # Update status indicator
        if success:
            self.status_indicator.configure(fg=ModernStyle.SUCCESS, text="●")
            self.progress_text_var.set("100% - Completed successfully!")
            self.add_log("✓ All compressions completed successfully!")
            # Update progress bar to show completion
            self.update_progress(100, "Completed successfully!")
        else:
            self.status_indicator.configure(fg=ModernStyle.ERROR, text="●")
            self.progress_text_var.set("Compression failed or cancelled")
            self.add_log("✗ Compression failed or was cancelled.")
            # Show error state in progress bar
            try:
                self.progress_fill.configure(bg=ModernStyle.ERROR)
            except:
                pass

    def cancel_compression(self):
        """Cancel the compression process."""
        self.is_cancelled = True
        self.add_log("Cancelling compression...")

    def close_window(self):
        """Close the progress window."""
        self.window.destroy()


class CompressorGUI:
    """Modern GUI application for the MKV Video Compressor."""

    def __init__(self):
        # Initialize logging
        self.logger = setup_logger()

        # Initialize configuration
        self.config_manager = ConfigManager()

        # Initialize video compressor
        self.compressor = VideoCompressor()

        # Initialize GUI with modern dark styling
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()

        self.root.title("🎬 MKV Video Compressor Pro")
        self.root.geometry("1100x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=ModernStyle.PRIMARY_BG)

        # Configure window attributes for modern look
        try:
            # Enable transparency and modern window effects (Windows 10/11)
            self.root.wm_attributes("-alpha", 0.98)  # Slight transparency
            # For Windows: enable modern window styling
            if hasattr(self.root, "wm_attributes"):
                try:
                    self.root.wm_attributes("-transparentcolor", "")
                except:
                    pass
        except:
            pass

        # Configure modern styles
        ModernStyle.configure_styles()

        # Set modern window icon if available
        try:
            # Create a modern icon programmatically or load from file
            pass
        except:
            pass

        # Variables
        self.input_files: List[str] = []
        self.output_directory = tk.StringVar()
        self.selected_preset = tk.StringVar(value="Balanced")

        # Load settings
        self.load_settings()

        # Setup modern UI
        self.setup_ui()

        # Setup logging handler for GUI
        self.setup_log_handler()

    def setup_ui(self):
        """Setup the modern user interface."""
        # Main container with padding
        main_container = ttk.Frame(self.root, style="Modern.TFrame", padding="0")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)  # Main container gets all the space
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)

        # Header section
        self.create_header(main_container)

        # Create modern dark notebook for tabs
        self.notebook = ttk.Notebook(main_container, style="Modern.TNotebook")
        self.notebook.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=(0, 15)
        )

        # Main compression tab
        self.main_frame = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(self.main_frame, text="🎬 Compression")
        self.setup_main_tab()

        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.settings_frame.columnconfigure(0, weight=1)
        self.settings_frame.rowconfigure(0, weight=1)
        self.notebook.add(self.settings_frame, text="⚙️ Settings")
        self.setup_settings_tab()

        # About tab
        self.about_frame = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.about_frame.columnconfigure(0, weight=1)
        self.about_frame.rowconfigure(0, weight=1)
        self.notebook.add(self.about_frame, text="ℹ️ About")
        self.setup_about_tab()

        # Status bar
        self.setup_status_bar()

    def create_header(self, parent):
        """Create modern dark header section with gradient effect."""
        header_frame = GlassEffect.create_glass_frame(parent)
        header_frame.configure(bg=ModernStyle.ACCENT_PRIMARY, bd=0)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=0, pady=0)
        header_frame.columnconfigure(1, weight=1)

        # App icon/title with modern styling
        title_label = tk.Label(
            header_frame,
            text="🎬 MKV Video Compressor Pro",
            bg=ModernStyle.ACCENT_PRIMARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 18, "bold"),
        )
        title_label.grid(row=0, column=0, sticky=tk.W, padx=25, pady=20)

        # Version and status info
        info_frame = tk.Frame(header_frame, bg=ModernStyle.ACCENT_PRIMARY)
        info_frame.grid(row=0, column=1, sticky=tk.E, padx=25, pady=20)

        version_label = tk.Label(
            info_frame,
            text="v1.1.0",
            bg=ModernStyle.ACCENT_PRIMARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 10),
        )
        version_label.grid(row=0, column=0, sticky=tk.E)

        status_label = tk.Label(
            info_frame,
            text="● Ready",
            bg=ModernStyle.ACCENT_PRIMARY,
            fg=ModernStyle.SUCCESS,
            font=("Segoe UI", 9),
        )
        status_label.grid(row=1, column=0, sticky=tk.E)

    def setup_main_tab(self):
        """Setup the modern main compression tab."""
        # Main container with padding
        main_container = ttk.Frame(self.main_frame, style="Modern.TFrame", padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        main_container.columnconfigure(0, weight=1)

        # Input files section with modern styling
        input_section = ttk.LabelFrame(
            main_container,
            text="📁 Input Video Files",
            style="Modern.TLabelframe",
            padding="15",
        )
        input_section.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15)
        )
        input_section.columnconfigure(0, weight=1)
        input_section.rowconfigure(1, weight=1)

        # File selection buttons
        file_button_frame = ttk.Frame(input_section, style="Modern.TFrame")
        file_button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Button(
            file_button_frame,
            text="📁 Add Files",
            command=self.add_files,
            style="Modern.TButton",
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(
            file_button_frame,
            text="📂 Add Folder",
            command=self.add_folder,
            style="Modern.TButton",
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(
            file_button_frame,
            text="🗑️ Remove Selected",
            command=self.remove_selected,
            style="Modern.TButton",
        ).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(
            file_button_frame,
            text="🧹 Clear All",
            command=self.clear_all,
            style="Modern.TButton",
        ).pack(side=tk.LEFT)

        # File list container
        list_container = ttk.Frame(input_section, style="Modern.TFrame")
        list_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)

        # Modern file listbox with styling
        listbox_frame = ttk.Frame(list_container, relief="solid", borderwidth=1)
        listbox_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5)
        )
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.EXTENDED,
            font=("Segoe UI", 9),
            bg=ModernStyle.TERTIARY_BG,
            fg=ModernStyle.TEXT_PRIMARY,
            selectbackground=ModernStyle.ACCENT_PRIMARY,
            selectforeground=ModernStyle.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            activestyle="none",
        )
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar for listbox
        listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        listbox_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.config(yscrollcommand=listbox_scrollbar.set)
        listbox_scrollbar.config(command=self.file_listbox.yview)

        # Drag and drop support
        if DND_AVAILABLE:
            self.file_listbox.drop_target_register(DND_FILES)
            self.file_listbox.dnd_bind("<<Drop>>", self.on_drop)

            # Add drop instruction
            tip_label = ttk.Label(
                input_section,
                text="💡 Tip: You can also drag and drop files here!",
                style="Modern.TLabel",
                font=("Segoe UI", 8),
            )
            tip_label.grid(row=2, column=0, sticky=tk.W, pady=(8, 0))

        # Output directory section
        output_section = ttk.LabelFrame(
            main_container,
            text="📁 Output Directory",
            style="Modern.TLabelframe",
            padding="15",
        )
        output_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        output_section.columnconfigure(0, weight=1)

        output_entry_frame = ttk.Frame(output_section, style="Modern.TFrame")
        output_entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        output_entry_frame.columnconfigure(0, weight=1)

        self.output_entry = ttk.Entry(
            output_entry_frame,
            textvariable=self.output_directory,
            state="readonly",
            style="Modern.TEntry",
        )
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        ttk.Button(
            output_entry_frame,
            text="🔍 Browse",
            command=self.browse_output_directory,
            style="Modern.TButton",
        ).grid(row=0, column=1)

        # Compression settings section
        settings_section = ttk.LabelFrame(
            main_container,
            text="⚙️ Compression Settings",
            style="Modern.TLabelframe",
            padding="15",
        )
        settings_section.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        settings_section.columnconfigure(1, weight=1)

        # Preset selection
        preset_frame = ttk.Frame(settings_section, style="Modern.TFrame")
        preset_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        preset_frame.columnconfigure(1, weight=1)

        ttk.Label(preset_frame, text="🎨 Preset:", style="Modern.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )

        self.preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.selected_preset,
            values=list(self.compressor.get_compression_presets().keys()),
            state="readonly",
            style="Modern.TCombobox",
            width=20,
        )
        self.preset_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_changed)

        ttk.Button(
            preset_frame,
            text="🔧 Custom Settings",
            command=self.show_custom_settings,
            style="Modern.TButton",
        ).grid(row=0, column=2, sticky=tk.E)

        # Quick info about selected preset
        self.preset_info_var = tk.StringVar()
        self.preset_info_label = ttk.Label(
            settings_section,
            textvariable=self.preset_info_var,
            style="Modern.TLabel",
            font=("Segoe UI", 8),
        )
        self.preset_info_label.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0)
        )
        self.update_preset_info()

        # Control buttons section
        control_section = ttk.Frame(main_container, style="Modern.TFrame")
        control_section.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        control_section.columnconfigure(0, weight=1)

        # Button frame aligned to the right
        button_container = ttk.Frame(control_section, style="Modern.TFrame")
        button_container.grid(row=0, column=0, sticky=tk.E)

        ttk.Button(
            button_container,
            text="👀 Preview Settings",
            command=self.preview_settings,
            style="Modern.TButton",
        ).grid(row=0, column=0, padx=(0, 10))

        self.start_button = ttk.Button(
            button_container,
            text="🚀 Start Compression",
            command=self.start_compression,
            style="Accent.TButton",
        )
        self.start_button.grid(row=0, column=1)

    def setup_settings_tab(self):
        """Setup the modern settings tab."""
        # Main container with padding
        settings_container = ttk.Frame(
            self.settings_frame, style="Modern.TFrame", padding="20"
        )
        settings_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        settings_container.columnconfigure(0, weight=1)

        # General settings section
        general_section = ttk.LabelFrame(
            settings_container,
            text="⚙️ General Settings",
            style="Modern.TLabelframe",
            padding="15",
        )
        general_section.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        general_section.columnconfigure(1, weight=1)

        # FFmpeg path
        ttk.Label(general_section, text="📁 FFmpeg Path:", style="Modern.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 10)
        )

        self.ffmpeg_path_var = tk.StringVar(
            value=self.config_manager.get("ffmpeg_path", "")
        )

        ffmpeg_entry_frame = ttk.Frame(general_section, style="Modern.TFrame")
        ffmpeg_entry_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        ffmpeg_entry_frame.columnconfigure(0, weight=1)

        ffmpeg_entry = ttk.Entry(
            ffmpeg_entry_frame, textvariable=self.ffmpeg_path_var, style="Modern.TEntry"
        )
        ffmpeg_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        ttk.Button(
            ffmpeg_entry_frame,
            text="🔍 Browse",
            command=self.browse_ffmpeg_path,
            style="Modern.TButton",
        ).grid(row=0, column=1)

        # Default output directory
        ttk.Label(
            general_section, text="📂 Default Output Directory:", style="Modern.TLabel"
        ).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 10))

        self.default_output_var = tk.StringVar(
            value=self.config_manager.get("default_output_dir", "")
        )

        default_output_frame = ttk.Frame(general_section, style="Modern.TFrame")
        default_output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        default_output_frame.columnconfigure(0, weight=1)

        default_output_entry = ttk.Entry(
            default_output_frame,
            textvariable=self.default_output_var,
            style="Modern.TEntry",
        )
        default_output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        ttk.Button(
            default_output_frame,
            text="🔍 Browse",
            command=self.browse_default_output,
            style="Modern.TButton",
        ).grid(row=0, column=1)

        # Options section
        options_section = ttk.LabelFrame(
            settings_container,
            text="🔧 Options",
            style="Modern.TLabelframe",
            padding="15",
        )
        options_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # Checkboxes for various settings
        self.overwrite_files_var = tk.BooleanVar(
            value=self.config_manager.get("overwrite_files", False)
        )
        ttk.Checkbutton(
            options_section,
            text="🔄 Overwrite existing files",
            variable=self.overwrite_files_var,
            style="Modern.TCheckbutton",
        ).grid(row=0, column=0, sticky=tk.W, pady=2)

        self.show_notifications_var = tk.BooleanVar(
            value=self.config_manager.get("show_notifications", True)
        )
        ttk.Checkbutton(
            options_section,
            text="🔔 Show completion notifications",
            variable=self.show_notifications_var,
            style="Modern.TCheckbutton",
        ).grid(row=1, column=0, sticky=tk.W, pady=2)

        self.auto_open_output_var = tk.BooleanVar(
            value=self.config_manager.get("auto_open_output", False)
        )
        ttk.Checkbutton(
            options_section,
            text="📂 Open output folder when complete",
            variable=self.auto_open_output_var,
            style="Modern.TCheckbutton",
        ).grid(row=2, column=0, sticky=tk.W, pady=2)

        # Save settings button
        save_button_frame = ttk.Frame(settings_container, style="Modern.TFrame")
        save_button_frame.grid(row=2, column=0, sticky=tk.E, pady=(10, 0))

        ttk.Button(
            save_button_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            style="Accent.TButton",
        ).grid(row=0, column=0)

    def setup_about_tab(self):
        """Setup the modern about tab."""
        # Main container with padding
        about_container = ttk.Frame(
            self.about_frame, style="Modern.TFrame", padding="30"
        )
        about_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        about_container.columnconfigure(0, weight=1)

        # App info section
        info_section = ttk.Frame(about_container, style="Modern.TFrame")
        info_section.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        info_section.columnconfigure(0, weight=1)

        # App title and version
        title_label = ttk.Label(
            info_section,
            text="🎬 MKV Video Compressor Pro",
            style="Title.TLabel",
            font=("Segoe UI", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        version_label = ttk.Label(
            info_section,
            text="Version 1.1.0",
            style="Modern.TLabel",
            font=("Segoe UI", 10),
        )
        version_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 15))

        # Description
        desc_text = "A professional video compression tool for MKV files with modern interface and advanced features."
        desc_label = ttk.Label(
            info_section,
            text=desc_text,
            style="Modern.TLabel",
            font=("Segoe UI", 10),
            wraplength=600,
        )
        desc_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        # Features section
        features_section = ttk.LabelFrame(
            about_container, text="✨ Features", style="Modern.TLabelframe", padding="15"
        )
        features_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        features_text = """• High-quality video compression using FFmpeg
• Multiple compression presets (Fast, Balanced, High Quality, Custom)
• Batch processing support for multiple files
• Modern drag-and-drop interface
• Real-time progress monitoring with dynamic updates
• Custom compression settings and advanced options
• Cross-platform support (Windows, macOS, Linux)"""

        features_label = ttk.Label(
            features_section,
            text=features_text,
            style="Modern.TLabel",
            font=("Segoe UI", 9),
            justify=tk.LEFT,
        )
        features_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Requirements section
        req_section = ttk.LabelFrame(
            about_container,
            text="📋 Requirements",
            style="Modern.TLabelframe",
            padding="15",
        )
        req_section.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        req_text = """• FFmpeg must be installed and available in PATH
• Python 3.8 or higher
• Supported input formats: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V
• Output format: MKV (Matroska Video)"""

        req_label = ttk.Label(
            req_section,
            text=req_text,
            style="Modern.TLabel",
            font=("Segoe UI", 9),
            justify=tk.LEFT,
        )
        req_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Credits section
        credits_section = ttk.LabelFrame(
            about_container,
            text="👨‍💻 Credits",
            style="Modern.TLabelframe",
            padding="15",
        )
        credits_section.grid(row=3, column=0, sticky=(tk.W, tk.E))

        credits_text = "Created with Python, tkinter, and FFmpeg.\nBuilt with ❤️ for video enthusiasts."
        credits_label = ttk.Label(
            credits_section,
            text=credits_text,
            style="Modern.TLabel",
            font=("Segoe UI", 9),
            justify=tk.CENTER,
        )
        credits_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def setup_status_bar(self):
        """Setup the modern status bar."""
        self.status_bar = ttk.Frame(self.root, style="Modern.TFrame", padding="5")
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            self.status_bar, textvariable=self.status_var, style="Modern.TLabel"
        )
        status_label.grid(row=0, column=0, sticky=tk.W, padx=10)

    def setup_log_handler(self):
        """Setup logging handler to display logs in GUI."""

        class GUILogHandler(logging.Handler):
            def __init__(self, gui):
                super().__init__()
                self.gui = gui

            def emit(self, record):
                # This will be used when progress window is open
                pass

        handler = GUILogHandler(self)
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def load_settings(self):
        """Load settings from configuration."""
        # Set default output directory if specified
        default_output = self.config_manager.get("default_output_dir", "")
        if default_output and os.path.exists(default_output):
            self.output_directory.set(default_output)

    def save_settings(self):
        """Save current settings to configuration."""
        settings = {
            "ffmpeg_path": self.ffmpeg_path_var.get(),
            "default_output_dir": self.default_output_var.get(),
            "overwrite_files": self.overwrite_files_var.get(),
            "show_notifications": self.show_notifications_var.get(),
            "auto_open_output": self.auto_open_output_var.get(),
        }

        for key, value in settings.items():
            self.config_manager.set(key, value)

        self.config_manager.save()
        messagebox.showinfo("Settings", "Settings saved successfully!")

    def add_files(self):
        """Add video files to the input list."""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("All files", "*.*"),
        ]

        files = filedialog.askopenfilenames(
            title="Select Video Files", filetypes=filetypes
        )

        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))

        self.update_status(f"{len(self.input_files)} files selected")

    def add_folder(self):
        """Add all video files from a folder."""
        folder = filedialog.askdirectory(title="Select Folder with Video Files")
        if not folder:
            return

        video_extensions = {
            ".mp4",
            ".avi",
            ".mov",
            ".mkv",
            ".wmv",
            ".flv",
            ".webm",
            ".m4v",
        }
        added_count = 0

        for root, dirs, files in os.walk(folder):
            for file in files:
                if Path(file).suffix.lower() in video_extensions:
                    full_path = os.path.join(root, file)
                    if full_path not in self.input_files:
                        self.input_files.append(full_path)
                        self.file_listbox.insert(tk.END, file)
                        added_count += 1

        self.update_status(f"Added {added_count} files from folder")

    def remove_selected(self):
        """Remove selected files from the input list."""
        selected_indices = list(self.file_listbox.curselection())
        selected_indices.reverse()  # Remove from end to start

        for index in selected_indices:
            self.file_listbox.delete(index)
            del self.input_files[index]

        self.update_status(f"{len(self.input_files)} files remaining")

    def clear_all(self):
        """Clear all files from the input list."""
        self.input_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_status("All files cleared")

    def on_drop(self, event):
        """Handle drag and drop of files."""
        files = self.root.tk.splitlist(event.data)
        added_count = 0

        for file in files:
            if os.path.isfile(file):
                # Check if it's a video file
                video_extensions = {
                    ".mp4",
                    ".avi",
                    ".mov",
                    ".mkv",
                    ".wmv",
                    ".flv",
                    ".webm",
                    ".m4v",
                }
                if Path(file).suffix.lower() in video_extensions:
                    if file not in self.input_files:
                        self.input_files.append(file)
                        self.file_listbox.insert(tk.END, os.path.basename(file))
                        added_count += 1
            elif os.path.isdir(file):
                # Add video files from directory
                video_extensions = {
                    ".mp4",
                    ".avi",
                    ".mov",
                    ".mkv",
                    ".wmv",
                    ".flv",
                    ".webm",
                    ".m4v",
                }
                for root, dirs, dir_files in os.walk(file):
                    for dir_file in dir_files:
                        if Path(dir_file).suffix.lower() in video_extensions:
                            full_path = os.path.join(root, dir_file)
                            if full_path not in self.input_files:
                                self.input_files.append(full_path)
                                self.file_listbox.insert(tk.END, dir_file)
                                added_count += 1

        self.update_status(f"Added {added_count} files via drag and drop")

    def browse_output_directory(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)

    def browse_ffmpeg_path(self):
        """Browse for FFmpeg executable."""
        filename = filedialog.askopenfilename(
            title="Select FFmpeg Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
        )
        if filename:
            self.ffmpeg_path_var.set(filename)

    def browse_default_output(self):
        """Browse for default output directory."""
        directory = filedialog.askdirectory(title="Select Default Output Directory")
        if directory:
            self.default_output_var.set(directory)

    def on_preset_changed(self, event=None):
        """Handle preset selection change."""
        self.update_preset_info()

    def update_preset_info(self):
        """Update preset information display."""
        preset_name = self.selected_preset.get()
        presets = self.compressor.get_compression_presets()

        if preset_name in presets:
            settings = presets[preset_name]
            info = f"CRF: {settings.crf}, Preset: {settings.preset}, Audio: {settings.audio_bitrate}"
            if settings.width and settings.height:
                info += f", Resolution: {settings.width}x{settings.height}"
            self.preset_info_var.set(info)

    def show_custom_settings(self):
        """Show custom settings dialog."""
        messagebox.showinfo(
            "Custom Settings",
            "Custom settings dialog not implemented yet.\nThis would allow fine-tuning of compression parameters.",
        )

    def preview_settings(self):
        """Preview the current compression settings."""
        if not self.input_files:
            messagebox.showwarning("No Files", "Please add some video files first.")
            return

        preset_name = self.selected_preset.get()
        presets = self.compressor.get_compression_presets()
        settings = presets[preset_name]

        # Get info about first file
        try:
            video_info = self.compressor.get_video_info(self.input_files[0])

            preview_text = f"""Compression Preview
            
Selected Preset: {preset_name}

Current Settings:
• Video Codec: {settings.video_codec}
• CRF (Quality): {settings.crf} (lower = better quality)
• Encoding Speed: {settings.preset}
• Audio Codec: {settings.audio_codec}
• Audio Bitrate: {settings.audio_bitrate}

First File Analysis:
• Filename: {video_info.filename}
• Current Size: {video_info.size_mb:.1f} MB
• Resolution: {video_info.resolution}
• Duration: {video_info.duration:.1f} seconds
• Current Codec: {video_info.video_codec}

Output: MKV format
Files to process: {len(self.input_files)}
"""

            messagebox.showinfo("Settings Preview", preview_text)

        except Exception as e:
            messagebox.showerror("Preview Error", f"Failed to analyze video file:\n{e}")

    def start_compression(self):
        """Start the compression process."""
        # Validate inputs
        if not self.input_files:
            messagebox.showwarning(
                "No Files", "Please add some video files to compress."
            )
            return

        if not self.output_directory.get():
            messagebox.showwarning(
                "No Output Directory", "Please select an output directory."
            )
            return

        # Confirm start
        response = messagebox.askyesno(
            "Start Compression",
            f"Start compressing {len(self.input_files)} file(s)?\n\nThis may take a while depending on file sizes.",
        )

        if not response:
            return

        # Disable start button
        self.start_button.config(state=tk.DISABLED)

        # Start compression in separate thread
        threading.Thread(target=self._compression_worker, daemon=True).start()

    def _compression_worker(self):
        """Worker thread for compression process."""
        progress_window = ProgressWindow(self.root)

        try:
            # Get compression settings
            preset_name = self.selected_preset.get()
            presets = self.compressor.get_compression_presets()
            settings = presets[preset_name]

            output_dir = self.output_directory.get()
            overwrite = self.overwrite_files_var.get()

            total_files = len(self.input_files)
            successful = 0

            for i, input_file in enumerate(self.input_files):
                if progress_window.is_cancelled:
                    break

                try:
                    # Update progress window
                    filename = os.path.basename(input_file)
                    progress_window.update_current_file(filename)
                    progress_window.add_log(f"Starting: {filename}")

                    # Generate output filename
                    name, _ = os.path.splitext(filename)
                    output_file = os.path.join(output_dir, f"{name}_compressed.mkv")

                    # Setup progress callback
                    def progress_callback(percentage):
                        overall_progress = ((i + percentage / 100) / total_files) * 100
                        progress_window.update_progress(
                            overall_progress, f"File {i+1}/{total_files}"
                        )

                    # Compress video
                    success = self.compressor.compress_video(
                        input_file,
                        output_file,
                        settings,
                        progress_callback=progress_callback,
                        overwrite=overwrite,
                    )

                    if success:
                        successful += 1
                        progress_window.add_log(f"✓ Completed: {filename}")
                        # Ensure progress shows 100% for this file
                        overall_progress = ((i + 1) / total_files) * 100
                        progress_window.update_progress(
                            overall_progress, f"File {i+1}/{total_files} completed"
                        )
                    else:
                        progress_window.add_log(f"✗ Failed: {filename}")

                except Exception as e:
                    progress_window.add_log(f"✗ Error processing {filename}: {e}")

            # Compression finished
            if not progress_window.is_cancelled:
                progress_window.update_progress(100, "All files processed")
                progress_window.compression_finished(successful > 0)

                # Show notification if enabled
                if self.show_notifications_var.get():
                    if successful == total_files:
                        messagebox.showinfo(
                            "Compression Complete",
                            f"All {total_files} files compressed successfully!",
                        )
                    else:
                        messagebox.showwarning(
                            "Compression Complete",
                            f"{successful}/{total_files} files compressed successfully.",
                        )

                # Open output folder if enabled
                if self.auto_open_output_var.get() and successful > 0:
                    os.startfile(output_dir)

        except Exception as e:
            progress_window.add_log(f"Critical error: {e}")
            progress_window.compression_finished(False)
            messagebox.showerror("Compression Error", f"An error occurred:\n{e}")

        finally:
            # Re-enable start button
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))

    def update_status(self, message: str):
        """Update status bar message."""
        self.status_var.set(message)

    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    try:
        app = CompressorGUI()
        app.run()
    except Exception as e:
        logging.error(f"Failed to start GUI application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application:\n{e}")


if __name__ == "__main__":
    main()
