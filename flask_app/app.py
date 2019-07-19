#importing libraries
import os
import numpy as np
import flask
import librosa
from werkzeug import secure_filename
from flask import Flask, render_template, request
import pandas as pd
import pickle
import json, requests
from DataPoint import DataPoint
from datacleaning import DataCleaner

class Model():

    def __init__(self, arr):
        self.arr = arr

    def predict(self):
        model = pickle.load(open('model.pkl', 'rb'))
        self.model = model
        pred = model.predict_proba(self.arr.reshape(1, -1))
        if pred[0][1] >= 0.8:
            pred_bi = "High Risk"
        elif pred[0][1] < 0.8 and pred[0][1] >= 0.3:
            pred_bi = "Medium Risk"
        else:
            pred_bi = "Low Risk"
        return pred_bi


app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def get_fraud():
    single_row = DataPoint().df
    cleaned_data = DataCleaner(single_row).X
    pred = Model(cleaned_data).predict()
    return render_template('results.html', data=(pred, cleaned_data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
