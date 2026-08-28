import re
import math
from collections import Counter


def viral_velocity(video):
    views = video.get("views", 0)
    hours = video.get("hours_since_upload", 24)

    if hours <= 0:
        hours = 1

    return round(views / hours)


def engagement_score(video):
    views = video.get("views", 1)
    likes = video.get("likes", 0)
    comments = video.get("comments", 0)

    if views == 0:
        return 0

    like_rate = likes / views
    comment_rate = comments / views

    score = (like_rate * 70) + (comment_rate * 30)

    return min(round(score * 100), 100)


def detect_outliers(videos):

    if not videos:
        return []

    velocities = [
        viral_velocity(v)
        for v in videos
    ]

    average = sum(velocities) / len(velocities)

    winners = []

    for video in videos:
        velocity = viral_velocity(video)

        if velocity > average * 3:
            winners.append(video)

    return winners


def keyword_strength(text):

    words = re.findall(r"[a-zA-Z]+", text.lower())

    strong = [
        "impossible",
        "clutch",
        "secret",
        "nobody",
        "insane",
        "crazy",
        "challenge",
        "world",
        "fastest",
        "best"
    ]

    score = 0

    for word in words:
        if word in strong:
            score += 10

    return min(score, 50)
import re
import math
from collections import Counter


def viral_velocity(video):
    views = video.get("views", 0)
    hours = video.get("hours_since_upload", 24)

    if hours <= 0:
        hours = 1

    return round(views / hours)


def engagement_score(video):
    views = video.get("views", 1)
    likes = video.get("likes", 0)
    comments = video.get("comments", 0)

    if views == 0:
        return 0

    like_rate = likes / views
    comment_rate = comments / views

    score = (like_rate * 70) + (comment_rate * 30)

    return min(round(score * 100), 100)


def detect_outliers(videos):

    if not videos:
        return []

    velocities = [
        viral_velocity(v)
        for v in videos
    ]

    average = sum(velocities) / len(velocities)

    winners = []

    for video in videos:
        velocity = viral_velocity(video)

        if velocity > average * 3:
            winners.append(video)

    return winners


def keyword_strength(text):

    words = re.findall(r"[a-zA-Z]+", text.lower())

    strong = [
        "impossible",
        "clutch",
        "secret",
        "nobody",
        "insane",
        "crazy",
        "challenge",
        "world",
        "fastest",
        "best"
    ]

    score = 0

    for word in words:
        if word in strong:
            score += 10

    return min(score, 50)
def generate_report(idea, videos):
    viral_radar(videos)

    print("\n🔥 VIRAL INTELLIGENCE REPORT")
    print("=" * 40)

    score = predict_viral_score(idea, videos)

    print("\n🔥 VIRAL POTENTIAL SCORE:")
    print(f"{score}/100")

    print("\n🚀 VIRAL VELOCITY CHECK:")

    winners = detect_outliers(videos)

    if winners:
        print(f"Found {len(winners)} breakout videos.")
        print("Studying patterns from fast-growing content.")
    else:
        print("No major breakout patterns detected.")

    print("\n🧠 WINNING PSYCHOLOGY:")
    
    for item in [
        "Curiosity gap",
        "High stakes situation",
        "Fast payoff",
        "Emotional reaction",
        "Viewer retention loop"
    ]:
        print("-", item)


    print("\n🏆 TITLE OPTIONS:")

    for title in generate_titles(idea):
        print("-", title)


    print("\n🎯 FIRST 3 SECOND HOOKS:")

    for hook in generate_hooks(idea):
        print("-", hook)


    print("\n📈 VIDEO STRUCTURE:")

    print(generate_blueprint(idea))


    print("\n📊 COMPETITIVE ADVANTAGE:")

    print("""
Copy the structure of top performing videos:
- opening emotion
- pacing
- payoff timing
- replay value

Do not copy the exact video.
Copy why viewers stayed.
""")


    print("\n✅ Viral Intelligence Engine Complete")

def predict_viral_score(idea, videos):

    score = 40

    score += keyword_strength(idea)

    score += curiosity_score(idea)

    if len(detect_outliers(videos)) > 0:
        score += 10

    return min(score, 100)


def curiosity_score(text):

    triggers = [
        "nobody",
        "wait",
        "secret",
        "hidden",
        "until",
        "last",
        "almost",
        "unexpected",
        "impossible"
    ]

    score = 0
    lower = text.lower()

    for trigger in triggers:
        if trigger in lower:
            score += 8

    return min(score, 40)


def generate_titles(idea):

    templates = [
        f"Nobody Expected This {idea}",
        f"I Tried The Impossible {idea} Challenge",
        f"The Final Seconds Changed Everything...",
        f"They Thought I Couldn't Do This...",
        f"The {idea} Moment Nobody Talks About",
        f"I Had One Chance To Prove Everyone Wrong"
    ]

    return templates


def generate_hooks(idea):

    hooks = [
        f"Wait until you see what happens in this {idea}...",
        "Everyone thought this was impossible...",
        "The last few seconds changed everything...",
        "I almost failed until this happened...",
        f"They laughed at this {idea} until they saw the result...",
        "Nobody expected the ending..."
    ]

    return hooks


def generate_blueprint(idea):

    blueprint = f"""
VIDEO BLUEPRINT:

0-3 SECONDS:
Show the craziest moment immediately.
Create instant curiosity.

3-10 SECONDS:
Build tension.
Make viewers ask: "Can he actually do this?"

MIDDLE:
Remove all downtime.
Keep constant movement and escalation.

ENDING:
Deliver the payoff.
Add a surprise, reaction, or replay loop.

VIDEO IDEA:
{idea}

STRUCTURE:
Hook → Challenge → Tension → Payoff
"""

    return blueprint


from datetime import datetime


def analyze_freshness(videos):

    windows = {
        "last_1_hour": 0,
        "last_6_hours": 0,
        "last_24_hours": 0,
        "last_7_days": 0
    }

    for video in videos:
        age = video.get("age_hours", 999)

        if age <= 1:
            windows["last_1_hour"] += 1
        if age <= 6:
            windows["last_6_hours"] += 1
        if age <= 24:
            windows["last_24_hours"] += 1
        if age <= 168:
            windows["last_7_days"] += 1

    return windows


def hashtag_scores(videos):

    tags = {}

    for video in videos:
        for tag in video.get("hashtags", []):

            if tag not in tags:
                tags[tag] = {
                    "uses": 0,
                    "views": 0,
                    "engagement": 0
                }

            tags[tag]["uses"] += 1
            tags[tag]["views"] += video.get("views", 0)

            tags[tag]["engagement"] += (
                video.get("likes", 0) +
                video.get("comments", 0)
            )

    results = []

    for tag, data in tags.items():

        score = min(
            100,
            int(
                (data["uses"] * 2) +
                (data["engagement"] / 10000) +
                (data["views"] / 100000)
            )
        )

        results.append({
            "hashtag": tag,
            "score": score,
            "uses": data["uses"]
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )[:20]


def viral_radar(videos):

    print("\n⏱ VIRAL FRESHNESS RADAR")
    print("=" * 35)

    fresh = analyze_freshness(videos)

    print("Videos detected:")
    print("- Last hour:", fresh["last_1_hour"])
    print("- Last 6 hours:", fresh["last_6_hours"])
    print("- Last 24 hours:", fresh["last_24_hours"])
    print("- Last 7 days:", fresh["last_7_days"])


    print("\n🔥 HASHTAG VIRAL SCORES")
    print("=" * 35)

    for tag in hashtag_scores(videos)[:10]:
        print(
            f"#{tag['hashtag']} | Score {tag['score']}/100 | Used {tag['uses']} times"
        )


