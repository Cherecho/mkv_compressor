"""
Setup script for MKV Video Compressor.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "A professional video compression tool for MKV files."

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]
else:
    requirements = [
        "ffmpeg-python>=0.2.0",
        "Pillow>=10.0.0",
        "tkinterdnd2>=0.3.0",
        "psutil>=5.9.5",
        "tqdm>=4.66.1",
        "pydantic>=2.4.2",
    ]

# Development requirements
dev_requirements = [
    "pytest>=7.4.2",
    "pytest-cov>=4.1.0",
    "black>=23.9.1",
    "flake8>=6.1.0",
    "mypy>=1.6.0",
]

# Documentation requirements
doc_requirements = [
    "sphinx>=7.2.6",
    "sphinx-rtd-theme>=1.3.0",
]

setup(
    name="mkv-video-compressor",
    version="1.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional video compression tool for MKV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/mkv_compressor",
    project_urls={
        "Bug Reports": "https://github.com/your-username/mkv_compressor/issues",
        "Source": "https://github.com/your-username/mkv_compressor",
        "Documentation": "https://github.com/your-username/mkv_compressor/wiki",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    keywords=[
        "video",
        "compression",
        "mkv",
        "ffmpeg",
        "transcoding",
        "multimedia",
        "video-processing",
        "batch-processing",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "docs": doc_requirements,
        "all": dev_requirements + doc_requirements,
    },
    entry_points={
        "console_scripts": [
            "mkv-compressor=mkv_compressor.cli:main",
            "mkv-compressor-gui=mkv_compressor.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mkv_compressor": [
            "config/*.json",
            "assets/*",
        ],
    },
    zip_safe=False,
    platforms=["any"],
    license="MIT",
)
