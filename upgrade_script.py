p="youtube_engine.py"

s=open(p).read()

insert=r'''

# ===== AI SCRIPT BLUEPRINT GENERATOR =====

def generate_script_blueprint(topic):

    return {
        "hook": f"You won't believe what happened during this {topic}...",
        
        "opening": 
        "Show the most intense moment immediately to create curiosity.",

        "setup":
        f"Explain the challenge and why this {topic} situation matters.",

        "tension":
        "Increase pressure, remove downtime, and make viewers question the outcome.",

        "payoff":
        "Deliver the unexpected result or biggest moment.",

        "ending":
        "Add reaction, replay value, or a reason to watch again."
    }

'''

if "def generate_script_blueprint" not in s:
    s += insert
    open(p,"w").write(s)
    print("SCRIPT GENERATOR ADDED")
else:
    print("ALREADY EXISTS")
