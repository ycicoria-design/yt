import re
from collections import Counter


def viral_velocity(video):
    views = video.get("views", 0)
    hours = (
        video.get("hours_since_upload")
        or video.get("hours_old")
        or video.get("age_hours")
        or 24
    )

    if hours <= 0:
        hours = 1

    return round(views / hours)


def engagement_score(video):
    views = video.get("views", 0)
    likes = video.get("likes", 0)
    comments = video.get("comments", 0)

    if views <= 0:
        return 0

    rate = ((likes + comments * 2) / views) * 100

    return min(round(rate * 10), 100)


def detect_outliers(videos):
    if not videos:
        return []

    velocities = [viral_velocity(v) for v in videos]

    if not velocities:
        return []

    average = sum(velocities) / len(velocities)

    if average <= 0:
        return []

    return [
        video
        for video in videos
        if viral_velocity(video) >= average * 2
    ]


def clean_words(text):
    stop_words = {
        "the", "and", "for", "you", "your", "this", "that",
        "with", "from", "shorts", "short", "video", "videos",
        "how", "what", "why", "when", "are", "was", "were",
        "have", "has", "had", "but", "not", "all", "just",
        "into", "out", "new"
    }

    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return [
        word
        for word in words
        if len(word) > 2 and word not in stop_words
    ]


def get_video_title(video):
    return (
        video.get("title")
        or video.get("name")
        or video.get("snippet", {}).get("title")
        or ""
    )


def extract_keywords_from_videos(videos):
    counter = Counter()

    for video in videos:
        title = get_video_title(video)

        for word in clean_words(title):
            counter[word] += 1

    return counter.most_common(15)


def extract_hashtags(videos):
    counter = Counter()

    for video in videos:
        hashtags = video.get("hashtags", [])

        if isinstance(hashtags, str):
            hashtags = re.findall(r"#([A-Za-z0-9_]+)", hashtags)

        for tag in hashtags:
            tag = str(tag).replace("#", "").strip()

            if tag:
                counter[tag.lower()] += 1

        title = get_video_title(video)

        for tag in re.findall(r"#([A-Za-z0-9_]+)", title):
            counter[tag.lower()] += 1

        description = video.get("description", "")

        for tag in re.findall(r"#([A-Za-z0-9_]+)", description):
            counter[tag.lower()] += 1

    return counter.most_common(20)


def keyword_strength(text):
    strong_words = {
        "secret": 12,
        "nobody": 12,
        "insane": 10,
        "crazy": 9,
        "impossible": 10,
        "best": 7,
        "broken": 10,
        "clutch": 10,
        "challenge": 8,
        "hidden": 10,
        "fastest": 8,
        "unexpected": 10,
        "finally": 7,
        "rare": 8,
        "worst": 7
    }

    score = 0

    for word in clean_words(text):
        score += strong_words.get(word, 0)

    return min(score, 40)


def curiosity_score(text):
    triggers = [
        "nobody",
        "secret",
        "hidden",
        "wait",
        "until",
        "almost",
        "unexpected",
        "impossible",
        "broken",
        "actually",
        "finally"
    ]

    text = text.lower()

    score = sum(7 for trigger in triggers if trigger in text)

    return min(score, 35)


def predict_viral_score(idea, videos):
    score = 35

    score += keyword_strength(idea)
    score += curiosity_score(idea)

    if detect_outliers(videos):
        score += 10

    return min(score, 100)


def generate_titles(idea, videos=None):
    videos = videos or []

    trending_keywords = [
        word for word, count
        in extract_keywords_from_videos(videos)[:5]
    ]

    keyword = trending_keywords[0] if trending_keywords else ""

    base = idea.strip()

    titles = [
        f"{base} But It Gets Worse...",
        f"I Didn't Expect This To Happen in {base}",
        f"This {base} Moment Was Actually Insane",
        f"Nobody Was Ready For This {base}",
        f"I Thought This {base} Trick Was Fake",
        f"The Most Broken {base} Moment I've Seen",
        f"This Changed Everything in {base}",
        f"Wait Until You See What Happens in {base}"
    ]

    if keyword and keyword.lower() not in base.lower():
        titles.insert(
            0,
            f"{keyword.title()} Changed Everything in {base}"
        )

    cleaned = []

    for title in titles:
        title = re.sub(r"\s+", " ", title).strip()

        if title not in cleaned:
            cleaned.append(title)

    return cleaned[:8]


def generate_hooks(idea):
    return [
        f"Wait until you see what happens in this {idea}...",
        f"I thought this {idea} moment was over...",
        "This looked completely normal for the first second...",
        "Nobody expected what happened next...",
        "I almost threw this away until this happened...",
        "Watch the last few seconds closely..."
    ]


def recommend_hashtags(idea, videos):
    discovered = extract_hashtags(videos)

    tags = []

    for tag, count in discovered:
        if tag not in tags:
            tags.append(tag)

    idea_words = clean_words(idea)

    for word in idea_words:
        normalized = word.replace(" ", "")

        if normalized not in tags:
            tags.append(normalized)

    universal = [
        "shorts",
        "youtubeshorts",
        "viralshorts"
    ]

    for tag in universal:
        if tag not in tags:
            tags.append(tag)

    return ["#" + tag for tag in tags[:8]]


def analyze_freshness(videos):
    windows = {
        "last_1_hour": 0,
        "last_6_hours": 0,
        "last_24_hours": 0,
        "last_7_days": 0
    }

    for video in videos:
        age = (
            video.get("hours_old")
            or video.get("hours_since_upload")
            or video.get("age_hours")
            or 999
        )

        if age <= 1:
            windows["last_1_hour"] += 1

        if age <= 6:
            windows["last_6_hours"] += 1

        if age <= 24:
            windows["last_24_hours"] += 1

        if age <= 168:
            windows["last_7_days"] += 1

    return windows


def generate_blueprint(idea):
    return {
        "0-2 seconds": "Show the strongest or most surprising moment immediately.",
        "2-6 seconds": "Create an open loop so the viewer needs to know what happens next.",
        "6-15 seconds": "Escalate quickly. Remove pauses, menus, loading screens, and filler.",
        "15-25 seconds": "Deliver the main payoff or reveal.",
        "ending": "Cut on a strong reaction, surprise, or loopable final moment."
    }


def generate_report(idea, videos):
    score = predict_viral_score(idea, videos)
    titles = generate_titles(idea, videos)
    hooks = generate_hooks(idea)
    hashtags = recommend_hashtags(idea, videos)
    freshness = analyze_freshness(videos)
    keywords = extract_keywords_from_videos(videos)
    outliers = detect_outliers(videos)

    best_title = titles[0] if titles else idea

    return {
        "viral_score": score,
        "best_title": best_title,
        "title_options": titles,
        "hashtags": hashtags,
        "best_hook": hooks[0],
        "hook_options": hooks,
        "keywords": [
            {
                "keyword": word,
                "count": count
            }
            for word, count in keywords
        ],
        "freshness": freshness,
        "breakout_videos_found": len(outliers),
        "blueprint": generate_blueprint(idea),
        "advice": [
            "Lead with the strongest visual immediately.",
            "Do not waste the first second on an intro.",
            "Keep captions large and easy to read.",
            "Cut any moment that does not increase curiosity or payoff.",
            "Use the recommended title and hashtags as a starting point, then adjust them to match the exact clip."
        ]
    }
