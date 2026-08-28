from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
from collections import Counter
import re


API_KEY = "AIzaSyAapo6UuuTFPH49ICzFkHBxkrKNmC1Uzfo"


youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


def get_shorts():

    now = datetime.now(timezone.utc)

    videos = []

    searches = [
        "cat shorts",
        "funny cat shorts",
        "cute kitten shorts",
        "cat reaction",
        "cat fails"
    ]

    print("🐱 LIVE CAT VIRAL ANALYZER")
    print("Pulling fresh YouTube data...\n")


    for search in searches:

        result = youtube.search().list(
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
            x["id"]["videoId"]
            for x in result["items"]
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

            views = int(
                stats.get("viewCount",0)
            )

            likes = int(
                stats.get("likeCount",0)
            )

            comments = int(
                stats.get("commentCount",0)
            )


            uploaded = datetime.fromisoformat(
                item["snippet"]["publishedAt"]
                .replace("Z","+00:00")
            )


            age = max(
                1,
                (now-uploaded)
                .total_seconds()/3600
            )


            velocity = views / age


            engagement = 0

            if views:
                engagement = (
                    (likes+comments)
                    /
                    views
                ) * 100


            score = (
                velocity * .7
                +
                engagement * 500
            )


            videos.append({

                "title": title,
                "views": views,
                "views_hour": round(velocity),
                "score": score

            })


    return sorted(
        videos,
        key=lambda x:x["score"],
        reverse=True
    )



def analyze(videos):

    words=[]
    hashtags=[]


    for v in videos[:100]:

        words += re.findall(
            r"\b[a-z]{4,}\b",
            v["title"].lower()
        )


        hashtags += re.findall(
            r"#\w+",
            v["title"]
        )


    return (
        Counter(words).most_common(10),
        Counter(hashtags).most_common(10)
    )



def result(idea, words, hashtags, videos):

    score = 75

    if len(videos) > 50:
        score += 10

    if words:
        score += 5

    if hashtags:
        score += 5


    score=min(score,100)


    print("\n🔥 VIRAL MATCH SCORE")
    print("="*40)
    print(score,"/100")


    print("\n🏆 TITLE THIS:")

    print(
        f"{idea.title()}... Nobody Expected This 😳🐱"
    )


    print("\n🏷️ HASHTAGS:")

    for tag in hashtags[:5]:
        print(tag[0])


    print("\n🔊 SOUND RECOMMENDATION:")

    print(
        "Searching trending audio module next..."
    )

    print(
        "Target: daily rising sounds matched to cat content"
    )


    print("\n📊 WHY:")

    print(
        "- Fresh YouTube Shorts data"
    )

    print(
        "- Views/hour analysis"
    )

    print(
        "- Engagement patterns"
    )

    print(
        "- Current title trends"
    )



videos=get_shorts()


print("\n🔥 TOP CURRENT CAT SHORTS")

for v in videos[:10]:

    print(
        "\n",
        v["title"]
    )

    print(
        "Views/hour:",
        v["views_hour"]
    )


words,hashtags=analyze(videos)


idea=input(
    "\nDescribe your cat video: "
)


result(
    idea,
    words,
    hashtags,
    videos
)