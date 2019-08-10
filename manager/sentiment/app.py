from flask import Flask
import pickle
import numpy as np
from manager.sentiment.model import NLPModel

model = NLPModel()

clf_path = 'lib/models/SentimentClassifier.pkl'
with open(clf_path, 'rb') as f:
    model.clf = pickle.load(f)

vec_path = 'lib/models/TFIDFVectorizer.pkl'
with open(vec_path, 'rb') as f:
    model.vectorizer = pickle.load(f)

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

print (output)

