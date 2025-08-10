import pandas as pd

df = pd.read_csv(r"C:\Users\vasim\Desktop\movie recomm\artifacts\data_transformation\transformed_data.csv")
print(df.head(5))


import numpy as np
import pandas as pd
import mlflow
import joblib
import random
import os

# Load similarity matrix and movie data
sim = joblib.load("sim.joblib")  # cosine similarity matrix
movies_df = pd.read_csv("movies.csv")  # must have 'title' column

# Ensure sim and movies_df match
assert sim.shape[0] == len(movies_df), "Matrix rows and movie count mismatch!"

# Start MLflow run
mlflow.start_run(run_name="cosine_similarity_eval")

# ---------------------
# Quantitative Metrics
# ---------------------
shape = sim.shape
mask = ~np.eye(shape[0], dtype=bool)
values = sim[mask]

metrics = {
    "matrix_rows": shape[0],
    "matrix_cols": shape[1],
    "avg_similarity": float(np.mean(values)),
    "max_similarity": float(np.max(values)),
    "min_similarity": float(np.min(values)),
    "std_similarity": float(np.std(values)),
    "sparsity": float(np.sum(values == 0) / values.size)
}

# Log metrics to MLflow
for k, v in metrics.items():
    mlflow.log_metric(k, v)

# ---------------------
# Qualitative Samples
# ---------------------
sample_movies = random.sample(range(len(movies_df)), min(5, len(movies_df)))
qualitative_results = []

for idx in sample_movies:
    title = movies_df.iloc[idx]['title']
    similar_indices = np.argsort(sim[idx])[::-1][1:6]  # top 5 excluding self
    recommended_titles = movies_df.iloc[similar_indices]['title'].tolist()
    
    qualitative_results.append({
        "movie": title,
        "recommendations": recommended_titles
    })

# Save qualitative results as CSV for MLflow artifact
os.makedirs("artifacts", exist_ok=True)
qual_df = pd.DataFrame(qualitative_results)
qual_path = "artifacts/qualitative_eval.csv"
qual_df.to_csv(qual_path, index=False)

mlflow.log_artifact(qual_path)


