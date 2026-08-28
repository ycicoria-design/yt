from youtube_engine import get_shorts, analyze_keywords, analyze_hashtags, viral_velocity
from strategy_engine import generate_report

topic = input("\n🎬 What video niche/topic are you analyzing? ")

print("\n📡 Collecting viral YouTube Shorts data...")

videos = get_shorts(topic)

if not videos:
    print("No videos found.")
    exit()

print("\n📊 DATA FOUND:")
print("Videos analyzed:", len(videos))

print("\n🔥 TOP KEYWORDS:")
for word, count in analyze_keywords(videos):
    print("-", word, count)

print("\n🎯 TOP HASHTAGS:")
for tag, score, status, data in analyze_hashtags(videos):
    print("-", tag, count)

print("\n⚡ VIRAL FRESHNESS RADAR")
print("=" * 35)

fresh = {
    "Last hour": 0,
    "Last 6 hours": 0,
    "Last 24 hours": 0,
    "Last 7 days": 0
}

for v in videos:
    age = v.get("hours_old", 999)

    if age <= 1:
        fresh["Last hour"] += 1
    elif age <= 6:
        fresh["Last 6 hours"] += 1
    elif age <= 24:
        fresh["Last 24 hours"] += 1
    elif age <= 168:
        fresh["Last 7 days"] += 1

for k,v in fresh.items():
    print("-", k, ":", v)

print("\n🔥 HASHTAG VIRAL SCORES")
print("=" * 35)

for tag,count in analyze_hashtags(videos):
    score = min(100, count * 5)
    print(f"#{tag} | Score {score}/100 | Used {count} times")

idea = input("\n💡 Describe your exact video idea: ")

generate_report(idea, videos)
