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
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.cbp.gov/newsroom")

    time.sleep(5)  # Wait for JS content to load

    articles = driver.find_elements(By.CSS_SELECTOR, "div.views-row")

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

    with open("customs_risks.json", "w") as f:
        json.dump(scraped_data, f, indent=2)

    print(f"Saved {len(scraped_data)} articles to customs_risks.json")

if __name__ == "__main__":
    scrape_cbp_newsroom()
