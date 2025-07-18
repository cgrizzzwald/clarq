import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_cbp_newsroom():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
    driver.get("https://www.cbp.gov/newsroom/media-releases/all")

    time.sleep(5)  # Wait for JS content to load
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_google_news(query):
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for g in soup.select(".dbsr, .SoaBEf"):
        a_tag = g.find("a", href=True)
        title_tag = g.find("div", attrs={"role": "heading"}) or g.find("div", class_="nDgy9d")
        snippet_tag = g.find("div", class_="Y3v8qd") or g.find("div", class_="GI74Re") or g.find("div", class_="st")

        if a_tag and title_tag:
            title = title_tag.get_text(strip=True)
            url = a_tag["href"]
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            if title and url.startswith("http"):
                results.append({
                    "source": "Google News",
                    "title": title,
                    "summary": snippet,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "link": url,
                    "risk_type": "customs_regulation"
                })

    scraped_data = []

    for article in articles:
        try:
            title_tag = article.find_element(By.TAG_NAME, "h3")
            link_tag = title_tag.find_element(By.TAG_NAME, "a")
            summary_tag = article.find_element(By.CLASS_NAME, "field-content")
            date_tag = article.find_element(By.CLASS_NAME, "date-display-single")

            title = title_tag.text.strip()
            summary = summary_tag.text.strip()
            date = datetime.strptime(date_tag.text.strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
            link = link_tag.get_attribute("href")

            scraped_data.append({
                "source": "U.S. CBP Newsroom",
                "title": title,
                "summary": summary,
                "date": date,
                "link": link,
                "risk_type": "customs_regulation"
            })
        except Exception as e:
            print(f"Skipping article due to error: {e}")

    driver.quit()
    return results[:4]

def main():
    query = "customs delays import duties site:cbp.gov OR site:ustr.gov"
    print(f"🔍 Searching: {query}")
    articles = fetch_google_news(query)

    with open("customs_risks.json", "w") as f:
        json.dump(articles, f, indent=2)

    print(f"✅ Saved {len(articles)} customs-related articles to customs_risks.json")

if __name__ == "__main__":
    main()
