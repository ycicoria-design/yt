from youtube_engine import get_cat_shorts
from strategy_engine import generate_report


print("🔥 AI VIRAL SHORTS ANALYZER")
print("============================")
print("Pulling live YouTube Shorts data...\n")


videos = get_cat_shorts()


description = input(
    "\nDescribe your video idea: "
)


generate_report(
    description,
    videos
)
