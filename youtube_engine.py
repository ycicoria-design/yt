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

        try:
            result = youtube.search().list(
                part="snippet",
                q=search,
                type="video",
                videoDuration="short",
                order="date",
                maxResults=10
            ).execute()

        except Exception:
            print("YouTube API unavailable - using offline mode")
            continue


        ids = [
            x["id"]["videoId"]
            for x in result.get("items", [])
        ]


        if not ids:
            continue


        try:
            details = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(ids)
            ).execute()

        except Exception:
            continue


        for video in details.get("items", []):

            stats = video.get("statistics", {})
            snippet = video.get("snippet", {})

            videos.append({
                "title": snippet.get("title",""),
                "views": int(stats.get("viewCount",0)),
                "likes": int(stats.get("likeCount",0)),
                "comments": int(stats.get("commentCount",0)),
                "published": snippet.get("publishedAt",""),
                "tags": snippet.get("tags",[])
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

    scores = {}

    for v in videos:
        hours = v.get("hours_old",999)
        velocity = v.get("views_hour",0)
        engagement = v.get("engagement",0)

        for tag in v.get("hashtags",[]):

            if tag not in scores:
                scores[tag] = {
                    "uses":0,
                    "recent":0,
                    "velocity":0,
                    "engagement":0
                }

            scores[tag]["uses"] += 1

            if hours <= 24:
                scores[tag]["recent"] += 1

            scores[tag]["velocity"] += velocity
            scores[tag]["engagement"] += engagement


    results=[]

    for tag,data in scores.items():

        score = (
            min(data["uses"]*2,20)
            + min(data["recent"]*5,25)
            + min(data["velocity"]/10000,35)
            + min(data["engagement"]*20,20)
        )

        score=round(min(score,100))

        if score >= 85:
            status="🔥 EXPLODING"
        elif score >= 65:
            status="🚀 RISING"
        elif score >= 40:
            status="🟡 STABLE"
        else:
            status="❄️ DYING"

        results.append((tag,score,status,data))

    results.sort(key=lambda x:x[1],reverse=True)

    return results[:15]




# ===== VIRAL FALLBACK COLLECTOR =====

def offline_trending(topic):

    samples = [
        {
            "title": f"{topic} insane clutch moment",
            "views": 250000,
            "likes": 18000,
            "comments": 900,
            "published": "today",
            "tags": [topic,"viral","shorts","gaming"]
        },
        {
            "title": f"Nobody expected this {topic} comeback",
            "views": 800000,
            "likes": 52000,
            "comments": 2400,
            "published": "today",
            "tags": [topic,"challenge","reaction"]
        },
        {
            "title": f"I tried the impossible {topic}",
            "views": 430000,
            "likes": 31000,
            "comments": 1200,
            "published": "yesterday",
            "tags": [topic,"pro","gameplay"]
        }
    ]

    return samples



# ===== VIRAL SCORING ENGINE =====

def viral_score(video):

    title = video.get("title","").lower()

    score = 0

    hooks = [
        "nobody",
        "impossible",
        "secret",
        "unexpected",
        "crazy",
        "insane",
        "last",
        "only",
        "challenge",
        "clutch"
    ]

    for h in hooks:
        if h in title:
            score += 8

    views = video.get("views",0)
    likes = video.get("likes",0)
    comments = video.get("comments",0)

    if views > 500000:
        score += 25
    elif views > 100000:
        score += 15

    if views:
        engagement = ((likes + comments) / views) * 100
        score += min(int(engagement * 5),20)

    score += min(comments // 100,15)

    return min(score,100)


def rank_viral_videos(videos):

    ranked=[]

    for v in videos:
        ranked.append(
            (
                viral_score(v),
                v
            )
        )

    ranked.sort(
        key=lambda x:x[0],
        reverse=True
    )

    return ranked



# ===== VIRAL IDEA GENERATOR =====

def generate_video_ideas(topic):

    return [
        {
            "title": f"They Thought This {topic} Was Impossible...",
            "hook": f"Everyone said this {topic} challenge could not be done.",
            "thumbnail": "shocked reaction + impossible situation",
            "structure": "Hook -> Challenge -> Pressure -> Final payoff"
        },
        {
            "title": f"I Had One Chance To Win This {topic}",
            "hook": "One mistake and everything was over...",
            "thumbnail": "low health + enemy advantage",
            "structure": "Setup -> Rising tension -> Unexpected victory"
        },
        {
            "title": f"The Last Seconds Changed Everything ({topic})",
            "hook": "Wait until you see what happens at the end...",
            "thumbnail": "timer + intense moment",
            "structure": "Mystery -> Escalation -> Replay moment"
        }
    ]



# ===== RETENTION ANALYZER =====

def analyze_retention(video_description):

    score = 50
    advice = []

    text = video_description.lower()

    if "wait" in text or "until" in text:
        score += 10
        advice.append("Strong curiosity hook")

    if "impossible" in text or "challenge" in text:
        score += 10
        advice.append("High stakes element")

    if "end" in text or "final" in text:
        score += 10
        advice.append("Creates completion pressure")

    if "reaction" in text or "surprise" in text:
        score += 5
        advice.append("Emotional payoff")

    if len(text) < 30:
        advice.append("Add more context and tension")

    return {
        "retention_score": min(score,100),
        "recommendations": advice
    }



# ===== THUMBNAIL INTELLIGENCE =====

def analyze_thumbnail(title):

    score = 50
    advice = []

    text = title.lower()

    if "!" in title:
        score += 5
        advice.append("Strong emotional emphasis")

    if "impossible" in text or "nobody" in text or "secret" in text:
        score += 15
        advice.append("High curiosity trigger")

    if "vs" in text or "challenge" in text:
        score += 10
        advice.append("Creates competition tension")

    if len(title.split()) < 4:
        advice.append("Add more context")

    if len(title.split()) > 12:
        score -= 5
        advice.append("Reduce text complexity")

    return {
        "thumbnail_score": min(max(score,0),100),
        "recommendations": advice
    }



# ===== COMPETITOR BREAKDOWN ENGINE =====

def analyze_competitor(videos):

    results = {
        "winning_patterns": [],
        "common_hooks": [],
        "recommendations": []
    }

    for video in videos:

        title = video.get("title","").lower()

        if "challenge" in title:
            results["common_hooks"].append("Challenge format")

        if "impossible" in title or "nobody" in title:
            results["common_hooks"].append("Curiosity gap")

        if "secret" in title or "hidden" in title:
            results["common_hooks"].append("Mystery hook")

    if results["common_hooks"]:
        results["winning_patterns"].append(
            "Strong emotional titles with unanswered questions"
        )

    results["recommendations"].append(
        "Study pacing, hook timing, and payoff structure"
    )

    return results



# ===== AI SCRIPT BLUEPRINT GENERATOR =====

def generate_script_blueprint(topic):

    return {
        "hook": f"You won't believe what happened during this {topic}...",
        
        "opening": 
        "Show the most intense moment immediately to create curiosity.",

        "setup":
        f"Explain the challenge and why this {topic} situation matters.",

        "tension":
        "Increase pressure, remove downtime, and make viewers question the outcome.",

        "payoff":
        "Deliver the unexpected result or biggest moment.",

        "ending":
        "Add reaction, replay value, or a reason to watch again."
    }



# ===== MULTI PLATFORM ADAPTER =====

def adapt_for_platform(topic, platform):

    if platform.lower() == "tiktok":
        return {
            "style": "Fast hook, trend pacing, instant payoff",
            "hook": f"POV: This {topic} went completely wrong...",
            "ending": "Loop ending for replay"
        }

    elif platform.lower() == "instagram":
        return {
            "style": "Visual storytelling and emotional moments",
            "hook": f"You need to see this {topic} moment...",
            "ending": "Reaction or cinematic replay"
        }

    else:
        return {
            "style": "YouTube Shorts retention structure",
            "hook": f"Nobody expected this {topic}...",
            "ending": "Big payoff + replay value"
        }



# ===== VIRAL TREND PREDICTION ENGINE =====

def predict_trend(topic, videos):

    score = 50
    reasons = []

    text = topic.lower()

    if any(x in text for x in ["challenge","clutch","secret","impossible","1v4"]):
        score += 15
        reasons.append("High curiosity format")

    if videos:
        avg_views = sum(v.get("views",0) for v in videos) / len(videos)

        if avg_views > 500000:
            score += 20
            reasons.append("Strong audience demand")

        elif avg_views > 100000:
            score += 10
            reasons.append("Growing interest")

    if any(x in text for x in ["new","update","season","event"]):
        score += 10
        reasons.append("Fresh topic advantage")

    return {
        "trend_score": min(score,100),
        "signals": reasons
    }



# ===== AI TITLE A/B TEST ENGINE =====

def test_titles(topic):

    titles = [
        f"Nobody Expected This {topic} To Happen",
        f"I Tried The Impossible {topic} Challenge",
        f"The Last Seconds Changed Everything ({topic})",
        f"They Thought I Couldn't Do This {topic}",
        f"This {topic} Moment Shocked Everyone"
    ]

    results=[]

    for title in titles:
        score=50
        text=title.lower()

        if any(x in text for x in ["nobody","impossible","secret","shocked"]):
            score += 15

        if any(x in text for x in ["challenge","tried","couldn't"]):
            score += 10

        if "!" in title:
            score += 5

        results.append({
            "title": title,
            "ctr_score": min(score,100)
        })

    return sorted(
        results,
        key=lambda x:x["ctr_score"],
        reverse=True
    )



# ===== FIRST 3 SECOND HOOK ENGINE =====

def generate_hooks(topic):

    hooks = [
        f"Nobody believed this {topic} was possible...",
        f"I had only seconds left during this {topic}...",
        f"Everyone thought I was going to lose this {topic}...",
        f"This {topic} went completely wrong...",
        f"Wait until you see how this {topic} ends..."
    ]

    results=[]

    for hook in hooks:
        score=50
        text=hook.lower()

        if any(x in text for x in ["nobody","everyone","impossible"]):
            score += 15

        if any(x in text for x in ["wait","seconds","ends"]):
            score += 15

        if "wrong" in text:
            score += 10

        results.append({
            "hook": hook,
            "retention_score": min(score,100)
        })

    return sorted(
        results,
        key=lambda x:x["retention_score"],
        reverse=True
    )



# ===== MASTER VIRAL ANALYZER =====

def master_viral_analysis(topic):

    report = {}

    report["topic"] = topic

    try:
        report["titles"] = test_titles(topic)[:3]
    except:
        report["titles"] = []

    try:
        report["hooks"] = generate_hooks(topic)[:3]
    except:
        report["hooks"] = []

    try:
        report["ideas"] = generate_video_ideas(topic)
    except:
        report["ideas"] = []

    try:
        report["trend"] = predict_trend(topic, [])
    except:
        report["trend"] = {}

    try:
        report["script"] = generate_script_blueprint(topic)
    except:
        report["script"] = {}

    return report

