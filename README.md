# TDS Virtual TA
A virtual teaching assistant for IIT Madras' Online Degree in Data Science (Jan–Apr 2025 Tools in Data Science).

## Features
- Answers student questions using scraped Discourse posts and course content.
- Accepts POST requests with questions and optional images.
- Returns JSON response with an answer and relevant links.

## Sample Request
```bash
curl -Uri "http://127.0.0.1:5000/api/" -Method POST -Body '{"question": "Which GPT model should I use for GA5?"}' -ContentType "application/json"
