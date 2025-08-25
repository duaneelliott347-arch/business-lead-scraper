# Installation and Setup Guide

This guide will help you install and set up the Business Lead Scraper on your system.

## System Requirements

- **Python 3.8 or higher**
- **Google Chrome browser** (for web scraping)
- **Internet connection**
- **Operating System**: Windows, macOS, or Linux

## Quick Installation

### Option 1: Automated Setup (Recommended)

1. **Download all files** to a folder on your computer
2. **Open terminal/command prompt** in that folder
3. **Run the setup script**:
   ```bash
   python setup.py
   ```

This will automatically:
- Install all required Python packages
- Download and configure ChromeDriver
- Create necessary directories
- Test the installation

### Option 2: Manual Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install ChromeDriver**:
   - Download from: https://chromedriver.chromium.org/
   - Extract and add to your system PATH
   - Or let webdriver-manager handle it automatically

3. **Create output directory**:
   ```bash
   mkdir output
   ```

## Verification

Test your installation:
```bash
python test_scraper.py
```

## Usage Examples

### 1. Command Line Interface

**Basic usage**:
```bash
python business_lead_scraper.py --keyword "restaurant" --location "New York"
```

**Advanced usage**:
```bash
python business_lead_scraper.py \
  --keyword "plumber" \
  --location "Los Angeles" \
  --source both \
  --max-results 100 \
  --output-format csv \
  --output-dir ./results
```

### 2. Graphical User Interface

**Start the GUI**:
```bash
python gui_scraper.py
```

Features:
- Easy-to-use interface
- Real-time progress tracking
- Live results display
- One-click CSV export

### 3. Batch Processing

**Create sample queries file**:
```bash
python batch_scraper.py --create-sample
```

**Process multiple queries**:
```bash
python batch_scraper.py --queries-file sample_queries.csv
```

### 4. Programmatic Usage

```python
from business_lead_scraper import GoogleMapsScraper, DataExporter

# Initialize scraper
scraper = GoogleMapsScraper(headless=True)

try:
    # Search for leads
    leads = scraper.search_businesses("coffee shop", "Seattle", 20)
    
    # Export results
    DataExporter.to_csv(leads, "coffee_shops_seattle.csv")
    
finally:
    scraper.close()
```

## Configuration

### Basic Configuration

Edit `config.py` to customize:
- Browser settings
- Rate limiting
- Output formats
- Scraping behavior

### Environment Variables

Create a `.env` file for sensitive settings:
```
CHROME_DRIVER_PATH=/path/to/chromedriver
DEFAULT_OUTPUT_DIR=./my_results
LOG_LEVEL=INFO
```

## Troubleshooting

### Common Issues

**1. ChromeDriver not found**
```
Error: 'chromedriver' executable needs to be in PATH
```
**Solution**: 
- Install ChromeDriver manually or run `python setup.py`
- Make sure Chrome browser is installed

**2. Permission denied**
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: 
- Run with administrator/sudo privileges
- Check file/folder permissions
- Use a different output directory

**3. No results found**
```
Found 0 leads
```
**Solution**: 
- Try different keywords or locations
- Check internet connection
- Verify the target websites are accessible
- Try running without headless mode to see what's happening

**4. Timeout errors**
```
TimeoutException: Message: 
```
**Solution**: 
- Increase timeout values in config.py
- Check internet connection speed
- Try with fewer max results

**5. Import errors**
```
ModuleNotFoundError: No module named 'selenium'
```
**Solution**: 
- Run `pip install -r requirements.txt`
- Make sure you're using the correct Python environment

### Performance Tips

1. **Use headless mode** for faster execution:
   ```bash
   python business_lead_scraper.py --keyword "pizza" --location "NYC" --headless
   ```

2. **Reduce max results** for testing:
   ```bash
   python business_lead_scraper.py --keyword "pizza" --location "NYC" --max-results 10
   ```

3. **Use batch processing** for multiple queries:
   ```bash
   python batch_scraper.py --queries-file my_queries.csv
   ```

## Advanced Usage

### Custom Scrapers

Create your own scraper by extending the base classes:

```python
from business_lead_scraper import GoogleMapsScraper

class CustomScraper(GoogleMapsScraper):
    def extract_custom_field(self, element):
        # Your custom extraction logic
        pass
```

### Data Processing

Process scraped data with pandas:

```python
import pandas as pd
from business_lead_scraper import DataExporter

# Load results
df = pd.read_csv('results.csv')

# Filter and analyze
high_rated = df[df['rating'].astype(float) >= 4.5]
by_location = df.groupby('address').size()

# Export processed data
high_rated.to_csv('high_rated_businesses.csv', index=False)
```

### Integration with Other Tools

**Export to Excel**:
```python
import pandas as pd
df = pd.read_csv('results.csv')
df.to_excel('results.xlsx', index=False)
```

**Send to database**:
```python
import sqlite3
import pandas as pd

df = pd.read_csv('results.csv')
conn = sqlite3.connect('leads.db')
df.to_sql('business_leads', conn, if_exists='append', index=False)
```

## File Structure

```
business-lead-scraper/
├── business_lead_scraper.py    # Main scraper module
├── gui_scraper.py             # GUI application
├── batch_scraper.py           # Batch processing
├── config.py                  # Configuration settings
├── setup.py                   # Installation script
├── test_scraper.py           # Test suite
├── example_usage.py          # Usage examples
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation
├── INSTALL.md               # This installation guide
└── output/                  # Results directory
```

## Getting Help

1. **Check the logs**: Look for error messages in the console output
2. **Run tests**: Use `python test_scraper.py` to verify functionality
3. **Try examples**: Run `python example_usage.py` to see working examples
4. **Check configuration**: Review `config.py` for customization options

## Legal Considerations

- **Respect robots.txt**: Check website policies before scraping
- **Rate limiting**: Don't overwhelm servers with requests
- **Terms of service**: Review and comply with website terms
- **Data usage**: Use scraped data responsibly and legally
- **Privacy**: Be mindful of privacy regulations (GDPR, CCPA, etc.)

## Updates and Maintenance

To update the scraper:

1. **Backup your data** and configuration files
2. **Download the latest version** of the scraper files
3. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
4. **Test the updated version**:
   ```bash
   python test_scraper.py
   ```

## Support

If you encounter issues:

1. Check this installation guide
2. Review the main README.md
3. Run the test suite to identify problems
4. Check the configuration settings
5. Try the example scripts to verify functionality

Remember to always use this tool responsibly and in compliance with applicable laws and website terms of service.
