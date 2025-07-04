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

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd neru-scrapper
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

## 📖 Usage

### Interactive Mode
Launch the interactive CLI for guided product searches:

```bash
python main.py
```

The interactive mode provides:
- Platform selection
- Search term input
- Real-time progress tracking
- Automatic analysis and export

### Command Line Arguments
```bash
python main.py --keyword "laptop gaming" --limit 50 --platforms shopee tokopedia
```

**Available Arguments:**
- `--keyword`: Search term (required)
- `--limit`: Maximum results per platform (default: 50)
- `--platforms`: Specific platforms to search (default: all enabled)
- `--output`: Output format (json, csv, excel)
- `--export-dir`: Custom export directory

### Example Usage

**Search for baby care products:**
```bash
python main.py --keyword "baby care" --limit 30
```

**Compare laptop prices across platforms:**
```bash
python main.py --keyword "laptop" --platforms shopee tokopedia lazada --limit 100
```

## 🏗️ Project Structure

```
neru-scrapper/
├── main.py                    # Entry point and CLI interface
├── multi_platform_scraper.py  # Core scraper orchestration
├── advanced_analyzer.py       # Analysis and intelligence engine
├── config.py                  # Configuration and constants
├── logger.py                  # Professional logging system
├── base_scraper.py           # Base scraper class
├── shopee_scraper.py         # Shopee-specific implementation
├── tokopedia_scraper.py      # Tokopedia-specific implementation
├── lazada_scraper.py         # Lazada-specific implementation
├── requirements.txt          # Python dependencies
├── data/                     # Raw scraped data
├── exports/                  # Processed exports
├── logs/                     # Application logs
├── reports/                  # Analysis reports
└── visualizations/           # Generated charts and graphs
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

**Rate Limiting:**
- Increase delay between requests in `config.py`
- Reduce concurrent request count
- Use VPN if IP is temporarily blocked

**Missing Dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

**Permission Errors:**
```bash
# Use --user flag if global installation fails
pip install --user -r requirements.txt
```

### Logging
Check `logs/scraper.log` for detailed error information:

```bash
tail -f logs/scraper.log
```

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
