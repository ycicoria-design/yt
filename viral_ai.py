import os
import sys
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build

KEY_FILE = ".youtube_api_key"

def get_api_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = f.read().strip()
            if key: return key
    key = input("Paste your Google API key here: ").strip()
    if key:
        with open(KEY_FILE, "w") as f: f.write(key)
    return key

API_KEY = get_api_key()
if not API_KEY: sys.exit(1)

youtube = build('youtube', 'v3', developerKey=API_KEY)

def run_viral_analysis(topic):
    print(f"\n🔥 PRO CREATOR ASSISTANT: {topic.upper()} 🔥")
    
    # Pulled with English language targeting to keep text readable and clean
    res_all = youtube.search().list(part="snippet", q=f"{topic} #shorts", type="video", order="viewCount", relevanceLanguage="en", maxResults=5).execute().get("items", [])
    
    today_utc = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    res_today = youtube.search().list(part="snippet", q=f"{topic} #shorts", type="video", order="viewCount", publishedAfter=today_utc, relevanceLanguage="en", maxResults=5).execute().get("items", [])
    
    print("\n🏆 ALL-TIME TOP TITLES (Evergreen):")
    titles = []
    for i, item in enumerate(res_all, 1):
        t = item["snippet"]["title"]
        print(f"- {t} | Score: {95 - (i * 2)}")
        titles.append(t)
        
    print("\n🚀 FRESH TODAY (Last 24 Hours):")
    if res_today:
        for i, item in enumerate(res_today, 1):
            t = item["snippet"]["title"]
            print(f"- {t} | Trend Score: {98 - (i * 2)}")
            titles.append(t)
    else:
        print("- (No major English shorts dropped in 24h; utilizing evergreen pool)")

    print("\n#️⃣ TOP 3 OPTIMAL HASHTAGS:")
    stopwords = {"with", "never", "use", "this", "that", "from", "your", "have", "what", "into", "just", "about", "how", "the", "and", "for", "you", "are", "can", "out"}
    
    words = []
    for t in titles:
        for w in t.split():
            c = "".join(filter(str.isalnum, w)).lower()
            if len(c) > 3 and c not in stopwords and c != topic.replace(" ", ""):
                if c not in words:
                    words.append(c)
                    
    clean_topic = topic.replace(" ", "")
    # Exactly 3 professional tags: Topic, #shorts, and top viral keyword modifier
    tags = [
        f"#{clean_topic}",
        "#shorts",
        f"#{words[0]}" if words else "#viral"
    ]
    print(" ".join(tags))
    print("\n✅ OPTIMIZED ANALYSIS COMPLETE\n")

if __name__ == "__main__":
    t = input("Enter video topic: ").strip()
    if t: run_viral_analysis(t)
