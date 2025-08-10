from flask import Flask, render_template, request
from src.datascience.pipeline.prediction_pipelne import PredictionPipeline

app = Flask(__name__)

# Initialize prediction pipeline once
prediction_pipeline = PredictionPipeline()

@app.route("/github-webhook/", methods=["GET", "POST"])
def index():
    recommendations = []
    if request.method == "POST":
        movie_name = request.form.get("movie")
        if movie_name:
            try:
                # Normalize the movie title
                #convert moviename to lowercase
                movie_name = movie_name.lower()
                recommendations = prediction_pipeline.recommend(movie_name)
            except Exception as e:
                recommendations = [f"Error: {str('MOVIE NOT FOUND IN DATABASE')}"]
    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)