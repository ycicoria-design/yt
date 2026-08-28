p="youtube_engine.py"

s=open(p).read()

insert=r'''

# ===== VIRAL SCORING ENGINE =====

def viral_score(video):

    title = video.get("title","").lower()

    score = 0

    hooks = [
        "nobody",
        "impossible",
        "secret",
        "unexpected",
        "crazy",
        "insane",
        "last",
        "only",
        "challenge",
        "clutch"
    ]

    for h in hooks:
        if h in title:
            score += 8

    views = video.get("views",0)
    likes = video.get("likes",0)
    comments = video.get("comments",0)

    if views > 500000:
        score += 25
    elif views > 100000:
        score += 15

    if views:
        engagement = ((likes + comments) / views) * 100
        score += min(int(engagement * 5),20)

    score += min(comments // 100,15)

    return min(score,100)


def rank_viral_videos(videos):

    ranked=[]

    for v in videos:
        ranked.append(
            (
                viral_score(v),
                v
            )
        )

    ranked.sort(
        key=lambda x:x[0],
        reverse=True
    )

    return ranked

'''

if "def viral_score" not in s:
    s += insert
    open(p,"w").write(s)
    print("VIRAL SCORING ENGINE ADDED")
else:
    print("ALREADY EXISTS")
