from youtube_engine import get_shorts, analyze_keywords, analyze_hashtags, viral_velocity
from strategy_engine import generate_report


print("🔥 AI VIRAL SHORTS ANALYZER PRO")
print("=" * 35)


topic = input("\n🎬 What video niche/topic are you analyzing? ")


print("\n📡 Collecting viral YouTube Shorts data...")


videos = get_shorts(topic)


if not videos:
    print("No videos found.")
    exit()


print("\n📊 DATA FOUND:")
print("Videos analyzed:", len(videos))

print("
🚀 VIRAL VELOCITY RADAR")
print("="*30)
for v in viral_velocity(videos)[:5]:
    print(v["title"], "|", v["views_hour"], "views/hour")


print("\n🔥 TOP KEYWORDS:")
for word, count in analyze_keywords(videos):
    print("-", word, count)


print("\n🎯 TOP HASHTAGS:")
for tag, count in analyze_hashtags(videos):
    print("-", tag, count)


idea = input(
    "\n💡 Describe your exact video idea: "
)


generate_report(
    idea,
    videos
)


print("\n✅ Analysis Complete")
