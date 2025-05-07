from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import pandas as pd
import sqlite3
import joblib

# Load dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)  # Feature names matter!
y = iris.target

# Train model
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save model + metadata
joblib.dump({
    'model': model,
    'feature_names': iris.feature_names,  # Critical for prediction
    'target_names': iris.target_names     # For human-readable outputs
}, 'model.joblib')

# Initialize SQLite DB
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY,
        sepal_length FLOAT,
        sepal_width FLOAT,
        petal_length FLOAT,
        petal_width FLOAT,
        predicted_class INT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()