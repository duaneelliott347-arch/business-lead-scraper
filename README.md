# Business Lead Scraper

A comprehensive Python tool for scraping business leads from Google Maps and Yelp. This tool extracts business information including name, address, phone number, website, ratings, and review counts.

## Features

- **Multi-source scraping**: Supports both Google Maps and Yelp
- **Comprehensive data extraction**: Name, address, phone, website, email, ratings, review counts
- **Rate limiting**: Built-in delays to prevent overwhelming servers
- **Error handling**: Graceful handling of missing data and network issues
- **Data export**: Export to CSV and JSON formats
- **Duplicate removal**: Automatically removes duplicate entries
- **Configurable**: Command-line interface with multiple options

## Installation

1. **Clone or download the repository**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver**:
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Make sure it's in your PATH or place it in the same directory as the script
   - Alternatively, use webdriver-manager (included in requirements.txt) for automatic management

## Usage

### Basic Usage

```bash
python business_lead_scraper.py --keyword "restaurant" --location "New York"
```

### Advanced Usage

```bash
python business_lead_scraper.py \
  --keyword "plumber" \
  --location "Los Angeles" \
  --source both \
  --max-results 100 \
  --output-format csv \
  --output-dir ./results
```

### Command Line Arguments

- `--keyword`: Business type to search for (required)
- `--location`: Location to search in (required)
- `--source`: Source to scrape from (`google`, `yelp`, or `both`) - default: `both`
- `--max-results`: Maximum results per source - default: `50`
- `--output-format`: Output format (`csv`, `json`, or `both`) - default: `both`
- `--output-dir`: Output directory - default: `./output`
- `--headless`: Run browser in headless mode - default: `True`

## Output

The scraper generates files with the following naming convention:
```
{keyword}_{location}_{timestamp}.csv
{keyword}_{location}_{timestamp}.json
```

### CSV Output Format
```csv
name,address,phone,website,email,source,rating,review_count
"Joe's Pizza","123 Main St, New York, NY","(555) 123-4567","https://joespizza.com","","Google Maps","4.5","150 reviews"
```

### JSON Output Format
```json
[
  {
    "name": "Joe's Pizza",
    "address": "123 Main St, New York, NY",
    "phone": "(555) 123-4567",
    "website": "https://joespizza.com",
    "email": "",
    "source": "Google Maps",
    "rating": "4.5",
    "review_count": "150 reviews"
  }
]
```

## Code Structure

### Main Classes

1. **BusinessLead**: Data class for storing business information
2. **RateLimiter**: Manages request timing to prevent overwhelming servers
3. **GoogleMapsScraper**: Handles Google Maps scraping logic
4. **YelpScraper**: Handles Yelp scraping logic
5. **DataExporter**: Exports data to various formats

### Key Features

- **Error Handling**: Graceful handling of missing elements and network issues
- **Rate Limiting**: Random delays between requests (1-3 seconds)
- **Data Validation**: Checks for required fields before saving
- **Duplicate Removal**: Removes duplicates based on name and address
- **Logging**: Comprehensive logging for debugging and monitoring

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**:
   - Install ChromeDriver and add to PATH
   - Or use webdriver-manager: `pip install webdriver-manager`

2. **Timeout errors**:
   - Increase wait times in the code
   - Check internet connection
   - Some sites may be blocking automated requests

3. **No results found**:
   - Try different keywords or locations
   - Check if the search terms are too specific
   - Verify the target websites are accessible

4. **Permission errors**:
   - Make sure output directory is writable
   - Run with appropriate permissions

### Performance Tips

- Use `--headless` mode for faster execution
- Reduce `--max-results` for quicker testing
- Monitor rate limiting if getting blocked

## Legal and Ethical Considerations

- **Respect robots.txt**: Check website policies before scraping
- **Rate limiting**: Don't overwhelm servers with requests
- **Terms of service**: Review and comply with website terms
- **Data usage**: Use scraped data responsibly and legally
- **Personal data**: Be mindful of privacy regulations (GDPR, CCPA, etc.)

## Extending the Scraper

### Adding New Sources

1. Create a new scraper class following the pattern of `GoogleMapsScraper`
2. Implement the `search_businesses` method
3. Add extraction logic for the specific website structure
4. Update the main function to include the new source

### Customizing Data Fields

1. Modify the `BusinessLead` dataclass to add new fields
2. Update extraction methods in scraper classes
3. Modify the `DataExporter` class to handle new fields

## Dependencies

- **selenium**: Web browser automation
- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests
- **lxml**: XML/HTML parser
- **pandas**: Data manipulation (optional, for advanced features)
- **webdriver-manager**: Automatic ChromeDriver management

## License

This project is provided as-is for educational and research purposes. Please ensure compliance with applicable laws and website terms of service when using this tool.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for ensuring their use complies with applicable laws, regulations, and website terms of service. The authors are not responsible for any misuse of this tool.
