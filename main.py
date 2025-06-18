from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load discourse data
with open("tds_posts.json", "r", encoding="utf-8") as f:
    discourse_posts = json.load(f)

@app.route("/", methods=["GET"])
def index():
    return "✅ Virtual TA API is running."

@app.route("/api/", methods=["POST"])
def virtual_ta():
    data = request.get_json()
    question = data.get("question", "").lower()

    matches = []
    for post in discourse_posts:
        if any(word in post["raw"].lower() for word in question.split()):
            matches.append(post)

    if matches:
        response = {
            "answer": matches[0]["raw"],
            "links": [
                {
                    "url": f"https://discourse.onlinedegree.iitm.ac.in/t/{post['topic_slug']}/{post['topic_id']}/{post['post_number']}",
                    "text": post["raw"][:100] + ("..." if len(post["raw"]) > 100 else "")
                }
                for post in matches[:3]
            ]
        }
    else:
        response = {
            "answer": "Sorry, I couldn't find a relevant post.",
            "links": []
        }

    return jsonify(response)


 
import os

if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )



