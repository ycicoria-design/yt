p="youtube_engine.py"

s=open(p).read()

insert=r'''

# ===== MULTI PLATFORM ADAPTER =====

def adapt_for_platform(topic, platform):

    if platform.lower() == "tiktok":
        return {
            "style": "Fast hook, trend pacing, instant payoff",
            "hook": f"POV: This {topic} went completely wrong...",
            "ending": "Loop ending for replay"
        }

    elif platform.lower() == "instagram":
        return {
            "style": "Visual storytelling and emotional moments",
            "hook": f"You need to see this {topic} moment...",
            "ending": "Reaction or cinematic replay"
        }

    else:
        return {
            "style": "YouTube Shorts retention structure",
            "hook": f"Nobody expected this {topic}...",
            "ending": "Big payoff + replay value"
        }

'''

if "def adapt_for_platform" not in s:
    s += insert
    open(p,"w").write(s)
    print("MULTI PLATFORM ADAPTER ADDED")
else:
    print("ALREADY EXISTS")
