p="youtube_engine.py"

s=open(p).read()

insert=r'''

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

'''

if "def predict_trend" not in s:
    s += insert
    open(p,"w").write(s)
    print("TREND PREDICTION ENGINE ADDED")
else:
    print("ALREADY EXISTS")
