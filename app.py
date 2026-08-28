from flask import Flask, render_template, request
from viral_ai import master_viral_analysis

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        topic = request.form.get("topic")

        try:
            result = master_viral_analysis(topic)
        except Exception as e:
            result = {
                "error": str(e)
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
