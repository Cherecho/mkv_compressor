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
from ..utils.assets import get_logo, get_window_icon, get_large_logo


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

        # Remove default title bar and create custom one
        self.window.overrideredirect(True)

        # Modern window effects
        try:
            self.window.wm_attributes("-alpha", 0.97)  # Slight transparency
        except:
            pass

        # Center window and make it modal
        self.window.transient(parent)
        self.window.grab_set()
        self._center_window()

        # Create custom title bar first
        self._create_custom_title_bar()

        self.setup_ui()
        self.is_cancelled = False

    def _create_custom_title_bar(self):
        """Create a custom dark title bar for the progress window."""
        try:
            # Configure grid for custom title bar
            self.window.grid_rowconfigure(0, weight=0)  # Title bar row
            self.window.grid_rowconfigure(1, weight=1)  # Content row
            self.window.grid_columnconfigure(0, weight=1)

            # Create custom title bar frame
            self.title_bar = tk.Frame(self.window, bg=ModernStyle.PRIMARY_BG, height=35)
            self.title_bar.grid(row=0, column=0, sticky="nsew")
            self.title_bar.grid_propagate(False)

            # Title bar content
            title_frame = tk.Frame(self.title_bar, bg=ModernStyle.PRIMARY_BG)
            title_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
            self.title_bar.grid_rowconfigure(0, weight=1)
            self.title_bar.grid_columnconfigure(0, weight=1)

            # Progress window icon and title
            title_label = tk.Label(
                title_frame,
                text="🎬 Compression Progress",
                bg=ModernStyle.PRIMARY_BG,
                fg=ModernStyle.TEXT_PRIMARY,
                font=("Segoe UI", 8, "bold"),  # Smaller font size
            )
            title_label.grid(row=0, column=0, sticky="w")

            # Window controls
            controls_frame = tk.Frame(title_frame, bg=ModernStyle.PRIMARY_BG)
            controls_frame.grid(row=0, column=1, sticky="e")
            title_frame.grid_columnconfigure(1, weight=1)

            # Close button
            close_btn = tk.Button(
                controls_frame,
                text="✕",
                bg=ModernStyle.ERROR,
                fg=ModernStyle.TEXT_PRIMARY,
                bd=0,
                font=("Segoe UI", 8),
                command=self.close_window,
                relief="flat",
            )
            close_btn.grid(row=0, column=0, padx=2)

            # Make title bar draggable
            self._make_draggable(self.title_bar)

        except Exception as e:
            # Fallback: restore normal window if custom title bar fails
            try:
                self.window.overrideredirect(False)
            except:
                pass

    def _make_draggable(self, widget):
        """Make the title bar draggable to move the window."""

        def start_move(event):
            widget.start_x = event.x
            widget.start_y = event.y

        def stop_move(event):
            widget.start_x = None
            widget.start_y = None

        def do_move(event):
            if hasattr(widget, "start_x") and widget.start_x is not None:
                deltax = event.x - widget.start_x
                deltay = event.y - widget.start_y
                x = self.window.winfo_x() + deltax
                y = self.window.winfo_y() + deltay
                self.window.geometry(f"+{x}+{y}")

        widget.bind("<Button-1>", start_move)
        widget.bind("<ButtonRelease-1>", stop_move)
        widget.bind("<B1-Motion>", do_move)

        # Also bind to all child widgets
        for child in widget.winfo_children():
            if isinstance(child, (tk.Label, tk.Frame)):
                child.bind("<Button-1>", start_move)
                child.bind("<ButtonRelease-1>", stop_move)
                child.bind("<B1-Motion>", do_move)

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
        # Main content area with modern styling (starts at row 1 due to custom title bar)
        main_frame = GlassEffect.create_glass_frame(self.window)
        main_frame.configure(bg=ModernStyle.PRIMARY_BG, bd=0)
        main_frame.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20
        )

        # Configure window grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)  # Main content row
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

        # Status indicator in the info card
        self.status_indicator = tk.Label(
            info_card,
            text="●",
            bg=ModernStyle.SURFACE_BG,
            fg=ModernStyle.SUCCESS,
            font=("Segoe UI", 14),
        )
        self.status_indicator.grid(row=0, column=2, sticky=tk.E, padx=15, pady=15)

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
        self._setup_dark_mode_window()
        self._create_main_interface()
        self._setup_event_handlers()

    def _setup_dark_mode_window(self):
        """Setup the main window with dark mode styling."""
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()

        self.root.title("MKV Video Compressor")
        self.root.geometry("1100x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=ModernStyle.PRIMARY_BG)

        # Setup proper window close handling
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Additional dark mode window styling
        try:
            # Center the window on screen
            self.root.eval("tk::PlaceWindow . center")

            # Set window to appear on top during startup for better visibility
            self.root.attributes("-topmost", True)
            self.root.after(100, lambda: self.root.attributes("-topmost", False))
        except Exception as e:
            self.logger.warning(f"Failed to apply window styling: {e}")

        # Set custom window icon and enable dark title bar
        self._configure_window_appearance()

        # Configure window icon BEFORE making it borderless (important for taskbar)
        self._set_window_icon_early()

    def _set_window_icon_early(self):
        """Set window icon early, before making window borderless."""
        try:
            icon_path = get_window_icon()
            if icon_path:
                # Set the ICO icon first
                self.root.iconbitmap(icon_path)
                self.logger.info(f"Set early window icon: {icon_path}")

                # Force the window to update its icon in the taskbar
                self.root.update_idletasks()

        except Exception as e:
            self.logger.warning(f"Failed to set early window icon: {e}")

    def _configure_window_appearance(self):
        """Configure window appearance and dark mode title bar."""
        # Set custom window icon if available - this must be done early for taskbar icon
        try:
            icon_path = get_window_icon()
            if icon_path:
                self.root.iconbitmap(icon_path)
                self.logger.info(f"Set window icon: {icon_path}")

                # For borderless windows, also set the icon using iconphoto for better compatibility
                try:
                    # Load the icon as PhotoImage for additional icon setting
                    logo_img = get_logo(size=(32, 32))
                    if logo_img:
                        self.root.iconphoto(True, logo_img)
                        self.logger.info("Set additional PNG logo as window icon")
                except Exception as e:
                    self.logger.warning(f"Failed to set additional PNG icon: {e}")
            else:
                # Try to use PNG logo as window icon (alternative method)
                logo_img = get_logo(size=(32, 32))
                if logo_img:
                    # For PNG logos, try setting as photoimage icon (limited support)
                    try:
                        self.root.iconphoto(True, logo_img)
                        self.logger.info("Set PNG logo as window icon")
                    except Exception as e:
                        self.logger.warning(f"Failed to set PNG as window icon: {e}")
        except Exception as e:
            self.logger.warning(f"Failed to set window icon: {e}")

        # Configure window attributes for modern dark look
        try:
            # Enable transparency and modern window effects (Windows 10/11)
            self.root.wm_attributes("-alpha", 0.99)  # Slight transparency

            # Check user preference for dark mode method
            dark_mode_config = self._load_dark_mode_config()

            # For Windows: enable dark mode window styling
            if hasattr(self.root, "wm_attributes"):
                try:
                    # Windows 10/11 dark mode title bar
                    import sys

                    if sys.platform == "win32":
                        if dark_mode_config.get("force_custom_titlebar", False):
                            self.logger.info(
                                "User configured: Force custom title bar (will be created later)"
                            )
                            # Custom title bar will be created in _create_main_interface after logos load
                        else:
                            self._enable_windows_dark_mode()

                    self.root.wm_attributes("-transparentcolor", "")
                except:
                    pass
        except:
            pass

    def _load_dark_mode_config(self):
        """Load dark mode configuration from user settings."""
        try:
            import json
            from pathlib import Path

            config_file = Path.home() / ".config" / "mkv-compressor" / "dark_mode.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            self.logger.debug(f"Could not load dark mode config: {e}")

        # Default configuration
        return {"dark_mode_method": "auto", "force_custom_titlebar": False}

    def _enable_windows_dark_mode(self):
        """Enable Windows dark mode title bar."""
        try:
            import ctypes
            from ctypes import wintypes
            import sys

            # Wait for window to be fully created
            self.root.update_idletasks()

            # Get window handle
            hwnd = self.root.winfo_id()

            # Try different dark mode approaches for different Windows versions
            success = False

            # Method 1: Force dark mode registry approach
            try:
                # Check if system is in dark mode
                import winreg

                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                )
                apps_use_light_theme = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
                winreg.CloseKey(key)

                if apps_use_light_theme == 0:  # System is in dark mode
                    self.logger.info("System is in dark mode, applying window styling")

            except:
                pass

            # Method 2: Windows 11/newer Windows 10 builds (attribute 20)
            try:
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                value = ctypes.c_int(1)
                result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(value),
                    ctypes.sizeof(value),
                )
                if result == 0:
                    success = True
                    self.logger.info("Dark mode title bar enabled (attribute 20)")
            except Exception as e:
                self.logger.debug(f"Method 2 failed: {e}")

            # Method 3: Alternative approach for older Windows 10 (attribute 19)
            if not success:
                try:
                    DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
                    value = ctypes.c_int(1)
                    result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd,
                        DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                        ctypes.byref(value),
                        ctypes.sizeof(value),
                    )
                    if result == 0:
                        success = True
                        self.logger.info("Dark mode title bar enabled (attribute 19)")
                except Exception as e:
                    self.logger.debug(f"Method 3 failed: {e}")

            # Method 4: Set window theme manually
            if not success:
                try:
                    # Try to set dark theme using SetWindowTheme
                    ctypes.windll.uxtheme.SetWindowTheme(
                        hwnd, "DarkMode_Explorer", None
                    )
                    success = True
                    self.logger.info("Dark theme applied using SetWindowTheme")
                except Exception as e:
                    self.logger.debug(f"Method 4 failed: {e}")

            # Method 5: Use custom borderless window approach
            if not success:
                self.logger.warning(
                    "Native dark mode not available, using custom approach"
                )
                self._create_custom_dark_titlebar()
                return

        except Exception as e:
            self.logger.warning(f"Failed to set dark title bar: {e}")
            self._create_custom_dark_titlebar()

    def _create_custom_dark_titlebar(self):
        """Create a custom dark title bar when native Windows dark mode fails."""
        try:
            # Option 1: Create borderless window with custom title bar
            self.logger.info("Creating custom dark title bar")

            # Store original geometry
            geometry = self.root.geometry()

            # Force icon update before going borderless
            try:
                self.root.update()
                self.root.focus_force()
            except:
                pass

            # Make window borderless
            self.root.overrideredirect(True)

            # Try to maintain taskbar presence after going borderless
            try:
                # Set window attributes to try to keep it in taskbar
                self.root.wm_attributes("-toolwindow", False)
                self.root.update_idletasks()
            except:
                pass

            # Ensure grid is used consistently on root (avoid mixing pack/grid)
            self.root.grid_rowconfigure(0, weight=0)  # Title bar row
            self.root.grid_rowconfigure(1, weight=1)  # Content row
            self.root.grid_columnconfigure(0, weight=1)

            # Create custom title bar frame (using grid)
            self.title_bar = tk.Frame(self.root, bg=ModernStyle.PRIMARY_BG, height=35)
            self.title_bar.grid(row=0, column=0, sticky="nsew")
            self.title_bar.grid_propagate(False)

            # Title bar content
            title_frame = tk.Frame(self.title_bar, bg=ModernStyle.PRIMARY_BG)
            title_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
            self.title_bar.grid_rowconfigure(0, weight=1)
            self.title_bar.grid_columnconfigure(0, weight=1)

            # App icon and title (use smaller logo for title bar)
            if self.app_logo:
                # Create a smaller version of the logo for the title bar
                try:
                    small_logo = get_logo(size=(24, 24))  # Much smaller for title bar
                    if small_logo:
                        icon_label = tk.Label(
                            title_frame, image=small_logo, bg=ModernStyle.PRIMARY_BG
                        )
                        icon_label.grid(row=0, column=0, padx=(0, 8), sticky="w")
                        # Keep reference to prevent garbage collection
                        self.title_bar_logo = small_logo
                except:
                    pass

            title_label = tk.Label(
                title_frame,
                text="MKV Video Compressor",
                bg=ModernStyle.PRIMARY_BG,
                fg=ModernStyle.TEXT_PRIMARY,
                font=("Segoe UI", 8, "bold"),  # Smaller font size
            )
            title_label.grid(row=0, column=1, sticky="w")

            # Window controls
            controls_frame = tk.Frame(title_frame, bg=ModernStyle.PRIMARY_BG)
            controls_frame.grid(row=0, column=2, sticky="e")
            title_frame.grid_columnconfigure(2, weight=1)

            # Minimize button
            min_btn = tk.Button(
                controls_frame,
                text="🗕",
                bg=ModernStyle.PRIMARY_BG,
                fg=ModernStyle.TEXT_PRIMARY,
                bd=0,
                font=("Segoe UI", 8),
                command=lambda: self.root.iconify(),
                relief="flat",
            )
            min_btn.grid(row=0, column=0, padx=2)

            # Close button
            close_btn = tk.Button(
                controls_frame,
                text="✕",
                bg=ModernStyle.ERROR,
                fg=ModernStyle.TEXT_PRIMARY,
                bd=0,
                font=("Segoe UI", 8),
                command=self._on_closing,
                relief="flat",
            )
            close_btn.grid(row=0, column=1, padx=2)

            # Make title bar draggable
            self._make_draggable(self.title_bar)

            # Restore geometry
            self.root.geometry(geometry)

            self.logger.info("Custom dark title bar created successfully")

        except Exception as e:
            self.logger.error(f"Failed to create custom title bar: {e}")
            # Fallback: restore normal window
            try:
                self.root.overrideredirect(False)
            except:
                pass

    def _make_draggable(self, widget):
        """Make a widget draggable to move the window."""

        def start_move(event):
            widget.start_x = event.x
            widget.start_y = event.y

        def stop_move(event):
            widget.start_x = None
            widget.start_y = None

        def do_move(event):
            if hasattr(widget, "start_x") and widget.start_x is not None:
                deltax = event.x - widget.start_x
                deltay = event.y - widget.start_y
                x = self.root.winfo_x() + deltax
                y = self.root.winfo_y() + deltay
                self.root.geometry(f"+{x}+{y}")

        widget.bind("<Button-1>", start_move)
        widget.bind("<ButtonRelease-1>", stop_move)
        widget.bind("<B1-Motion>", do_move)

        # Also bind to all child widgets
        for child in widget.winfo_children():
            if isinstance(child, (tk.Label, tk.Frame)):
                child.bind("<Button-1>", start_move)
                child.bind("<ButtonRelease-1>", stop_move)
                child.bind("<B1-Motion>", do_move)

    def _apply_alternative_dark_styling(self):
        """Apply alternative dark styling when native dark mode is not available."""
        try:
            # Remove window border for a more modern look (optional fallback)
            # self.root.configure(relief='flat', bd=0)

            # Add a subtle dark border effect
            self.root.configure(highlightbackground=ModernStyle.BORDER_COLOR)
            self.root.configure(highlightcolor=ModernStyle.ACCENT_PRIMARY)

            self.logger.info("Applied alternative dark styling")
        except Exception as e:
            self.logger.warning(f"Failed to apply alternative dark styling: {e}")

    def _create_main_interface(self):
        """Create the main application interface."""
        # Configure modern styles
        ModernStyle.configure_styles()

        # Variables (initialize before loading logos)
        self.input_files: List[str] = []
        self.output_directory = tk.StringVar()
        self.selected_preset = tk.StringVar(value="Balanced")

        # Load application logo for use in GUI (after root window is fully initialized)
        self.app_logo = get_logo(size=(48, 48))  # Header logo
        self.app_logo_large = get_large_logo()  # About dialog logo
        self.about_small_logo = None  # Will be loaded in about tab

        # Now check if we need to create custom title bar (after logos are loaded)
        dark_mode_config = self._load_dark_mode_config()
        if dark_mode_config.get("force_custom_titlebar", False):
            self._create_custom_dark_titlebar()

        # Load settings
        self.load_settings()

        # Create the main interface
        self.setup_ui()

    def _setup_event_handlers(self):
        """Setup event handlers for the application."""

        # Load settings
        self.load_settings()

        # Setup modern UI
        self.setup_ui()

        # Setup logging handler for GUI
        self.setup_log_handler()

    def setup_ui(self):
        """Setup the modern user interface."""
        # Initialize status variable for status updates
        self.status_var = tk.StringVar(value="Ready")

        # Determine the starting row based on whether we have a custom title bar
        start_row = 1 if hasattr(self, "title_bar") else 0

        # Main container with minimal padding when custom title bar is present
        padding_top = "0" if hasattr(self, "title_bar") else "0"

        # Main container with padding (always use grid on root)
        main_container = ttk.Frame(
            self.root, style="Modern.TFrame", padding=f"{padding_top} 0 0 0"
        )
        main_container.grid(
            row=start_row,
            column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=0,
            pady=(0, 0),
        )

        # Configure root grid if not already done
        if not hasattr(self, "title_bar"):
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(start_row, weight=1)

        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(
            1 if not hasattr(self, "title_bar") else 0, weight=1
        )

        # Header section (only if we don't have a custom title bar)
        if not hasattr(self, "title_bar"):
            self.create_header(main_container)
            notebook_row = 1
            notebook_pady = (10, 20)
        else:
            # Skip header creation since we have a custom title bar
            notebook_row = 0
            notebook_pady = (5, 20)  # Minimal top padding when custom title bar

        # Create modern dark notebook for tabs
        self.notebook = ttk.Notebook(main_container, style="Modern.TNotebook")
        self.notebook.grid(
            row=notebook_row,
            column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=20,
            pady=notebook_pady,
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

    def create_header(self, parent):
        """Create modern dark header section with gradient effect."""
        header_frame = GlassEffect.create_glass_frame(parent)
        header_frame.configure(bg=ModernStyle.ACCENT_PRIMARY, bd=0)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=0, pady=0)
        header_frame.columnconfigure(1, weight=1)

        # App icon/title with modern styling
        header_content = tk.Frame(header_frame, bg=ModernStyle.ACCENT_PRIMARY)
        header_content.grid(row=0, column=0, sticky=tk.W, padx=25, pady=20)

        # Logo (if available)
        if self.app_logo:
            logo_label = tk.Label(
                header_content,
                image=self.app_logo,
                bg=ModernStyle.ACCENT_PRIMARY,
                borderwidth=0,
            )
            logo_label.grid(row=0, column=0, padx=(0, 15), pady=0)

        # Title text
        title_label = tk.Label(
            header_content,
            text="MKV Video Compressor",
            bg=ModernStyle.ACCENT_PRIMARY,
            fg=ModernStyle.TEXT_PRIMARY,
            font=("Segoe UI", 18, "bold"),
        )
        title_label.grid(row=0, column=1, sticky=tk.W, pady=0)

        # Version and status info
        info_frame = tk.Frame(header_frame, bg=ModernStyle.ACCENT_PRIMARY)
        info_frame.grid(row=0, column=1, sticky=tk.E, padx=25, pady=20)

        version_label = tk.Label(
            info_frame,
            text="v1.2.0",
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
        """Setup the modern about tab with scrolling support."""
        # Create a canvas with scrollbar for scrolling
        canvas = tk.Canvas(
            self.about_frame,
            bg=ModernStyle.PRIMARY_BG,
            highlightthickness=0,
            borderwidth=0,
        )
        scrollbar = ttk.Scrollbar(
            self.about_frame,
            orient="vertical",
            command=canvas.yview,
            style="Modern.Vertical.TScrollbar",
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        # Grid the canvas and scrollbar
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights
        self.about_frame.grid_rowconfigure(0, weight=1)
        self.about_frame.grid_columnconfigure(0, weight=1)

        # Create scrollable frame inside canvas
        scrollable_frame = ttk.Frame(canvas, style="Modern.TFrame")
        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )

        # Configure scrollable frame to expand
        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Main container with reduced side padding to use more width
        about_container = ttk.Frame(
            scrollable_frame,
            style="Modern.TFrame",
            padding="30 30 10 30",  # top, right, bottom, left
        )
        about_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        about_container.columnconfigure(0, weight=1)

        # Configure scrolling behavior
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Update canvas window width to match canvas width (minus scrollbar width)
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:  # Only update if canvas has been drawn
                canvas.itemconfig(canvas_window, width=canvas_width)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind scroll events
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)

        # Initial configuration to set proper width
        canvas.update_idletasks()
        configure_scroll_region()

        # Bind mousewheel to canvas and all child widgets for smooth scrolling
        def bind_mousewheel(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)

        # Bind after content is created
        self.about_frame.after(100, lambda: bind_mousewheel(self.about_frame))

        # Header section with logo and basic info
        header_section = ttk.Frame(about_container, style="Modern.TFrame")
        header_section.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 25))
        header_section.columnconfigure(1, weight=1)

        # Small professional logo (if available)
        if self.app_logo_large:
            # Use a smaller logo for professional appearance
            small_logo = get_logo(size=(48, 48))  # Much smaller logo
            if small_logo:
                logo_label = tk.Label(
                    header_section,
                    image=small_logo,
                    bg=ModernStyle.PRIMARY_BG,
                    borderwidth=0,
                )
                logo_label.grid(row=0, column=0, rowspan=2, padx=(0, 15), pady=(0, 5))
                # Store reference to prevent garbage collection
                self.about_small_logo = small_logo

        # App title and tagline
        title_label = ttk.Label(
            header_section,
            text="🎬 MKV Video Compressor",
            style="Title.TLabel",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))

        tagline_label = ttk.Label(
            header_section,
            text="Professional Video Compression Suite",
            style="Modern.TLabel",
            font=("Segoe UI", 11, "italic"),
            foreground=ModernStyle.TEXT_SECONDARY,
        )
        tagline_label.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 15))

        # Version and build info section
        version_section = ttk.LabelFrame(
            about_container,
            text="📦 Version Information",
            style="Modern.TLabelframe",
            padding="15",
        )
        version_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        version_section.columnconfigure(1, weight=1)

        # Version details
        version_info = [
            ("Version:", "1.2.0"),
            ("Build:", "Release"),
            ("Release Date:", "August 2025"),
            ("Architecture:", "x64"),
            ("Python Version:", "3.8+"),
        ]

        for i, (label_text, value_text) in enumerate(version_info):
            label = ttk.Label(
                version_section,
                text=label_text,
                style="Modern.TLabel",
                font=("Segoe UI", 9, "bold"),
            )
            label.grid(row=i, column=0, sticky=tk.W, padx=(0, 10), pady=2)

            value = ttk.Label(
                version_section,
                text=value_text,
                style="Modern.TLabel",
                font=("Segoe UI", 9),
            )
            value.grid(row=i, column=1, sticky=tk.W, pady=2)

        # Description section
        desc_section = ttk.LabelFrame(
            about_container,
            text="📝 Description",
            style="Modern.TLabelframe",
            padding="15",
        )
        desc_section.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        desc_text = """A professional-grade video compression application designed for efficiency and ease of use. 
Built with modern technology stack and optimized for high-quality video processing. 
Perfect for content creators, video professionals, and anyone who needs reliable video compression."""

        desc_label = ttk.Label(
            desc_section,
            text=desc_text,
            style="Modern.TLabel",
            font=("Segoe UI", 10),
            wraplength=650,
            justify=tk.LEFT,
        )
        desc_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Features section
        features_section = ttk.LabelFrame(
            about_container,
            text="✨ Key Features",
            style="Modern.TLabelframe",
            padding="15",
        )
        features_section.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        features_text = """• Advanced video compression with FFmpeg integration
• Multiple optimization presets (Fast, Balanced, High Quality, Custom)
• Batch processing with parallel compression support
• Professional drag-and-drop interface with file validation
• Real-time progress monitoring and detailed logging
• Comprehensive format support (MP4, AVI, MOV, MKV, WMV, FLV, WebM)
• Custom compression profiles and advanced parameter control
• Automatic quality optimization and file size prediction
• Cross-platform compatibility (Windows, macOS, Linux)"""

        features_label = ttk.Label(
            features_section,
            text=features_text,
            style="Modern.TLabel",
            font=("Segoe UI", 9),
            justify=tk.LEFT,
        )
        features_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Technical specifications section
        tech_section = ttk.LabelFrame(
            about_container,
            text="⚙️ Technical Specifications",
            style="Modern.TLabelframe",
            padding="15",
        )
        tech_section.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        tech_text = """• Built with Python 3.8+ and modern tkinter framework
• FFmpeg-powered compression engine for maximum compatibility
• Multi-threading support for improved performance
• Memory-efficient processing for large video files
• Supports hardware acceleration when available
• Unicode filename and path support
• Comprehensive error handling and recovery systems"""

        tech_label = ttk.Label(
            tech_section,
            text=tech_text,
            style="Modern.TLabel",
            font=("Segoe UI", 9),
            justify=tk.LEFT,
        )
        tech_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Requirements section
        req_section = ttk.LabelFrame(
            about_container,
            text="📋 System Requirements",
            style="Modern.TLabelframe",
            padding="15",
        )
        req_section.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        req_text = """• Operating System: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
• Python 3.8 or higher with tkinter support
• FFmpeg must be installed and accessible in system PATH
• Minimum 4GB RAM recommended (8GB+ for 4K video processing)
• At least 1GB free disk space for temporary files
• Display resolution: 1024x768 minimum (1920x1080 recommended)"""

        req_label = ttk.Label(
            req_section,
            text=req_text,
            style="Modern.TLabel",
            font=("Segoe UI", 9),
            justify=tk.LEFT,
        )
        req_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

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

        # Create progress window in main thread (important for Tkinter thread safety)
        self.progress_window = ProgressWindow(self.root)

        # Start compression in separate thread
        threading.Thread(target=self._compression_worker, daemon=True).start()

    def _compression_worker(self):
        """Worker thread for compression process."""
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
                if self.progress_window.is_cancelled:
                    break

                try:
                    # Update progress window (thread-safe using root.after)
                    filename = os.path.basename(input_file)
                    self.root.after(
                        0,
                        lambda f=filename: self.progress_window.update_current_file(f),
                    )
                    self.root.after(
                        0,
                        lambda f=filename: self.progress_window.add_log(
                            f"Starting: {f}"
                        ),
                    )

                    # Generate output filename
                    name, _ = os.path.splitext(filename)
                    output_file = os.path.join(output_dir, f"{name}_compressed.mkv")

                    # Setup progress callback (thread-safe)
                    def progress_callback(percentage):
                        overall_progress = ((i + percentage / 100) / total_files) * 100
                        self.root.after(
                            0,
                            lambda p=overall_progress, msg=f"File {i+1}/{total_files}": self.progress_window.update_progress(
                                p, msg
                            ),
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
                        self.root.after(
                            0,
                            lambda f=filename: self.progress_window.add_log(
                                f"✓ Completed: {f}"
                            ),
                        )
                        # Ensure progress shows 100% for this file
                        overall_progress = ((i + 1) / total_files) * 100
                        self.root.after(
                            0,
                            lambda p=overall_progress, msg=f"File {i+1}/{total_files} completed": self.progress_window.update_progress(
                                p, msg
                            ),
                        )
                    else:
                        self.root.after(
                            0,
                            lambda f=filename: self.progress_window.add_log(
                                f"✗ Failed: {f}"
                            ),
                        )

                except Exception as e:
                    self.root.after(
                        0,
                        lambda f=filename, err=str(e): self.progress_window.add_log(
                            f"✗ Error processing {f}: {err}"
                        ),
                    )

            # Compression finished
            if not self.progress_window.is_cancelled:
                self.root.after(
                    0,
                    lambda: self.progress_window.update_progress(
                        100, "All files processed"
                    ),
                )
                self.root.after(
                    0, lambda: self.progress_window.compression_finished(successful > 0)
                )

                # Show notification if enabled
                if self.show_notifications_var.get():
                    if successful == total_files:
                        self.root.after(
                            0,
                            lambda: messagebox.showinfo(
                                "Compression Complete",
                                f"All {total_files} files compressed successfully!",
                            ),
                        )
                    else:
                        self.root.after(
                            0,
                            lambda: messagebox.showwarning(
                                "Compression Complete",
                                f"{successful}/{total_files} files compressed successfully.",
                            ),
                        )

                # Open output folder if enabled
                if self.auto_open_output_var.get() and successful > 0:
                    self.root.after(0, lambda: os.startfile(output_dir))

        except Exception as e:
            self.root.after(
                0,
                lambda err=str(e): self.progress_window.add_log(
                    f"Critical error: {err}"
                ),
            )
            self.root.after(0, lambda: self.progress_window.compression_finished(False))
            self.root.after(
                0,
                lambda err=str(e): messagebox.showerror(
                    "Compression Error", f"An error occurred:\n{err}"
                ),
            )

        finally:
            # Re-enable start button
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))

    def update_status(self, message: str):
        """Update status bar message."""
        self.status_var.set(message)

    def _on_closing(self):
        """Handle window closing event with proper cleanup."""
        try:
            # Stop any running compression processes
            if hasattr(self, "compressor") and self.compressor:
                # Add any necessary cleanup for the compressor here
                pass

            # Save configuration before closing
            if hasattr(self, "config_manager"):
                try:
                    self.config_manager.save_config()
                except Exception as e:
                    self.logger.warning(f"Failed to save config on exit: {e}")

            # Destroy the window and exit
            self.root.quit()  # Exit the mainloop
            self.root.destroy()  # Destroy the window and cleanup resources

        except Exception as e:
            self.logger.error(f"Error during application closing: {e}")
            # Force exit if there's an error
            self.root.destroy()

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
