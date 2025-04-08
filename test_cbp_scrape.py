import requests
from bs4 import BeautifulSoup

url = "https://www.cbp.gov/newsroom"
res = requests.get(url)
print("STATUS:", res.status_code)

soup = BeautifulSoup(res.text, "html.parser")

# Print the first few lines of what we got back
print("----- First 1000 chars of the page -----")
print(res.text[:1000])
