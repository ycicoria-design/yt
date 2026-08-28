p="youtube_engine.py"

s=open(p).read()

insert=r'''

# ===== FIRST 3 SECOND HOOK ENGINE =====

def generate_hooks(topic):

    hooks = [
        f"Nobody believed this {topic} was possible...",
        f"I had only seconds left during this {topic}...",
        f"Everyone thought I was going to lose this {topic}...",
        f"This {topic} went completely wrong...",
        f"Wait until you see how this {topic} ends..."
    ]

    results=[]

    for hook in hooks:
        score=50
        text=hook.lower()

        if any(x in text for x in ["nobody","everyone","impossible"]):
            score += 15

        if any(x in text for x in ["wait","seconds","ends"]):
            score += 15

        if "wrong" in text:
            score += 10

        results.append({
            "hook": hook,
            "retention_score": min(score,100)
        })

    return sorted(
        results,
        key=lambda x:x["retention_score"],
        reverse=True
    )

'''

if "def generate_hooks" not in s:
    s += insert
    open(p,"w").write(s)
    print("HOOK ENGINE ADDED")
else:
    print("ALREADY EXISTS")
