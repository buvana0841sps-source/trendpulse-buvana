import requests
import time
import json
import os
# User-Agent identifies our application
headers = {"User-Agent": "TrendPulse/1.0"}
# URL to get the top Hacker News story IDs
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
# Get the top 500 story IDs
response = requests.get(top_stories_url, headers=headers)
story_ids = response.json()[:500]

print(len(story_ids))
# Keywords used to classify stories into categories
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}
# Count the number of stories collected in each category
category_counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}
# Store all fetched stories
stories = []
# Store the final matching stories
collected_stories = []

# Fetch details for each story
for story_id in story_ids:
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    # Try the request up to 3 times
    for attempt in range(3):
        try:
            story_response = requests.get(
                story_url,
                headers=headers,
                timeout=5
            )

            if story_response.status_code == 200:
                story = story_response.json()
                stories.append(story)
                break

            else:
                print("Failed to fetch story:", story_id)

        except requests.RequestException:
            print("Request failed:", story_id)

        if attempt == 2:
            print("Giving up on story:", story_id)
# Match stories keywords with the category           
for category, keywords in categories.items():
    # Check every fetched story
    for story in stories:
        # Stop when 25 stories are collected for this category
        if category_counts[category] >= 25:
            break

        title = story.get("title", "")
        title_lower = title.lower()

        # Check whether a keyword appears in the title
        for keyword in keywords:
            if keyword.lower() in title_lower:
                # Extract the required fields
                story_data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "collected_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_stories.append(story_data)
                category_counts[category] += 1
                break
    # Wait 2 seconds before processing the next category
    time.sleep(2)
# Display the total number of collected stories
print("Total collected:", len(collected_stories))
# Warn if fewer than 100 stories are found
if len(collected_stories) < 100:
    print("Warning: Fewer than 100 matching stories were found.")
print(category_counts)     
# Create the data folder if it does not exist
os.makedirs("data", exist_ok=True)
# Create the JSON filename using today's date
filename = "data/trends_" + time.strftime("%Y%m%d") + ".json"
# Save the stories to a JSON file
with open(filename, "w", encoding="utf-8") as file:
    json.dump(collected_stories, file, indent=2)

print("Saved to:", filename)