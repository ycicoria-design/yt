from flask import Flask, render_template, request
import traceback

app = Flask(__name__)

# Import AI engine
master_viral_analysis = None
engine_error = None

try:
    from master_analyzer import master_viral_analysis
    print("Loaded master_analyzer successfully")

except Exception as e:
    print("MASTER ANALYZER ERROR:")
    traceback.print_exc()
    engine_error = str(e)

    try:
        from viral_ai import master_viral_analysis
        print("Loaded viral_ai successfully")

    except Exception as e2:
        print("VIRAL AI ERROR:")
        traceback.print_exc()
        engine_error = str(e2)


@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    error = None

    if request.method == "POST":
        topic = request.form.get("topic", "")

        if master_viral_analysis is None:
            error = "Engine import failed: " + str(engine_error)

        else:
            try:
                report = master_viral_analysis(topic)

            except Exception as e:
                error = str(e)
                traceback.print_exc()

    return render_template(
        "index.html",
        report=report,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
