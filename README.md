# 🛒 Multi-Platform E-commerce Scraper

> **Professional Indonesian Market Analysis Tool**

A comprehensive, production-ready scraper for Indonesian e-commerce platforms including Shopee, Tokopedia, and Lazada. Built with clean architecture, advanced analytics, and professional logging capabilities.

## ✨ Features

### 🚀 Core Functionality
- **Multi-Platform Support**: Shopee, Tokopedia, Lazada
- **Advanced Product Analysis**: Price trends, rating analysis, merchant insights
- **Real-time Data Collection**: Concurrent scraping with rate limiting
- **Professional Logging**: Comprehensive error tracking and performance monitoring
- **Export Capabilities**: JSON, CSV, Excel formats
- **Interactive CLI**: User-friendly command-line interface

### 📊 Analytics & Intelligence
- **Price Analysis**: Min/max/average pricing with market insights
- **Rating Analysis**: Product quality assessment across platforms
- **Merchant Analysis**: Top sellers and market concentration
- **Category Analysis**: Product distribution and trends
- **Platform Comparison**: Cross-platform price and availability analysis

### 🛡️ Robust Architecture
- **Error Handling**: Comprehensive retry mechanisms and graceful failures
- **Rate Limiting**: Respectful scraping with configurable delays
- **User Agent Rotation**: Anti-detection measures
- **Modular Design**: Easy to extend and maintain
- **Configuration Management**: Centralized settings and platform management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

#### Option 1: Install as Package (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd malaysia-marketplace-scrapper-1
   ```

2. **Create and activate virtual environment** (recommended)
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install the package in editable mode**
   ```bash
   pip install -e .
   ```

   This will:
   - Install all dependencies automatically
   - Make the `malaysia-scraper` command available globally
   - Allow you to modify the code and see changes immediately

4. **Run the scraper**
   ```bash
   malaysia-scraper
   ```
   
   Or use command-line arguments:
   ```bash
   malaysia-scraper --keyword "laptop" --limit 50
   ```

#### Option 2: Build and Install as Wheel

1. **Install build tools**
   ```bash
   pip install build
   ```

2. **Build the package**
   ```bash
   python -m build
   ```

3. **Install the wheel**
   ```bash
   pip install dist/malaysia_marketplace_scraper-1.0.0-py3-none-any.whl
   ```

#### Option 3: Manual Installation (Development)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd malaysia-marketplace-scrapper-1
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate  # Windows
   ```

3. **Upgrade pip and install build tools**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   **If you encounter metadata generation errors, try:**
   ```bash
   # Install packages individually
   pip install requests beautifulsoup4 selenium pandas lxml
   pip install fake-useragent python-dotenv openpyxl
   pip install plotly wordcloud matplotlib seaborn numpy
   pip install fastapi uvicorn pydantic pydantic-settings aiofiles
   ```

5. **Run the scraper**
   ```bash
   python main.py
   ```

## 🌐 Web Interface

The scraper now includes a modern web interface! No terminal required.

### Quick Start (Web Interface)

1. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

2. **Start the web interface**:
   ```bash
   python start_web.py
   ```

3. **Open your browser**:
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Web Interface Features

- ✅ **Product Search** - Search across platforms with real-time progress
- ✅ **Best Sellers** - Find top-selling affordable items
- ✅ **Platform Comparison** - Compare prices and availability
- ✅ **Interactive Charts** - Visualize price, rating, and sales data
- ✅ **Export Results** - Download as CSV, JSON, or Excel
- ✅ **Search History** - View and manage past searches
- ✅ **Mobile Responsive** - Works on all devices

For detailed web interface documentation, see [README_WEB.md](README_WEB.md)

## 📖 Usage

### Using the Installed Command

After installing the package with `pip install -e .`, you can use the `malaysia-scraper` command:

#### Interactive Mode
Launch the interactive CLI for guided product searches:

```bash
malaysia-scraper
```

Or if installed manually:
```bash
python main.py
```

The interactive mode provides:
- Platform selection
- Search term input
- Real-time progress tracking
- Automatic analysis and export
- Export to `exports/` directory

#### Command Line Arguments
```bash
malaysia-scraper --keyword "laptop gaming" --limit 50 --platforms shopee,lazada
```

**Available Arguments:**
- `--keyword`, `-k`: Search term (required for non-interactive mode)
- `--limit`, `-l`: Maximum results per platform (default: 100)
- `--platforms`, `-p`: Comma-separated platform names (shopee, lazada, mudah)
- `--export`, `-e`: Export format (json, csv, txt)
- `--output`, `-o`: Custom output filename
- `--interactive`, `-i`: Force interactive mode
- `--max-price`: Maximum price filter in RM (default: 50)
- `--sort-by`: Sort by sales, price, or rating (default: sales)
- `--top-n`: Number of top items to return (default: 50)
- `--bestsellers`, `-b`: Best seller analysis mode
- `--version`, `-v`: Show version information

### Example Usage

**Interactive mode:**
```bash
malaysia-scraper --interactive
```

**Search for affordable USB cables:**
```bash
malaysia-scraper --keyword "USB-C Cable" --limit 30
```

**Find best-selling items under RM 50:**
```bash
malaysia-scraper --keyword "electronics" --bestsellers --max-price 50 --top-n 20
```

**Compare laptop prices across platforms and export:**
```bash
malaysia-scraper --keyword "laptop" --platforms shopee,lazada,mudah --limit 100 --export csv
```

**Search specific platform only:**
```bash
malaysia-scraper --keyword "phone case" --platforms shopee --limit 50 --export json
```

All exported files are automatically saved to the `exports/` directory.

## 🏗️ Project Structure

```
malaysia-marketplace-scrapper-1/
├── main.py                    # Entry point and CLI interface
├── multi_platform_scraper.py  # Core scraper orchestration
├── advanced_analyzer.py       # Analysis and intelligence engine
├── config.py                  # Configuration and constants
├── logger.py                  # Professional logging system
├── base_scraper.py           # Base scraper class
├── shopee_scraper.py         # Shopee-specific implementation
├── lazada_scraper.py         # Lazada-specific implementation
├── mudah_scraper.py          # Mudah.my-specific implementation
├── facebook_marketplace_scraper.py  # Facebook Marketplace implementation
├── tokopedia_scraper.py      # Tokopedia-specific implementation
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installation configuration
├── pyproject.toml            # Modern Python package metadata
├── MANIFEST.in               # Package data file specification
├── install.sh                # Linux/macOS installation script
├── install.bat               # Windows installation script
├── data/                     # Raw scraped data
├── exports/                  # Processed exports (auto-created)
├── logs/                     # Application logs (auto-created)
├── reports/                  # Analysis reports (auto-created)
└── venv/                     # Virtual environment (not included in package)
```

## ⚙️ Configuration

### Platform Configuration
Edit `config.py` to customize platform settings:

```python
SUPPORTED_PLATFORMS = {
    'shopee': {
        'name': 'Shopee',
        'enabled': True,
        'region': 'id'
    },
    # ... other platforms
}
```

### Scraping Parameters
Adjust default scraping behavior:

```python
DEFAULT_CONFIG = {
    'max_results_per_platform': 50,
    'request_timeout': 30,
    'retry_attempts': 3,
    'delay_between_requests': 1.0,
    'concurrent_requests': 5
}
```

## 📊 Output Formats

### JSON Export
```json
{
  "search_metadata": {
    "keyword": "laptop gaming",
    "timestamp": "2025-07-04T09:03:23",
    "total_products": 150
  },
  "products": [
    {
      "name": "ASUS ROG Gaming Laptop",
      "price": 15000000,
      "rating": 4.8,
      "platform": "shopee",
      "merchant": "ASUS Official Store"
    }
  ],
  "analysis": {
    "price_analysis": {
      "min_price": 8000000,
      "max_price": 25000000,
      "avg_price": 15500000
    }
  }
}
```

### Analysis Reports
- **Price Distribution**: Statistical analysis of pricing trends
- **Rating Insights**: Quality assessment across platforms
- **Market Share**: Platform and merchant analysis
- **Competitive Intelligence**: Cross-platform price comparison

## 🔧 Advanced Features

### Custom Scrapers
Extend the base scraper for new platforms:

```python
from base_scraper import BaseScraper

class NewPlatformScraper(BaseScraper):
    def __init__(self, country='id'):
        super().__init__(country)
        self.base_url = 'https://newplatform.co.id'
    
    def search_products(self, keyword, limit=50):
        # Implementation
        pass
```

### Analytics Integration
Access advanced analytics programmatically:

```python
from advanced_analyzer import AdvancedAnalyzer

analyzer = AdvancedAnalyzer()
results = analyzer.analyze_products(product_data)
print(results['price_analysis'])
```

## 🐛 Troubleshooting

### Installation Issues

**Package Installation Fails:**
```bash
# Solution 1: Install in editable mode with verbose output
pip install -e . -v

# Solution 2: Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel
pip install -e .

# Solution 3: Install dependencies manually first
pip install -r requirements.txt
pip install -e .
```

**Command Not Found (malaysia-scraper):**
```bash
# Make sure you installed the package
pip install -e .

# Or reinstall
pip uninstall malaysia-marketplace-scraper
pip install -e .

# Check if it's in your PATH
which malaysia-scraper

# If still not working, use python -m
python -m main
```

**Metadata Generation Failed Error:**
```bash
# Solution 1: Upgrade pip and build tools
pip install --upgrade pip setuptools wheel

# Solution 2: Install packages individually
pip install requests beautifulsoup4 selenium pandas lxml
pip install fake-useragent python-dotenv openpyxl
pip install plotly wordcloud matplotlib seaborn numpy

# Solution 3: Use conda instead of pip
conda install requests beautifulsoup4 selenium pandas lxml
conda install -c conda-forge fake-useragent python-dotenv openpyxl
```

**SSL Certificate Errors:**
```bash
pip install --upgrade certifi requests
# Or on macOS:
/Applications/Python\ 3.x/Install\ Certificates.command
```

**Virtual Environment Issues:**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install --upgrade pip setuptools wheel
```

### Runtime Issues

**Export Not Working / Files Not Saving:**
- Fixed in v1.0.0! All exports now automatically save to `exports/` directory
- The directory is created automatically if it doesn't exist
- Check `exports/` directory for your exported files
- If you see "Export failed" errors, check the logs for details

**Rate Limiting:**
- Increase delay between requests in `config.py`
- Reduce concurrent request count
- Use VPN if IP is temporarily blocked

**Missing Dependencies:**
```bash
# If installed as package
pip install -e . --upgrade

# If using requirements.txt
pip install -r requirements.txt --upgrade
```

**Permission Errors:**
```bash
# Use --user flag if global installation fails
pip install --user -e .
```

**Module Import Errors:**
```bash
# Make sure you're in the correct directory
cd /path/to/malaysia-marketplace-scrapper-1

# Reinstall in editable mode
pip install -e .
```

### Logging
Check `logs/scraper.log` for detailed error information:

```bash
tail -f logs/scraper.log
```

**Note**: Log files are automatically excluded from git tracking to prevent large file issues. The `logs/` directory and `*.log` files are in `.gitignore`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## 📦 Package Distribution

### Building the Package

To build a distributable package:

```bash
# Install build tools
pip install build

# Build the package
python -m build

# This creates:
# - dist/malaysia_marketplace_scraper-1.0.0-py3-none-any.whl
# - dist/malaysia-marketplace-scraper-1.0.0.tar.gz
```

### Installing from Built Package

```bash
# Install the wheel file
pip install dist/malaysia_marketplace_scraper-1.0.0-py3-none-any.whl

# Or install from source distribution
pip install dist/malaysia-marketplace-scraper-1.0.0.tar.gz
```

### Uninstalling

```bash
pip uninstall malaysia-marketplace-scraper
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Roadmap

### Upcoming Features
- [ ] **Web Dashboard**: Real-time monitoring and control panel
- [ ] **API Endpoints**: RESTful API for programmatic access
- [ ] **Database Integration**: PostgreSQL/MongoDB support
- [ ] **Machine Learning**: Price prediction and trend analysis
- [ ] **Mobile App**: React Native companion app
- [ ] **Cloud Deployment**: Docker containers and Kubernetes support

### Platform Expansion
- [ ] Blibli support
- [ ] Bukalapak integration
- [ ] Amazon Indonesia
- [ ] JD.ID support

## 💡 Use Cases

### Market Research
- **Competitive Analysis**: Compare pricing strategies across platforms
- **Product Discovery**: Identify trending products and categories
- **Market Entry**: Assess market saturation and opportunities

### Business Intelligence
- **Price Monitoring**: Track competitor pricing in real-time
- **Inventory Planning**: Analyze product availability and stock levels
- **Vendor Analysis**: Evaluate merchant performance and ratings

### Academic Research
- **E-commerce Studies**: Analyze Indonesian digital market trends
- **Consumer Behavior**: Study purchasing patterns and preferences
- **Economic Analysis**: Monitor inflation and price changes

## 📞 Support

For questions, issues, or feature requests:

- **GitHub Issues**: [Create an issue](https://github.com/your-repo/issues)
- **Email**: your-email@domain.com
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)

---

**Made with ❤️ for the Indonesian e-commerce ecosystem**

*Last updated: July 4, 2025*
