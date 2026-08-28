from googleapiclient.discovery import build
from collections import Counter
from datetime import datetime, timezone
import re


API_KEY = "AIzaSyAapo6UuuTFPH49ICzFkHBxkrKNmC1Uzfo"


youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


def get_shorts(topic):

    videos = []

    searches = [
        topic,
        topic + " shorts",
        topic + " viral",
        topic + " gameplay"
    ]


    for search in searches:

        result = youtube.search().list(
            part="snippet",
            q=search,
            type="video",
            videoDuration="short",
            order="date",
            maxResults=50
        ).execute()


        ids = [
            x["id"]["videoId"]
            for x in result.get("items", [])
        ]


        if not ids:
            continue


        details = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(ids)
        ).execute()



        for video in details.get("items", []):

            stats = video.get(
                "statistics",
                {}
            )


            snippet = video["snippet"]


            title = snippet["title"]


            views = int(
                stats.get("viewCount",0)
            )

            likes = int(
                stats.get("likeCount",0)
            )

            comments = int(
                stats.get("commentCount",0)
            )


            published = snippet["publishedAt"]

            upload_time = datetime.fromisoformat(
                published.replace("Z","+00:00")
            )


            hours_old = max(
                (datetime.now(timezone.utc)-upload_time).total_seconds()/3600,
                1
            )


            views_per_hour = round(
                views / hours_old,
                2
            )


            engagement = 0

            if views > 0:
                engagement = round(
                    ((likes + comments) / views) * 100,
                    2
                )


            hashtags = re.findall(
                r"#\w+",
                title.lower()
            )


            videos.append({

                "title": title,

                "views": views,

                "likes": likes,

                "comments": comments,

                "hours_old": round(hours_old,1),

                "views_hour": views_per_hour,

                "engagement": engagement,

                "hashtags": hashtags

            })


    return videos



def viral_velocity(videos):

    ranked = sorted(
        videos,
        key=lambda x:x["views_hour"],
        reverse=True
    )

    return ranked[:10]



def analyze_keywords(videos):

    words=[]

    for v in videos:

        words += re.findall(
            r"\b[a-z]{4,}\b",
            v["title"].lower()
        )


    return Counter(words).most_common(20)



def analyze_hashtags(videos):

    tags=[]

    for v in videos:

        tags += v["hashtags"]


    return Counter(tags).most_common(15)
