
from flask import Flask, render_template, request
import traceback

app = Flask(__name__)

# Import your original engine
try:
    from master_analyzer import master_viral_analysis
except Exception:
    try:
        from viral_ai import master_viral_analysis
    except Exception:
        master_viral_analysis = None

@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    error = None

    if request.method == "POST":
        topic = request.form.get("topic", "")
        try:
            if master_viral_analysis:
                report = master_viral_analysis(topic)
            else:
                error = "Engine import failed"
        except Exception as e:
            error = str(e)

    return render_template("index.html", report=report, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
