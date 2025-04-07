import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

CBP_URL = "https://www.cbp.gov/newsroom"

def scrape_cbp_newsroom():
    response = requests.get(CBP_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('div', class_='views-row')
    scraped_data = []

    for article in articles:
        title_tag = article.find('h3')
        summary_tag = article.find('div', class_='field-content')
        date_tag = article.find('span', class_='date-display-single')

        if title_tag and summary_tag and date_tag:
            title = title_tag.get_text(strip=True)
            summary = summary_tag.get_text(strip=True)
            date_str = date_tag.get_text(strip=True)

            try:
                date_obj = datetime.strptime(date_str, "%m/%d/%Y")
                date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                date = date_str

            link_tag = title_tag.find('a')
            link = "https://www.cbp.gov" + link_tag['href'] if link_tag and 'href' in link_tag.attrs else None

            scraped_data.append({
                "source": "U.S. CBP Newsroom",
                "title": title,
                "summary": summary,
                "date": date,
                "link": link,
                "risk_type": "customs_regulation"
            })

    return scraped_data

def save_to_json(data, filename="customs_risks.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    cbp_data = scrape_cbp_newsroom()
    save_to_json(cbp_data)
    print(f"Saved {len(cbp_data)} articles to customs_risks.json")

