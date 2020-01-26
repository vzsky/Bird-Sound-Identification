# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 12:26:40 2020

@author: 6100267
"""

from flask import Flask, render_template, request
from keras.models import load_model, Model
from keras.backend import clear_session
from librosa import load, frames_to_time
from librosa.feature import melspectrogram
from librosa.onset import onset_detect
import numpy as np
import os

app = Flask(__name__, template_folder = 'template')  


@app.route('/')  
def upload():  
    return render_template("uploadfile.html")  
 
@app.route('/result', methods = ['POST'])  
def result():  
    if request.method == 'POST':  
        testing = []
        f = request.files['file']
        f.save(f.filename)  
        file = f.filename
        model = load_model('Birdmodel.h5') 
        Y, SR = load(file, res_type = 'kaiser_fast')
        onsets = frames_to_time(onset_detect(Y, SR), SR)
        leading_silence = onsets[0]
        y, sr = load(file, offset = leading_silence, res_type = 'kaiser_fast', duration=10)
        spec = melspectrogram(y=y, sr=sr)
        testing.append(spec)
        testing = np.asarray(testing)
        result = Model.predict(model, testing)
        if(np.where(result[0] == max(result[0]))[0] == 0):
            spe = 'Vanellus indicus'
        elif(np.where(result[0] == max(result[0]))[0] == 1):
            spe = 'Acridotheres tristis'
        elif(np.where(result[0] == max(result[0]))[0] == 2):
            spe = 'Columba Livia'
        elif(np.where(result[0] == max(result[0]))[0] == 3):
            spe = 'Amaurornis phoenicurus'
        elif(np.where(result[0] == max(result[0]))[0] == 4):
            spe = 'Centropus sinensis'
        os.remove(file)
        clear_session()
        return render_template("result.html", name = f.filename, species = spe)
  
if __name__ == '__main__':  
    app.run(debug = True)  
