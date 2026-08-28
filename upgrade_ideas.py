p="youtube_engine.py"

s=open(p).read()

insert=r'''

# ===== VIRAL IDEA GENERATOR =====

def generate_video_ideas(topic):

    return [
        {
            "title": f"They Thought This {topic} Was Impossible...",
            "hook": f"Everyone said this {topic} challenge could not be done.",
            "thumbnail": "shocked reaction + impossible situation",
            "structure": "Hook -> Challenge -> Pressure -> Final payoff"
        },
        {
            "title": f"I Had One Chance To Win This {topic}",
            "hook": "One mistake and everything was over...",
            "thumbnail": "low health + enemy advantage",
            "structure": "Setup -> Rising tension -> Unexpected victory"
        },
        {
            "title": f"The Last Seconds Changed Everything ({topic})",
            "hook": "Wait until you see what happens at the end...",
            "thumbnail": "timer + intense moment",
            "structure": "Mystery -> Escalation -> Replay moment"
        }
    ]

'''

if "def generate_video_ideas" not in s:
    s += insert
    open(p,"w").write(s)
    print("IDEA GENERATOR ADDED")
else:
    print("ALREADY EXISTS")
