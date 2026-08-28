from collections import Counter
import re


def generate_report(idea, videos):

    print("\n🔥 VIRAL STRATEGY REPORT")
    print("=" * 35)

    print("\n🎬 VIDEO IDEA:")
    print(idea)

    # Analyze actual videos
    titles = []
    views = []

    for v in videos:
        title = v.get("title", "")
        titles.append(title.lower())

        try:
            views.append(int(v.get("views", 0)))
        except:
            views.append(0)

    avg_views = sum(views) / max(len(views),1)

    viral_videos = []

    for i,v in enumerate(views):
        if v > avg_views * 3:
            viral_videos.append(titles[i])


    # Score based on data
    score = 50

    if viral_videos:
        score += 25

    if len(idea.split()) >= 3:
        score += 10

    score = min(score,95)


    print("\n🔥 VIRAL SCORE:")
    print(f"{score}/100")


    # Find winning title patterns
    patterns = []

    for word in [
        "impossible",
        "challenge",
        "secret",
        "mistake",
        "nobody",
        "best",
        "world",
        "1v1",
        "1v4",
        "insane"
    ]:
        count = sum(word in t for t in titles)
        if count:
            patterns.append((word,count))


    patterns.sort(key=lambda x:x[1],reverse=True)


    print("\n🧠 WINNING PSYCHOLOGY FOUND:")

    for p,c in patterns[:5]:
        print("-",p,c,"videos")


    print("\n🏆 TITLE STRATEGY:")

    print("""
Use this structure:

[Impossible situation] + [Curiosity] + [Payoff]

Examples:
""")

    print(f"- Nobody Thought This Would Happen In {idea}")
    print(f"- I Tried The Hardest {idea} Challenge")
    print(f"- The Final Seconds Changed Everything In {idea}")


    print("\n🎯 FIRST 3 SECOND HOOK:")

    print(f"""
0-1 sec:
Show the most insane moment from {idea}

1-3 sec:
Create a question viewers need answered

Example:
"They thought this was impossible..."
""")


    print("\n📈 RETENTION PLAN:")

    print("""
0-3 seconds:
Instant payoff preview

3-10 seconds:
Build tension

Middle:
Remove all downtime

Ending:
Give unexpected result or replay loop
""")


    print("\n#️⃣ HASHTAG STRATEGY:")

    words = re.findall(r"[a-zA-Z]+", idea.lower())

    tags = []

    for w in words:
        if len(w)>3:
            tags.append("#"+w)

    tags += [
        "#shorts",
        "#viral",
        "#trending"
    ]

    for t in tags[:8]:
        print(t)


    print("\n💡 VIRAL OPPORTUNITY:")

    if viral_videos:
        print("Found above-average performing videos. Study their structure.")
    else:
        print("No strong outliers found. Test multiple hooks.")


    print("\n✅ Professional analysis complete")
