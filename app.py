from flask import Flask, render_template, request, jsonify
from src.datascience.pipeline.prediction_pipelne import PredictionPipeline

app = Flask(__name__)

# Initialize prediction pipeline once
prediction_pipeline = PredictionPipeline()

@app.route("/github-webhook/", methods=["POST"])
def github_webhook():
    try:
        payload = request.get_json(force=True)  # Get JSON from GitHub
        print("Webhook received:", payload)  # Log for debugging
        # You can trigger Jenkins or run your own logic here
        return jsonify({"status": "Webhook received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    if request.method == "POST":
        movie_name = request.form.get("movie")
        if movie_name:
            try:
                movie_name = movie_name.lower()
                recommendations = prediction_pipeline.recommend(movie_name)
            except Exception:
                recommendations = ["Error: MOVIE NOT FOUND IN DATABASE"]
    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True, port=5000)