from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.prediction_pipeline import PredictionPipeline

predictor = PredictionPipeline()

app = FastAPI(title="Sentiment Prediction API", version="1.0")

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict_sentiment(input: TextInput):
    try:
        clean_text = predictor.text_cleaning(input.text)
        prediction = predictor.predict(clean_text)
        sentiment = "Positive" if prediction[0] == 0 else "Negative"
        return {"text": input.text, "prediction": sentiment, "raw": prediction}
    except Exception as e:
        return {"error": str(e)}