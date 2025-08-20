"""
Main GUI application for MKV Video Compressor.
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


class ProgressWindow:
    """Separate window for showing compression progress."""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Compression Progress")
        self.window.geometry("600x400")
        self.window.resizable(True, True)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.is_cancelled = False
        
    def setup_ui(self):
        """Setup progress window UI."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Current file label
        self.current_file_var = tk.StringVar(value="Preparing...")
        ttk.Label(main_frame, textvariable=self.current_file_var, font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, variable=self.progress_var, maximum=100, length=400
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress text
        self.progress_text_var = tk.StringVar(value="0% - Starting...")
        ttk.Label(main_frame, textvariable=self.progress_text_var).grid(
            row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10)
        )
        
        # Log area
        ttk.Label(main_frame, text="Log:", font=("Arial", 9, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(10, 5)
        )
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame, height=15, width=70, state=tk.DISABLED
        )
        self.log_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        self.cancel_button = ttk.Button(
            button_frame, text="Cancel", command=self.cancel_compression
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.close_button = ttk.Button(
            button_frame, text="Close", command=self.close_window, state=tk.DISABLED
        )
        self.close_button.pack(side=tk.RIGHT)
    
    def update_progress(self, percentage: float, message: str = ""):
        """Update progress bar and text."""
        self.progress_var.set(percentage)
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
        """Add message to log area."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.window.update_idletasks()
    
    def compression_finished(self, success: bool = True):
        """Mark compression as finished."""
        self.cancel_button.config(state=tk.DISABLED)
        self.close_button.config(state=tk.NORMAL)
        
        if success:
            self.progress_text_var.set("100% - Completed successfully!")
            self.add_log("✓ All compressions completed successfully!")
        else:
            self.progress_text_var.set("Compression failed or cancelled")
            self.add_log("✗ Compression failed or was cancelled.")
    
    def cancel_compression(self):
        """Cancel the compression process."""
        self.is_cancelled = True
        self.add_log("Cancelling compression...")
    
    def close_window(self):
        """Close the progress window."""
        self.window.destroy()


class CompressorGUI:
    """Main GUI application for the MKV Video Compressor."""
    
    def __init__(self):
        # Initialize logging
        self.logger = setup_logger()
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        
        # Initialize video compressor
        self.compressor = VideoCompressor()
        
        # Initialize GUI
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
            
        self.root.title("MKV Video Compressor")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variables
        self.input_files: List[str] = []
        self.output_directory = tk.StringVar()
        self.selected_preset = tk.StringVar(value="Balanced")
        
        # Load settings
        self.load_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Setup logging handler for GUI
        self.setup_log_handler()
        
    def setup_ui(self):
        """Setup the main user interface."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main compression tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Compression")
        self.setup_main_tab()
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self.setup_settings_tab()
        
        # About tab
        self.about_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.about_frame, text="About")
        self.setup_about_tab()
        
        # Status bar
        self.setup_status_bar()
    
    def setup_main_tab(self):
        """Setup the main compression tab."""
        # Input files section
        input_frame = ttk.LabelFrame(self.main_frame, text="Input Files", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # File list
        list_frame = ttk.Frame(input_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        self.file_listbox = tk.Listbox(listbox_frame, selectmode=tk.EXTENDED)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar for listbox
        listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=listbox_scrollbar.set)
        listbox_scrollbar.config(command=self.file_listbox.yview)
        
        # Buttons frame
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        ttk.Button(buttons_frame, text="Add Files", command=self.add_files).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(buttons_frame, text="Add Folder", command=self.add_folder).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(buttons_frame, text="Remove Selected", command=self.remove_selected).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(buttons_frame, text="Clear All", command=self.clear_all).pack(fill=tk.X)
        
        # Drag and drop support
        if DND_AVAILABLE:
            self.file_listbox.drop_target_register(DND_FILES)
            self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)
            
            # Add drop instruction
            ttk.Label(input_frame, text="💡 Tip: You can also drag and drop files here!", 
                     foreground="gray").pack(pady=(5, 0))
        
        # Output directory section
        output_frame = ttk.LabelFrame(self.main_frame, text="Output Directory", padding="10")
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        output_entry_frame = ttk.Frame(output_frame)
        output_entry_frame.pack(fill=tk.X)
        
        ttk.Entry(output_entry_frame, textvariable=self.output_directory, 
                 state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_entry_frame, text="Browse", 
                  command=self.browse_output_directory).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Compression settings section
        settings_frame = ttk.LabelFrame(self.main_frame, text="Compression Settings", padding="10")
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Preset selection
        preset_frame = ttk.Frame(settings_frame)
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(preset_frame, text="Preset:").pack(side=tk.LEFT)
        
        self.preset_combo = ttk.Combobox(
            preset_frame, 
            textvariable=self.selected_preset,
            values=list(self.compressor.get_compression_presets().keys()),
            state="readonly",
            width=20
        )
        self.preset_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.preset_combo.bind('<<ComboboxSelected>>', self.on_preset_changed)
        
        ttk.Button(preset_frame, text="Custom Settings", 
                  command=self.show_custom_settings).pack(side=tk.RIGHT)
        
        # Quick info about selected preset
        self.preset_info_var = tk.StringVar()
        self.preset_info_label = ttk.Label(settings_frame, textvariable=self.preset_info_var,
                                          foreground="gray", font=("Arial", 9))
        self.preset_info_label.pack(fill=tk.X)
        self.update_preset_info()
        
        # Control buttons
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        self.start_button = ttk.Button(
            control_frame, text="Start Compression", command=self.start_compression,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(control_frame, text="Preview Settings", 
                  command=self.preview_settings).pack(side=tk.RIGHT)
    
    def setup_settings_tab(self):
        """Setup the settings tab."""
        # General settings
        general_frame = ttk.LabelFrame(self.settings_frame, text="General Settings", padding="10")
        general_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # FFmpeg path
        ffmpeg_frame = ttk.Frame(general_frame)
        ffmpeg_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(ffmpeg_frame, text="FFmpeg Path:").pack(side=tk.LEFT)
        
        self.ffmpeg_path_var = tk.StringVar(value=self.config_manager.get('ffmpeg_path', ''))
        ffmpeg_entry = ttk.Entry(ffmpeg_frame, textvariable=self.ffmpeg_path_var)
        ffmpeg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        ttk.Button(ffmpeg_frame, text="Browse", 
                  command=self.browse_ffmpeg_path).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Default output directory
        default_output_frame = ttk.Frame(general_frame)
        default_output_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(default_output_frame, text="Default Output Directory:").pack(side=tk.LEFT)
        
        self.default_output_var = tk.StringVar(value=self.config_manager.get('default_output_dir', ''))
        default_output_entry = ttk.Entry(default_output_frame, textvariable=self.default_output_var)
        default_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        ttk.Button(default_output_frame, text="Browse", 
                  command=self.browse_default_output).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Checkboxes for various settings
        self.overwrite_files_var = tk.BooleanVar(value=self.config_manager.get('overwrite_files', False))
        ttk.Checkbutton(general_frame, text="Overwrite existing files", 
                       variable=self.overwrite_files_var).pack(anchor=tk.W, pady=2)
        
        self.show_notifications_var = tk.BooleanVar(value=self.config_manager.get('show_notifications', True))
        ttk.Checkbutton(general_frame, text="Show completion notifications", 
                       variable=self.show_notifications_var).pack(anchor=tk.W, pady=2)
        
        self.auto_open_output_var = tk.BooleanVar(value=self.config_manager.get('auto_open_output', False))
        ttk.Checkbutton(general_frame, text="Open output folder when complete", 
                       variable=self.auto_open_output_var).pack(anchor=tk.W, pady=2)
        
        # Save settings button
        ttk.Button(general_frame, text="Save Settings", 
                  command=self.save_settings).pack(pady=(10, 0))
    
    def setup_about_tab(self):
        """Setup the about tab."""
        about_text = """
MKV Video Compressor v1.0.0

A professional video compression tool for MKV files.

Features:
• High-quality video compression using FFmpeg
• Multiple compression presets
• Batch processing support
• Drag-and-drop interface
• Real-time progress monitoring
• Custom compression settings

Requirements:
• FFmpeg must be installed and available in PATH
• Supported input formats: MP4, AVI, MOV, MKV, WMV, FLV, and more
• Output format: MKV (Matroska Video)

Created with Python and tkinter.
        """
        
        about_label = tk.Label(self.about_frame, text=about_text.strip(), 
                              justify=tk.LEFT, font=("Arial", 10), padx=20, pady=20)
        about_label.pack(fill=tk.BOTH, expand=True)
    
    def setup_status_bar(self):
        """Setup the status bar."""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.status_bar, textvariable=self.status_var).pack(
            side=tk.LEFT, padx=10, pady=5
        )
    
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
        default_output = self.config_manager.get('default_output_dir', '')
        if default_output and os.path.exists(default_output):
            self.output_directory.set(default_output)
    
    def save_settings(self):
        """Save current settings to configuration."""
        settings = {
            'ffmpeg_path': self.ffmpeg_path_var.get(),
            'default_output_dir': self.default_output_var.get(),
            'overwrite_files': self.overwrite_files_var.get(),
            'show_notifications': self.show_notifications_var.get(),
            'auto_open_output': self.auto_open_output_var.get()
        }
        
        for key, value in settings.items():
            self.config_manager.set(key, value)
        
        self.config_manager.save()
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def add_files(self):
        """Add video files to the input list."""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=filetypes
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
        
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
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
                video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
                if Path(file).suffix.lower() in video_extensions:
                    if file not in self.input_files:
                        self.input_files.append(file)
                        self.file_listbox.insert(tk.END, os.path.basename(file))
                        added_count += 1
            elif os.path.isdir(file):
                # Add video files from directory
                video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
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
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
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
        messagebox.showinfo("Custom Settings", "Custom settings dialog not implemented yet.\nThis would allow fine-tuning of compression parameters.")
    
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
            messagebox.showwarning("No Files", "Please add some video files to compress.")
            return
        
        if not self.output_directory.get():
            messagebox.showwarning("No Output Directory", "Please select an output directory.")
            return
        
        # Confirm start
        response = messagebox.askyesno(
            "Start Compression",
            f"Start compressing {len(self.input_files)} file(s)?\n\nThis may take a while depending on file sizes."
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
                        progress_window.update_progress(overall_progress, f"File {i+1}/{total_files}")
                    
                    # Compress video
                    success = self.compressor.compress_video(
                        input_file,
                        output_file,
                        settings,
                        progress_callback=progress_callback,
                        overwrite=overwrite
                    )
                    
                    if success:
                        successful += 1
                        progress_window.add_log(f"✓ Completed: {filename}")
                        # Ensure progress shows 100% for this file
                        overall_progress = ((i + 1) / total_files) * 100
                        progress_window.update_progress(overall_progress, f"File {i+1}/{total_files} completed")
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
                        messagebox.showinfo("Compression Complete", 
                                          f"All {total_files} files compressed successfully!")
                    else:
                        messagebox.showwarning("Compression Complete",
                                             f"{successful}/{total_files} files compressed successfully.")
                
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