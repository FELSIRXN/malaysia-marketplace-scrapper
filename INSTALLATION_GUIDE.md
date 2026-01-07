# Malaysia Marketplace Scraper - Installation & Usage Guide

## Quick Start

### Installation (Recommended Method)

```bash
# Navigate to the project directory
cd malaysia-marketplace-scrapper-1

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install the package
pip install -e .
```

### Running the Application

After installation, you can use the application in two ways:

#### 1. Using the Global Command

```bash
malaysia-scraper
```

This launches the interactive mode where you can:
- Select platforms to search
- Enter search keywords
- Choose number of results
- Analyze results
- Export to JSON, CSV, or TXT (saved in `exports/` directory)

#### 2. Using Command-Line Arguments

```bash
# Search for products
malaysia-scraper --keyword "laptop" --limit 50

# Search specific platforms only
malaysia-scraper --keyword "phone case" --platforms shopee,lazada

# Find best-sellers under RM 50
malaysia-scraper --keyword "electronics" --bestsellers --max-price 50

# Export results
malaysia-scraper --keyword "USB cable" --export csv --output my_results.csv
```

## Available Commands

| Command | Description |
|---------|-------------|
| `malaysia-scraper` | Launch interactive mode |
| `malaysia-scraper --help` | Show all available options |
| `malaysia-scraper --version` | Show version information |

## Common Command-Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--keyword` | `-k` | Search term | `--keyword "laptop"` |
| `--platforms` | `-p` | Platforms to search (comma-separated) | `--platforms shopee,lazada` |
| `--limit` | `-l` | Max results per platform | `--limit 100` |
| `--export` | `-e` | Export format (json/csv/txt) | `--export csv` |
| `--output` | `-o` | Output filename | `--output results.json` |
| `--bestsellers` | `-b` | Best seller analysis mode | `--bestsellers` |
| `--max-price` | | Maximum price filter (RM) | `--max-price 50` |
| `--interactive` | `-i` | Force interactive mode | `--interactive` |

## Export Functionality

All exports are automatically saved to the `exports/` directory:

```bash
malaysia-marketplace-scrapper-1/
└── exports/
    ├── hasil_pencarian_USB-C_Cable_20260107_123456.csv
    ├── hasil_pencarian_laptop_20260107_123500.json
    └── bestsellers_electronics_20260107_123600.txt
```

## Troubleshooting

### Command Not Found

If you get "command not found: malaysia-scraper":

```bash
# Reinstall the package
pip uninstall malaysia-marketplace-scraper
pip install -e .

# Or use Python module syntax
python -m main
```

### Export Not Working

The export bug has been fixed in v1.0.0. If you're still experiencing issues:

1. Ensure you have the latest version:
   ```bash
   pip install -e . --upgrade
   ```

2. Check the `exports/` directory is created (it should be automatic)

3. Check logs for errors:
   ```bash
   cat logs/scraper.log
   ```

### Module Import Errors

```bash
# Make sure you're in the correct directory
cd /path/to/malaysia-marketplace-scrapper-1

# Reinstall
pip install -e .
```

## Building Distribution Package

To create a distributable wheel file:

```bash
# Install build tools
pip install build

# Build the package
python -m build

# Install from the built wheel
pip install dist/malaysia_marketplace_scraper-1.0.0-py3-none-any.whl
```

## Supported Platforms

- ✓ **Shopee Malaysia** - Active
- ✓ **Lazada Malaysia** - Active
- ✓ **Mudah.my** - Active
- ✗ **Facebook Marketplace** - Disabled (requires authentication)

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review [logs/scraper.log](logs/scraper.log) for error details
- Ensure all dependencies are installed: `pip install -r requirements.txt`

---

**Version:** 1.0.0  
**Last Updated:** January 7, 2026
