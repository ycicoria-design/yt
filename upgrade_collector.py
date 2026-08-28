p="youtube_engine.py"

s=open(p).read()

insert = r'''

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

'''

if "def offline_trending" not in s:
    s += insert
    open(p,"w").write(s)
    print("OFFLINE VIRAL DATABASE ADDED")
else:
    print("ALREADY ADDED")
