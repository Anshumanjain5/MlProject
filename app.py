from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline, CustomData

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('predict.html')
    else:
        try:
            
            reading_score = request.form.get('reading_score')
            writing_score = request.form.get('writing_score')
            if not reading_score.isdigit() or not writing_score.isdigit():
                return render_template('predict.html', results="Please enter valid numeric values for scores.")
            
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=int(reading_score),
                writing_score=int(writing_score)
            )
            
            pred_df = data.get_data_as_dataframe()
            pred_pipeline = PredictPipeline()
            prediction = pred_pipeline.predict(pred_df)
            return render_template('predict.html', results=int(prediction[0]))
        
        except Exception as e:
            return render_template('predict.html', results=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
