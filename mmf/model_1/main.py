import pickle
import numpy as np
from mmf.model_1.src.model import NLPModel
import os

def run_model():

    model = NLPModel()

    with open(os.path.join(os.path.dirname(__file__) , 'models/SentimentClassifier.pkl'), 'rb') as model_file:
        model.clf = pickle.load(model_file)

    with open(os.path.join(os.path.dirname(__file__) ,  'models/TFIDFVectorizer.pkl'), 'rb') as model_file:
        model.vectorizer = pickle.load(model_file)

    uq_vectorized = model.vectorizer_transform(np.array(["this is a sentence"]))
    prediction = model.predict(uq_vectorized)
    pred_proba = model.predict_proba(uq_vectorized)

    # Output either 'Negative' or 'Positive' along with the score
    if prediction == 0:
        pred_text = 'Negative'
    else:
        pred_text = 'Positive'

    # round the predict proba value and set to new variable
    confidence = round(pred_proba[0], 3)

    # create JSON object
    output = {'prediction': pred_text, 'confidence': confidence}

    return output

