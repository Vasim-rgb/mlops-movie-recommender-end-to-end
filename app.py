from flask import Flask, render_template, request
import joblib
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(_name_)

# Load model once
model_data = joblib.load("artifacts/model_trainer/model.joblib")
vectorizer = model_data["vectorizer"]
vectors = model_data["vectors"]
titles = model_data["titles"]

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    movie_input = ""
    if request.method == "POST":
        movie_input = request.form["movie"]
        if movie_input in titles:
            idx = titles.index(movie_input)
            distances = cosine_similarity([vectors[idx]], vectors)
            recommended_indices = distances[0].argsort()[::-1][1:6]
            recommendations = [titles[i] for i in recommended_indices]
        else:
            recommendations = [f"'{movie_input}' not found."]
    return render_template("index.html", recommendations=recommendations, movie_input=movie_input)

if _name_ == "_main_":
    app.run(debug=True)