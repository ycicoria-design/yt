p="youtube_engine.py"

s=open(p).read()

insert=r'''

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

'''

if "def test_titles" not in s:
    s += insert
    open(p,"w").write(s)
    print("TITLE A/B ENGINE ADDED")
else:
    print("ALREADY EXISTS")
