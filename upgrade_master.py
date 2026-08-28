p="youtube_engine.py"

s=open(p).read()

insert=r'''

# ===== MASTER VIRAL ANALYZER =====

def master_viral_analysis(topic):

    report = {}

    report["topic"] = topic

    try:
        report["titles"] = test_titles(topic)[:3]
    except:
        report["titles"] = []

    try:
        report["hooks"] = generate_hooks(topic)[:3]
    except:
        report["hooks"] = []

    try:
        report["ideas"] = generate_video_ideas(topic)
    except:
        report["ideas"] = []

    try:
        report["trend"] = predict_trend(topic, [])
    except:
        report["trend"] = {}

    try:
        report["script"] = generate_script_blueprint(topic)
    except:
        report["script"] = {}

    return report

'''

if "def master_viral_analysis" not in s:
    s += insert
    open(p,"w").write(s)
    print("MASTER ANALYZER ADDED")
else:
    print("ALREADY EXISTS")
