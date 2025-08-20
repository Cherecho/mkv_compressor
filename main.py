#!/usr/bin/env python3
"""
Main entry point for MKV Video Compressor.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MKV Video Compressor")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument("--cli", action="store_true", help="Use CLI interface")

    args, remaining = parser.parse_known_args()

    if args.gui:
        from mkv_compressor.gui import main

        main()
    elif args.cli or remaining:
        # Use CLI if explicitly requested or if there are remaining arguments
        from mkv_compressor.cli import main

        sys.argv = [sys.argv[0]] + remaining
        main()
    else:
        # Default to GUI if no arguments
        try:
            from mkv_compressor.gui import main

            main()
        except ImportError:
            print("GUI dependencies not available, falling back to CLI")
            from mkv_compressor.cli import main

            main()
