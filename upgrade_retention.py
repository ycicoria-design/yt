p="youtube_engine.py"

s=open(p).read()

insert=r'''

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

'''

if "def analyze_retention" not in s:
    s += insert
    open(p,"w").write(s)
    print("RETENTION ANALYZER ADDED")
else:
    print("ALREADY EXISTS")
