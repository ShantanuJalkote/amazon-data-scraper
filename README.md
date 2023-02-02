# Amazon-data-scraper
A Python script that uses Selenium and BeautifulSoup to scrape data from Amazon websites. This script can be used to extract information such 
as Product URL, Product Name, Product Price, Rating, Number of reviews, ASIN, Product Description, • Manufacturer from Amazon pages.

## Requirements
- Python 3.x
- Selenium
- BeautifulSoup
- WebDriver for Chrome or Firefox
## Usage
1. Clone the repository
```bash
git clone https://github.com/your-username/amazon-data-scraper.git
```
2. Install the required packages
```
pip install selenium
pip install beautifulsoup4
```
3. Download the appropriate webdriver for your browser and place it in your PATH, or specify its location in the script.

4. Edit the `amazon_scraper.py` script to include the URL of the Amazon page you want to scrape.

5. Run the script
```
python amazon_scraper.py
```
6. Output
The script will generate a CSV file containing the extracted data.
