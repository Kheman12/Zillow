# Zillow Scraper Documentation

## Overview
This script scrapes real estate listings from Zillow using their asynchronous API endpoint. It collects property details such as address, price, number of bedrooms and bathrooms, and area size. The scraped data is then saved into an Excel file for further analysis.

## Requirements
- Python
- Required Libraries: `requests`, `json`, `pandas`
- A valid Zillow session cookie (necessary for authentication)

## Script Breakdown

### 1. Setting Up the Request
- The script sends a `PUT` request to the Zillow API endpoint:
  ```python
  url = "https://www.zillow.com/async-create-search-page-state"
  ```
- Custom headers are used to mimic a real browser request, including `user-agent`, `referer`, and `cookie` for authentication.
- The `searchQueryState` JSON payload specifies the search parameters such as location (Arizona), pagination, and sorting order.

### 2. Scraping Multiple Pages
- A loop runs up to `max_pages = 30`, iterating through multiple pages of listings.
- Each request updates the `currentPage` parameter:
  ```python
  "pagination": { "currentPage": page }
  ```
- If access is denied (`403` error), the script stops and alerts the user.
- If no listings are found on a page, scraping halts to avoid unnecessary requests.

### 3. Extracting and Storing Data
- The script extracts relevant fields from the JSON response:
  ```python
  "address": listing.get("address", "N/A"),
  "price": listing.get("price", "N/A"),
  "bedrooms": listing.get("beds", "N/A"),
  "bathrooms": listing.get("baths", "N/A"),
  "area": f"{listing.get('area', 'N/A')} sqft"
  ```
- Data is stored in a Pandas DataFrame.
- Finally, the data is saved as an Excel file:
  ```python
  df.to_excel('zillow_data.xlsx', index=False)
  ```

## Error Handling
- `403 Forbidden`: Indicates an issue with headers or session cookies. The script stops execution.
- Empty Listings: If no results are returned, the script stops to avoid redundant requests.

## Output
- The scraped data is stored in `zillow_data.xlsx` in tabular format.
- Fields include `address`, `price`, `bedrooms`, `bathrooms`, and `area`.

## Disclaimer
Scraping Zillow may violate its terms of service. Ensure compliance with their policies before running this script.


