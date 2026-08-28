import os
import re
from collections import Counter
from datetime import datetime, timezone

from googleapiclient.discovery import build


API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable is missing")


youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def parse_youtube_duration(duration):
    """
    Convert YouTube ISO 8601 duration like:
    PT45S
    PT1M20S
    PT2M5S
    into total seconds.
    """

    hours = 0
    minutes = 0
    seconds = 0

    h = re.search(r"(\d+)H", duration)
    m = re.search(r"(\d+)M", duration)
    s = re.search(r"(\d+)S", duration)

    if h:
        hours = int(h.group(1))

    if m:
        minutes = int(m.group(1))

    if s:
        seconds = int(s.group(1))

    return (hours * 3600) + (minutes * 60) + seconds


def hours_since(published_at):
    try:
        published = datetime.fromisoformat(
            published_at.replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        age = now - published

        return max(age.total_seconds() / 3600, 0.01)

    except Exception:
        return 999999


def extract_hashtags(title, description):
    text = f"{title} {description}"

    tags = re.findall(
        r"#([A-Za-z0-9_]+)",
        text
    )

    return list(dict.fromkeys(tags))


# --------------------------------------------------
# COLLECT REAL YOUTUBE DATA
# --------------------------------------------------

def get_shorts(topic):

    collected = {}

    searches = [
        topic,
        f"{topic} shorts",
        f"{topic} #shorts",
        f"{topic} viral"
    ]

    for search in searches:

        try:

            result = youtube.search().list(
                part="snippet",
                q=search,
                type="video",
                videoDuration="short",
                order="relevance",
                maxResults=25
            ).execute()

        except Exception as e:

            print("YouTube search error:", e)
            continue


        ids = [
            item["id"]["videoId"]
            for item in result.get("items", [])
            if item.get("id", {}).get("videoId")
        ]


        if not ids:
            continue


        try:

            details = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(ids)
            ).execute()

        except Exception as e:

            print("YouTube video detail error:", e)
            continue


        for video in details.get("items", []):

            video_id = video.get("id")

            # Avoid duplicates from multiple searches
            if video_id in collected:
                continue


            stats = video.get("statistics", {})
            snippet = video.get("snippet", {})
            content = video.get("contentDetails", {})


            duration_text = content.get("duration", "")

            duration_seconds = parse_youtube_duration(
                duration_text
            )


            # YouTube API "short" means under 4 minutes.
            # Filter more aggressively for Shorts.
            if duration_seconds <= 0:
                continue

            if duration_seconds > 180:
                continue


            title = snippet.get("title", "")
            description = snippet.get("description", "")

            views = int(
                stats.get("viewCount", 0)
            )

            likes = int(
                stats.get("likeCount", 0)
            )

            comments = int(
                stats.get("commentCount", 0)
            )

            published = snippet.get(
                "publishedAt",
                ""
            )

            age_hours = hours_since(
                published
            )


            # Average views per hour since publication.
            # This is NOT YouTube giving us historical velocity.
            # It is our own calculated average.
            views_per_hour = round(
                views / age_hours,
                2
            )


            # Public engagement estimate
            if views > 0:

                engagement = (
                    (likes + comments) / views
                ) * 100

            else:

                engagement = 0


            hashtags = extract_hashtags(
                title,
                description
            )


            collected[video_id] = {

                "video_id": video_id,

                "url":
                    f"https://www.youtube.com/watch?v={video_id}",

                "title": title,

                "description": description,

                "channel":
                    snippet.get("channelTitle", ""),

                "views": views,

                "likes": likes,

                "comments": comments,

                "published": published,

                "hours_old":
                    round(age_hours, 2),

                "views_hour":
                    views_per_hour,

                "engagement":
                    round(engagement, 2),

                "hashtags":
                    hashtags,

                "tags":
                    snippet.get("tags", []),

                "duration_seconds":
                    duration_seconds
            }


    videos = list(
        collected.values()
    )


    # Highest calculated velocity first
    videos.sort(
        key=lambda x: x.get(
            "views_hour",
            0
        ),
        reverse=True
    )


    return videos


# --------------------------------------------------
# VIRAL VELOCITY
# --------------------------------------------------

def viral_velocity(videos):

    ranked = sorted(
        videos,
        key=lambda x: x.get(
            "views_hour",
            0
        ),
        reverse=True
    )

    return ranked[:10]


# --------------------------------------------------
# KEYWORDS
# --------------------------------------------------

def analyze_keywords(videos):

    words = []

    ignore = {
        "this",
        "that",
        "with",
        "from",
        "your",
        "shorts",
        "video",
        "youtube",
        "have",
        "what",
        "when",
        "they",
        "will",
        "just",
        "about"
    }


    for video in videos:

        title = video.get(
            "title",
            ""
        ).lower()


        found = re.findall(
            r"\b[a-z0-9]{4,}\b",
            title
        )


        for word in found:

            if word not in ignore:

                words.append(
                    word
                )


    return Counter(
        words
    ).most_common(20)


# --------------------------------------------------
# HASHTAGS
# --------------------------------------------------

def analyze_hashtags(videos):

    scores = {}


    for video in videos:

        hours = video.get(
            "hours_old",
            999
        )

        velocity = video.get(
            "views_hour",
            0
        )

        engagement = video.get(
            "engagement",
            0
        )


        for tag in video.get(
            "hashtags",
            []
        ):

            tag = tag.lower()


            if tag not in scores:

                scores[tag] = {

                    "uses": 0,

                    "recent": 0,

                    "velocity": 0,

                    "engagement_total": 0
                }


            scores[tag]["uses"] += 1


            if hours <= 24:

                scores[tag]["recent"] += 1


            scores[tag]["velocity"] += velocity

            scores[tag]["engagement_total"] += engagement


    results = []


    for tag, data in scores.items():

        uses = data["uses"]

        avg_velocity = (
            data["velocity"] / uses
            if uses
            else 0
        )

        avg_engagement = (
            data["engagement_total"] / uses
            if uses
            else 0
        )


        score = (

            min(
                uses * 4,
                25
            )

            +

            min(
                data["recent"] * 5,
                25
            )

            +

            min(
                avg_velocity / 5000,
                30
            )

            +

            min(
                avg_engagement * 2,
                20
            )
        )


        score = round(
            min(
                score,
                100
            )
        )


        if score >= 80:

            status = "EXPLODING"

        elif score >= 60:

            status = "RISING"

        elif score >= 35:

            status = "ACTIVE"

        else:

            status = "LOW SIGNAL"


        results.append(
            (
                tag,
                score,
                status,
                {
                    "uses":
                        uses,

                    "recent":
                        data["recent"],

                    "avg_views_hour":
                        round(
                            avg_velocity,
                            2
                        ),

                    "avg_engagement":
                        round(
                            avg_engagement,
                            2
                        )
                }
            )
        )


    results.sort(
        key=lambda x: x[1],
        reverse=True
    )


    return results[:15]


# --------------------------------------------------
# VIRAL SCORE
# --------------------------------------------------

def viral_score(video):

    views = video.get(
        "views",
        0
    )

    velocity = video.get(
        "views_hour",
        0
    )

    engagement = video.get(
        "engagement",
        0
    )

    hours = video.get(
        "hours_old",
        999
    )


    score = 0


    if velocity >= 100000:

        score += 40

    elif velocity >= 25000:

        score += 30

    elif velocity >= 5000:

        score += 20

    elif velocity >= 1000:

        score += 10


    if engagement >= 10:

        score += 30

    elif engagement >= 6:

        score += 20

    elif engagement >= 3:

        score += 10


    if hours <= 6:

        score += 20

    elif hours <= 24:

        score += 15

    elif hours <= 72:

        score += 10


    if views >= 1000000:

        score += 10

    elif views >= 100000:

        score += 5


    return min(
        score,
        100
    )


def rank_viral_videos(videos):

    ranked = []


    for video in videos:

        ranked.append(
            (
                viral_score(video),
                video
            )
        )


    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )


    return ranked
