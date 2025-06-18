# import requests
# import json
# from datetime import datetime

# BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
# CATEGORY_SLUG = "tools-in-data-science"

# def get_posts(start_date, end_date, limit=50):
#     collected_posts = []
#     for page in range(0, 20):  # 20 pages ≈ 1000 posts
#         response = requests.get(f"{BASE_URL}/c/{CATEGORY_SLUG}.json?page={page}")
#         if response.status_code != 200:
#             break
#         data = response.json()
#         for topic in data.get("topic_list", {}).get("topics", []):
#             created_at = topic.get("created_at", "")
#             if not created_at:
#                 continue
#             created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
#             if start_date <= created_dt <= end_date:
#                 topic_id = topic["id"]
#                 topic_slug = topic["slug"]
#                 post_resp = requests.get(f"{BASE_URL}/t/{topic_slug}/{topic_id}.json")
#                 if post_resp.status_code != 200:
#                     continue
#                 post_data = post_resp.json()
#                 for post in post_data.get("post_stream", {}).get("posts", []):
#                     collected_posts.append({
#                         "topic_id": topic_id,
#                         "topic_slug": topic_slug,
#                         "post_number": post["post_number"],
#                         "raw": post["raw"]
#                     })
#     return collected_posts

# if __name__ == "__main__":
#     from datetime import datetime
#     posts = get_posts(
#         datetime(2025, 1, 1),
#         datetime(2025, 4, 14)
#     )
#     with open("tds_posts.json", "w", encoding="utf-8") as f:
#         json.dump(posts, f, indent=2)
# # python discourse_scraper.py

import requests
import json
from datetime import datetime

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_SLUG = "tools-in-data-science"  # Optional: change if not valid

def get_posts(start_date, end_date, limit=50):
    collected_posts = []
    print("🔍 Starting scrape...")

    for page in range(0, 5):  # 5 pages ≈ 250 topics
        url = f"{BASE_URL}/c/{CATEGORY_SLUG}.json?page={page}"
        print(f"📄 Fetching: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Failed to fetch page {page}, status code: {response.status_code}")
            break

        data = response.json()
        topics = data.get("topic_list", {}).get("topics", [])
        print(f"📌 Found {len(topics)} topics on page {page}")

        for topic in topics:
            created_at = topic.get("created_at", "")
            if not created_at:
                continue
            created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            if start_date <= created_dt <= end_date:
                topic_id = topic["id"]
                topic_slug = topic["slug"]
                topic_url = f"{BASE_URL}/t/{topic_slug}/{topic_id}.json"
                print(f"🔗 Fetching topic: {topic_url}")

                post_resp = requests.get(topic_url)
                if post_resp.status_code != 200:
                    print(f"⚠️ Failed to fetch topic {topic_id}")
                    continue

                post_data = post_resp.json()
                for post in post_data.get("post_stream", {}).get("posts", []):
                    collected_posts.append({
                        "topic_id": topic_id,
                        "topic_slug": topic_slug,
                        "post_number": post["post_number"],
                        "raw": post["raw"]
                    })

    print(f"✅ Total posts collected: {len(collected_posts)}")
    return collected_posts

if __name__ == "__main__":
    posts = get_posts(
        datetime(2025, 1, 1),
        datetime(2025, 4, 14)
    )
    if posts:
        with open("tds_posts.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2)
        print("📁 Saved to tds_posts.json")
    else:
        print("⚠️ No posts found or saved.")
