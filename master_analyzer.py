from youtube_engine import get_shorts, analyze_keywords, analyze_hashtags, viral_velocity


def clean_tag(tag):
    tag = str(tag).strip().replace("#", "").replace(" ", "")
    return tag


def master_viral_analysis(topic):
    videos = get_shorts(topic)

    if not videos:
        return {
            "success": False,
            "topic": topic,
            "message": "No recent YouTube Shorts were found for this topic."
        }

    # ----------------------------
    # KEYWORDS
    # ----------------------------

    keywords = []

    try:
        keyword_results = analyze_keywords(videos)

        for word, count in keyword_results[:10]:
            keywords.append({
                "keyword": word,
                "count": count
            })

    except Exception as e:
        print("KEYWORD ERROR:", e)


    # ----------------------------
    # HASHTAGS
    # ----------------------------

    hashtags = []

    try:
        hashtag_results = analyze_hashtags(videos)

        for item in hashtag_results:

            if len(item) >= 4:
                tag, score, status, data = item

                tag = clean_tag(tag)

                if tag:
                    hashtags.append("#" + tag)

            elif len(item) >= 2:
                tag, count = item

                tag = clean_tag(tag)

                if tag:
                    hashtags.append("#" + tag)

    except Exception as e:
        print("HASHTAG ERROR:", e)


    # If YouTube data has no hashtags,
    # generate useful ones from the actual topic/keywords.

    topic_tag = clean_tag(topic)

    if topic_tag:
        hashtags.insert(0, "#" + topic_tag)

    for item in keywords[:5]:

        word = clean_tag(item["keyword"])

        if len(word) >= 3:
            candidate = "#" + word

            if candidate.lower() not in [x.lower() for x in hashtags]:
                hashtags.append(candidate)


    universal_tags = [
        "#Shorts",
        "#YouTubeShorts"
    ]

    for tag in universal_tags:
        if tag.lower() not in [x.lower() for x in hashtags]:
            hashtags.append(tag)


    hashtags = hashtags[:8]


    # ----------------------------
    # TITLE IDEAS
    # ----------------------------

    main_keyword = topic

    if keywords:
        candidate = keywords[0]["keyword"]

        if len(candidate) >= 3:
            main_keyword = candidate


    titles = [
        f"This {topic} Moment Is Actually Insane",
        f"I Didn't Expect This From {topic}...",
        f"Everyone Is Talking About This {topic} Moment",
        f"This Changed Everything For {topic}",
        f"You Need To See This {topic} Clip"
    ]


    # ----------------------------
    # BEST TITLE
    # ----------------------------

    best_title = titles[0]


    # ----------------------------
    # HOOK IDEAS
    # ----------------------------

    hooks = [
        "Wait until you see what happens...",
        "I seriously wasn't expecting this.",
        "Watch this before you scroll.",
        "This is why everyone is talking about it.",
        "The ending completely changes everything."
    ]


    # ----------------------------
    # FRESHNESS
    # ----------------------------

    freshness = {
        "last_hour": 0,
        "last_6_hours": 0,
        "last_24_hours": 0,
        "last_7_days": 0
    }

    for video in videos:

        age = video.get("hours_old", 999999)

        if age <= 1:
            freshness["last_hour"] += 1

        if age <= 6:
            freshness["last_6_hours"] += 1

        if age <= 24:
            freshness["last_24_hours"] += 1

        if age <= 168:
            freshness["last_7_days"] += 1


    # ----------------------------
    # VIRAL VELOCITY
    # ----------------------------

    try:
        velocity = viral_velocity(videos)

    except Exception as e:
        print("VELOCITY ERROR:", e)
        velocity = None


    return {

        "success": True,

        "topic": topic,

        "videos_analyzed": len(videos),

        "best_title": best_title,

        "titles": titles,

        "hashtags": hashtags,

        "hooks": hooks,

        "keywords": keywords,

        "freshness": freshness,

        "viral_velocity": velocity
    }
