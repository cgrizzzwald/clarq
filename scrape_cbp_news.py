from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
import time

def scrape_cbp_newsroom():
    options = Options()
    # Comment this out to debug with visible browser
    options.add_argument("--headless") # options.
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.cbp.gov/newsroom/national-media-release")

    time.sleep(5)  # Wait for JS to load

    articles = driver.find_elements(By.CSS_SELECTOR, "div.views-row")

    print(f"Found {len(articles)} article blocks")

    scraped_data = []

    for article in articles:
        try:
            title_tag = article.find_element(By.CSS_SELECTOR, "h3 a")
            date_tag = article.find_element(By.CSS_SELECTOR, ".date-display-single")
            summary_tag = article.find_element(By.CSS_SELECTOR, ".field-content")

            title = title_tag.text.strip()
            link = title_tag.get_attribute("href")
            if not link.startswith("http"):
                link = "https://www.cbp.gov" + link
            date = datetime.strptime(date_tag.text.strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
            summary = summary_tag.text.strip()

            scraped_data.append({
                "source": "U.S. CBP Media Release",
                "title": title,
                "summary": summary,
                "date": date,
                "link": link,
                "risk_type": "customs_regulation"
            })
        except Exception as e:
            print("Skipped article due to error:", e)

    driver.quit()

    with open("customs_risks.json", "w") as f:
        json.dump(scraped_data, f, indent=2)

    print(f"Saved {len(scraped_data)} articles to customs_risks.json")

if __name__ == "__main__":
    scrape_cbp_newsroom()
