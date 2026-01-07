# Changelog

All notable changes to the Malaysia Marketplace Scraper project.

## [1.0.0] - 2026-01-07

### Added
- **Package Configuration**: Created `setup.py` and `pyproject.toml` for pip installation
- **MANIFEST.in**: Added package data specification file
- **CLI Entry Point**: Added `malaysia-scraper` command for global access
- **INSTALLATION_GUIDE.md**: Comprehensive installation and usage guide
- **Export Directory Handling**: Automatic creation of `exports/` directory

### Fixed
- **CSV Export Bug**: Fixed `'list' object has no attribute 'items'` error
  - Now handles both direct results structure (`{platform: [products]}`) 
  - And nested results structure (`{keyword: {platform: [products]}}`)
- **Export File Location**: All exports now save to `exports/` directory automatically
  - Affects `_export_json()`, `_export_csv()`, `_export_txt()` methods
  - Updated `save_multi_platform_results()` method
- **Missing os Import**: Added `import os` to `multi_platform_scraper.py`

### Changed
- **Export Methods**: Updated all export functions to prepend `OUTPUT_DIRS['exports']` to filenames
- **README.md**: Completely rewritten installation section with three installation options:
  1. Install as Package (Recommended) - `pip install -e .`
  2. Build and Install as Wheel
  3. Manual Installation (Development)
- **Usage Documentation**: Added comprehensive command-line arguments documentation
- **Project Structure**: Updated to reflect package files
- **Troubleshooting Guide**: Expanded with package-specific issues

### Technical Details

#### Files Modified
1. **multi_platform_scraper.py**
   - Added `import os` at line 8
   - Modified `_export_json()` to handle exports directory
   - Modified `_export_csv()` to handle multiple data structures and exports directory
   - Modified `_export_txt()` to handle exports directory and additional data fields
   - Modified `save_multi_platform_results()` to use exports directory

2. **README.md**
   - Rewrote Installation section (lines 38-81)
   - Rewrote Usage section (lines 83-128)
   - Updated Project Structure (lines 121-141)
   - Expanded Troubleshooting section (lines 235-296)
   - Added Package Distribution section (lines 312-332)

#### Files Created
1. **setup.py** - Package installation configuration
   - Defines package metadata
   - Lists all Python modules
   - Creates `malaysia-scraper` console script entry point
   - Specifies Python 3.8+ requirement

2. **pyproject.toml** - Modern Python package metadata
   - Build system requirements
   - Project metadata and dependencies
   - Optional dev dependencies
   - Tool configurations (black, mypy)

3. **MANIFEST.in** - Package data file specification
   - Includes documentation files (README.md, LICENSE)
   - Includes configuration files
   - Excludes build artifacts and data directories

4. **INSTALLATION_GUIDE.md** - Quick start guide
   - Installation instructions
   - Command reference table
   - Common troubleshooting steps

## Installation Instructions

```bash
# Clone the repository
git clone <repository-url>
cd malaysia-marketplace-scrapper-1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Install the package
pip install -e .

# Run the application
malaysia-scraper
```

## Migration Notes

### For Existing Users

If you were using the application before v1.0.0:

1. Pull the latest changes
2. Reinstall the package:
   ```bash
   pip install -e . --upgrade
   ```
3. The export functionality now works correctly - files save to `exports/` directory
4. You can now use `malaysia-scraper` command instead of `python main.py`

### Export Behavior Changes

- **Before**: Exports saved to current working directory, CSV export failed with certain data structures
- **After**: All exports automatically save to `exports/` directory, CSV export handles all data structures

## Known Issues

None at this time.

## Future Plans

- Web Dashboard integration
- API endpoints for programmatic access
- Database integration options
- Additional platform support (Blibli, Bukalapak)

---

**Maintainer Note**: This version marks the transition from a development script to a properly packaged Python application.
