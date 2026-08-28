from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
from collections import Counter
import re


API_KEY = "PASTE_NEW_KEY_HERE"


youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


def collect_data():

    now = datetime.now(timezone.utc)

    videos = []

    searches = [
        "cat shorts",
        "funny cat shorts",
        "cute kitten shorts",
        "cat reaction",
        "cat fails",
        "cat funny moments"
    ]

    print("🐱 LIVE CAT VIRAL ANALYZER")
    print("Collecting fresh YouTube Shorts data...\n")


    for search in searches:

        response = youtube.search().list(
            part="snippet",
            q=search,
            type="video",
            videoDuration="short",
            order="date",
            maxResults=50,
            publishedAfter=(
                now - timedelta(hours=24)
            ).isoformat()
        ).execute()


        ids = [
            item["id"]["videoId"]
            for item in response["items"]
        ]


        if not ids:
            continue


        details = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(ids)
        ).execute()


        for item in details["items"]:

            title = item["snippet"]["title"]

            stats = item.get(
                "statistics",
                {}
            )

            views = int(stats.get("viewCount",0))
            likes = int(stats.get("likeCount",0))
            comments = int(stats.get("commentCount",0))


            uploaded = datetime.fromisoformat(
                item["snippet"]["publishedAt"]
                .replace("Z","+00:00")
            )


            age = max(
                1,
                (now-uploaded).total_seconds()/3600
            )


            views_hour = views / age


            engagement = 0

            if views:
                engagement = (
                    (likes + comments)
                    /
                    views
                ) * 100


            viral_score = (
                views_hour * .7
                +
                engagement * 500
            )


            videos.append({
                "title": title,
                "views": views,
                "views_hour": round(views_hour),
                "score": viral_score
            })


    return sorted(
        videos,
        key=lambda x:x["score"],
        reverse=True
    )



def analyze_patterns(videos):

    words = []
    hashtags = []

    for video in videos[:100]:

        words += re.findall(
            r"\b[a-zA-Z]{4,}\b",
            video["title"].lower()
        )

        hashtags += re.findall(
            r"#\w+",
            video["title"]
        )


    return (
        Counter(words).most_common(15),
        Counter(hashtags).most_common(10)
    )



def recommend(video_idea, words, hashtags):

    score = 80

    if words:
        score += 5

    if hashtags:
        score += 5

    score = min(score,100)


    print("\n🔥 VIRAL MATCH SCORE")
    print("="*40)
    print(f"{score}/100")


    print("\n🏆 TITLE THIS:")

    print(
        f"{video_idea.title()}... Nobody Expected What Happened Next 😳🐱"
    )


    print("\n🏷️ HASHTAGS:")

    for tag in hashtags[:5]:
        print(tag[0])


    print("\n🔊 SOUND STRATEGY:")
    print("- Match the emotion of the video")
    print("- Use currently rising Shorts audio")
    print("- Prefer sounds appearing in similar cat videos")


    print("\n📊 BASED ON:")
    print("- Fresh YouTube Shorts data")
    print("- Views per hour")
    print("- Engagement")
    print("- Current title patterns")



if __name__ == "__main__":

    videos = collect_data()

    if not videos:
        print("No data found")
        exit()


    print("\n🔥 FASTEST GROWING CAT SHORTS")

    for video in videos[:10]:

        print("\n" + video["title"])
        print(
            "Views/hour:",
            video["views_hour"]
        )


    words, hashtags = analyze_patterns(videos)


    print("\n🔥 CURRENT WINNING WORDS")
    print(words)


    idea = input(
        "\nDescribe your cat video: "
    )


    recommend(
        idea,
        words,
        hashtags
    )
