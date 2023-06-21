# Email Scrapper 📩🕵️‍♂️

A simple Python script to search and collect email addresses associated with a domain on Google search results.

## Features ✨

- Google search for email addresses associated with a domain
- Beautiful Soup for web scraping
- Random User-Agent selection to bypass request restrictions
- Optional proxy support to avoid IP blocking
- Save results to an output file

## Requirements 📦

- Python 3.x
- BeautifulSoup
- googlesearch-python
- requests
- fake_useragent

To install the required packages, run:

```bash
pip install beautifulsoup4 googlesearch-python requests fake_useragent
```

## Usage 🚀

1. Clone the repository:

```bash
git clone https://github.com/TomnzIT/mailScraper.git
cd email-scrapper
```

2. Run the script with the required arguments:

```bash
python email_scrapper.py -d example.com -o output.txt -n 10 -p proxies.txt
```

### Command-line arguments 📝

- `-d`, `--domain`: Domain for email address search (required)
- `-o`, `--output`: Output file path to save the results (optional)
- `-n`, `--num-results`: Number of results to retrieve (default: 10)
- `-p`, `--proxies`: Proxy file path (optional)

## Disclaimer ⚠️

This script is for educational purposes only. Be cautious and respectful of websites' terms of service and privacy policies. Do not use it for any illegal activities or to invade someone's privacy. The developer of this script is not responsible for any misuse or consequences.
