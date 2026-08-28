p="youtube_engine.py"

s=open(p).read()

insert=r'''

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

'''

if "def analyze_thumbnail" not in s:
    s += insert
    open(p,"w").write(s)
    print("THUMBNAIL INTELLIGENCE ADDED")
else:
    print("ALREADY EXISTS")
