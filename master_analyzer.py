from youtube_engine import (
    get_shorts,
    analyze_keywords,
    analyze_hashtags,
    viral_velocity,
    rank_viral_videos
)


def clean_tag(tag):
    tag = str(tag).strip().replace("#", "").replace(" ", "")
    return tag


def format_number(num):
    try:
        num = int(num)
    except:
        return "0"

    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"

    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"

    if num >= 1_000:
        return f"{num / 1_000:.1f}K"

    return str(num)


def master_viral_analysis(topic):

    videos = get_shorts(topic)

    if not videos:
        return {
            "success": False,
            "topic": topic,
            "message": "No YouTube videos were returned for this topic."
        }

    # -------------------------------------------------
    # TRENDING KEYWORDS
    # -------------------------------------------------

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


    # -------------------------------------------------
    # HASHTAGS FROM REAL VIDEOS
    # -------------------------------------------------

    hashtag_details = []
    hashtags = []

    try:

        hashtag_results = analyze_hashtags(videos)

        for item in hashtag_results:

            if len(item) >= 4:

                tag, score, status, data = item

                cleaned = clean_tag(tag)

                if cleaned:

                    hashtag = "#" + cleaned

                    hashtag_details.append({
                        "tag": hashtag,
                        "score": score,
                        "status": status,
                        "uses": data.get("uses", 0),
                        "avg_views_hour": data.get("avg_views_hour", 0),
                        "avg_engagement": data.get("avg_engagement", 0)
                    })

                    hashtags.append(hashtag)

    except Exception as e:
        print("HASHTAG ERROR:", e)


    # Add topic hashtag if missing
    topic_tag = "#" + clean_tag(topic)

    if topic_tag.lower() not in [x.lower() for x in hashtags]:
        hashtags.insert(0, topic_tag)


    # Use popular keywords only if real hashtags are limited
    if len(hashtags) < 5:

        for item in keywords:

            word = clean_tag(item["keyword"])

            if len(word) >= 3:

                tag = "#" + word

                if tag.lower() not in [x.lower() for x in hashtags]:
                    hashtags.append(tag)

            if len(hashtags) >= 6:
                break


    if "#Shorts".lower() not in [x.lower() for x in hashtags]:
        hashtags.append("#Shorts")


    hashtags = hashtags[:8]


    # -------------------------------------------------
    # REAL VIRAL RANKING
    # -------------------------------------------------

    try:
        ranked = rank_viral_videos(videos)

    except Exception as e:
        print("RANK ERROR:", e)
        ranked = []


    top_videos = []

    for score, video in ranked[:10]:

        top_videos.append({

            "viral_score": score,

            "title": video.get("title", ""),

            "channel": video.get("channel", ""),

            "views": video.get("views", 0),

            "views_display": format_number(
                video.get("views", 0)
            ),

            "likes": video.get("likes", 0),

            "likes_display": format_number(
                video.get("likes", 0)
            ),

            "comments": video.get("comments", 0),

            "comments_display": format_number(
                video.get("comments", 0)
            ),

            "hours_old": video.get("hours_old", 0),

            "views_hour": video.get("views_hour", 0),

            "views_hour_display": format_number(
                video.get("views_hour", 0)
            ),

            "engagement": video.get("engagement", 0),

            "url": video.get("url", "")

        })


    # -------------------------------------------------
    # TOP VIDEO
    # -------------------------------------------------

    if top_videos:

        top_video = top_videos[0]

    else:

        first = videos[0]

        top_video = {

            "title": first.get("title", ""),

            "channel": first.get("channel", ""),

            "views": first.get("views", 0),

            "views_display": format_number(
                first.get("views", 0)
            ),

            "likes_display": format_number(
                first.get("likes", 0)
            ),

            "comments_display": format_number(
                first.get("comments", 0)
            ),

            "hours_old": first.get("hours_old", 0),

            "views_hour": first.get("views_hour", 0),

            "views_hour_display": format_number(
                first.get("views_hour", 0)
            ),

            "engagement": first.get("engagement", 0),

            "viral_score": 0,

            "url": first.get("url", "")
        }


    # -------------------------------------------------
    # LIVE STATISTICS
    # -------------------------------------------------

    total_views = sum(
        video.get("views", 0)
        for video in videos
    )


    average_views = (
        total_views / len(videos)
        if videos
        else 0
    )


    average_likes = (
        sum(
            video.get("likes", 0)
            for video in videos
        ) / len(videos)
        if videos
        else 0
    )


    average_engagement = (
        sum(
            video.get("engagement", 0)
            for video in videos
        ) / len(videos)
        if videos
        else 0
    )


    average_views_hour = (
        sum(
            video.get("views_hour", 0)
            for video in videos
        ) / len(videos)
        if videos
        else 0
    )


    # -------------------------------------------------
    # FRESHNESS
    # -------------------------------------------------

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


    # -------------------------------------------------
    # BUILD TITLES FROM REAL WINNING TITLES
    # -------------------------------------------------

    winning_titles = [
        video["title"]
        for video in top_videos[:5]
        if video.get("title")
    ]


    if winning_titles:

        best_title = winning_titles[0]

        title_ideas = winning_titles[:5]

    else:

        best_title = f"This {topic} Moment Is Actually Insane"

        title_ideas = [
            f"This {topic} Moment Is Actually Insane",
            f"I Didn't Expect This From {topic}...",
            f"Everyone Is Talking About This {topic}",
            f"This Changed Everything For {topic}",
            f"You Need To See This {topic} Clip"
        ]


    # -------------------------------------------------
    # HOOKS BASED ON TOP TITLE PATTERNS
    # -------------------------------------------------

    hooks = []

    for title in winning_titles[:5]:

        lower = title.lower()

        if "how" in lower:
            hooks.append(
                "Start by immediately showing the result, then explain how it happened."
            )

        elif "why" in lower:
            hooks.append(
                "Open with the surprising result first, then reveal why it happened."
            )

        elif "vs" in lower:
            hooks.append(
                "Show both sides immediately and establish the competition in the first second."
            )

        elif "secret" in lower:
            hooks.append(
                "Tease the hidden trick immediately without revealing it until the payoff."
            )

        else:
            hooks.append(
                "Show the strongest moment immediately, then build context around it."
            )


    if not hooks:

        hooks = [
            "Show the best moment in the first second.",
            "Create curiosity before explaining what happened.",
            "Keep the setup short and move quickly to the payoff."
        ]


    hooks = list(dict.fromkeys(hooks))[:5]


    # -------------------------------------------------
    # VIRAL VELOCITY
    # -------------------------------------------------

    try:
        velocity = viral_velocity(videos)

    except Exception as e:
        print("VELOCITY ERROR:", e)
        velocity = []


    # -------------------------------------------------
    # FINAL REPORT
    # -------------------------------------------------

    return {

        "success": True,

        "topic": topic,

        "videos_analyzed": len(videos),

        "total_views": int(total_views),

        "total_views_display": format_number(total_views),

        "average_views": int(average_views),

        "average_views_display": format_number(average_views),

        "average_likes": int(average_likes),

        "average_likes_display": format_number(average_likes),

        "average_engagement": round(
            average_engagement,
            2
        ),

        "average_views_hour": round(
            average_views_hour,
            2
        ),

        "average_views_hour_display": format_number(
            average_views_hour
        ),

        "top_video": top_video,

        "top_videos": top_videos,

        "best_title": best_title,

        "titles": title_ideas,

        "hashtags": hashtags,

        "hashtag_details": hashtag_details,

        "hooks": hooks,

        "keywords": keywords,

        "freshness": freshness,

        "viral_velocity": velocity
    }
