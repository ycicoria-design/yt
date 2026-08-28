from youtube_engine import get_shorts, analyze_keywords, analyze_hashtags, viral_velocity
from strategy_engine import generate_report


def master_viral_analysis(topic):
    print("Collecting viral YouTube Shorts data...")

    videos = get_shorts(topic)

    if not videos:
        return {
            "success": False,
            "message": "No videos found for this topic."
        }

    keywords = []

    try:
        for word, count in analyze_keywords(videos):
            keywords.append({
                "keyword": word,
                "count": count
            })
    except Exception as e:
        keywords = [{"error": str(e)}]


    hashtags = []

    try:
        for item in analyze_hashtags(videos):

            if len(item) == 4:
                tag, score, status, data = item

                hashtags.append({
                    "hashtag": tag,
                    "score": score,
                    "status": status,
                    "data": data
                })

            elif len(item) == 2:
                tag, count = item

                hashtags.append({
                    "hashtag": tag,
                    "score": min(100, count * 5),
                    "count": count
                })

    except Exception as e:
        hashtags = [{"error": str(e)}]


    freshness = {
        "Last hour": 0,
        "Last 6 hours": 0,
        "Last 24 hours": 0,
        "Last 7 days": 0
    }


    for video in videos:
        age = video.get("hours_old", 999)

        if age <= 1:
            freshness["Last hour"] += 1

        elif age <= 6:
            freshness["Last 6 hours"] += 1

        elif age <= 24:
            freshness["Last 24 hours"] += 1

        elif age <= 168:
            freshness["Last 7 days"] += 1


    try:
        velocity = viral_velocity(videos)
    except Exception:
        velocity = None


    return {
        "success": True,
        "topic": topic,
        "videos_analyzed": len(videos),
        "keywords": keywords,
        "hashtags": hashtags,
        "freshness": freshness,
        "viral_velocity": velocity,
        "videos": videos
    }
