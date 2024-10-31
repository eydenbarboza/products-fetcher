# Products Fetcher

## Overview
This project implements basic data fetching and parsing for product information. The following features have been implemented:

- **DataFetcher**: A class to retrieve product data from a specified URL.
- **ProductParser**: A class to parse and extract relevant attributes from the product data.
- **CSVWriter**: A class to output parsed product data into a CSV file.
- **Command-Line Interface**: Allows user input for language selection.
- **Requirements**: Managed dependencies with `requirements.txt` (requests).

## Usage

To run the script and fetch product data, use the following commands:

```bash
python3 fetcher.py --lang en-CR  # For English language
python3 fetcher.py --lang es-CR  # For Spanish language

