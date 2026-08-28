p="youtube_engine.py"

s=open(p).read()

insert=r'''

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

'''

if "def analyze_competitor" not in s:
    s += insert
    open(p,"w").write(s)
    print("COMPETITOR ENGINE ADDED")
else:
    print("ALREADY EXISTS")
