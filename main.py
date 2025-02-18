import requests
import json
import pandas as pd

url = "https://www.zillow.com/async-create-search-page-state"
headers = {
  'accept': '*/*',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'cache-control': 'no-cache',
  'content-type': 'application/json',
  'origin': 'https://www.zillow.com',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://www.zillow.com/az/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-120.56616090624999%2C%22east%22%3A-103.29565309374999%2C%22south%22%3A28.641943263154513%2C%22north%22%3A39.44428523080873%7D%2C%22usersSearchTerm%22%3A%22arizona%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A8%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A6%7D&category=RECENT_SEARCH',
  'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
  'Cookie': 'search=6|1742468394704%7Crect%3D39.44428523080873%2C-103.29565309374999%2C28.641943263154513%2C-120.56616090624999%26rid%3D8%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%098%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; zgsession=1|6c696c87-1a27-454f-a444-c0dc6269d3a0; zguid=24|%246a2dbcec-0e20-4582-a065-c785231bde25'
}

all_listings = []
max_pages = 30 # Set the number of pages you want to scrape

for page in range(1, max_pages + 1):
    payload = json.dumps({
        "searchQueryState": {
            "pagination": {
                "currentPage": page
            },
            "isMapVisible": False,
            "mapBounds": {
                "west": -120.56616090624999,
                "east": -103.29565309374999,
                "south": 28.641943263154513,
                "north": 39.44428523080873
            },
            "usersSearchTerm": "arizona",
            "regionSelection": [
                {
                    "regionId": 8
                }
            ],
            "filterState": {
                "sortSelection": {
                    "value": "globalrelevanceex"
                }
            },
            "isListVisible": True,
            "mapZoom": 6
        },
        "wants": {
            "cat1": [
                "listResults"
            ],
            "cat2": [
                "total"
            ]
        },
        "requestId": page,
        "isDebugRequest": False
    })

    response = requests.request("PUT", url, headers=headers, data=payload)

    if response.status_code == 403:
        print(f"Access denied on page {page}. Check headers or cookies.")
        break

    data = response.json()
    listings = data.get("cat1", {}).get("searchResults", {}).get("listResults", [])

    if not listings:
        print(f"No more listings found on page {page}. Stopping.")
        break

    for listing in listings:
        all_listings.append({
            "address": listing.get("address", "N/A"),
            "price": listing.get("price", "N/A"),
            "bedrooms": listing.get("beds", "N/A"),
            "bathrooms": listing.get("baths", "N/A"),
            "area": f"{listing.get('area', 'N/A')} sqft"
        })

    print(f"Page {page} scraped successfully.")

df = pd.DataFrame(all_listings)
df.to_excel('zillow_data.xlsx', index=False)
print("Scraping completed. Data saved to 'zillow_data.json'.")
