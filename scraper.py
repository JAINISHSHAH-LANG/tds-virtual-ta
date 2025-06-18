import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_discourse(base_url, start_date, end_date):
    output = []
    for page in range(0, 100):  # Adjust range as needed
        url = f"{base_url}/latest.json?page={page}"
        res = requests.get(url)
        if res.status_code != 200:
            break

        posts = res.json().get("topic_list", {}).get("topics", [])
        for post in posts:
            created_at = post["created_at"][:10]
            if start_date <= created_at <= end_date:
                output.append({
                    "title": post["title"],
                    "url": f"{base_url}/t/{post['slug']}/{post['id']}",
                    "created_at": created_at
                })
    return output

if __name__ == "__main__":
    base_url = "https://discourse.onlinedegree.iitm.ac.in"
    start_date = "2025-01-01"
    end_date = "2025-04-14"
    data = scrape_discourse(base_url, start_date, end_date)
    for d in data:
        print(d)

