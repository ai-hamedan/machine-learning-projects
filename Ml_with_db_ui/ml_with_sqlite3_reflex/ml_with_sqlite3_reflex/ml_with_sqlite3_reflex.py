import reflex as rx
import sqlite3
import pandas as pd
import joblib

# Load model and metadata
model_data = joblib.load("model.joblib")
model = model_data["model"]
feature_names = model_data["feature_names"]
target_names = model_data["target_names"]

#test_sql_ml.py
class State(rx.State):
    # Input fields
    sepal_length: float = 5.1
    sepal_width: float = 3.5
    petal_length: float = 1.4
    petal_width: float = 0.2
    
    # Results
    prediction: str = ""
    confidence: float = 0.0

    def predict(self):
        # Convert inputs to DataFrame with correct feature names
        input_df = pd.DataFrame(
            [[self.sepal_length, self.sepal_width, self.petal_length, self.petal_width]],
            columns=feature_names
        )
        
        # Get prediction
        pred_class = model.predict(input_df)[0]
        proba = model.predict_proba(input_df).max()
        print(pred_class)

        # Update state
        self.prediction = target_names[pred_class]
        print(self.prediction)

        self.confidence = round(proba * 100, 2)
        
        # Log to DB
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO predictions 
            (sepal_length, sepal_width, petal_length, petal_width, predicted_class) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.sepal_length, self.sepal_width, 
             self.petal_length, self.petal_width, pred_class)
        )
        conn.commit()
        conn.close()

def index():
    return rx.container(
        rx.vstack(
            rx.heading("Iris Classifier"),
            rx.input(placeholder="Sepal Length", type="number", on_change=State.set_sepal_length),
            rx.input(placeholder="Sepal Width", type="number", on_change=State.set_sepal_width),
            rx.input(placeholder="Petal Length", type="number", on_change=State.set_petal_length),
            rx.input(placeholder="Petal Width", type="number", on_change=State.set_petal_width),
            # ... (more inputs for other features)
            rx.button("Predict", on_click=State.predict),
            rx.divider(),
            rx.cond(
                State.prediction,
                rx.text(f"Prediction: {State.prediction} (Confidence: {State.confidence}%)")
            ),
            spacing="7"
        ),
        padding="2em"
    )

app = rx.App()
app.add_page(index)
# app.compile()