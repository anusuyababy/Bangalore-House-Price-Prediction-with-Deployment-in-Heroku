# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:30:21 2020

@author: DELL
"""


from flask import Flask, render_template, request, jsonify
import json
import pickle
import numpy as np

columns = None
model = None


app = Flask(__name__)
with open("columns.json", "r") as f:
    columns = json.load(f)["data_columns"]
    
clf = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/location')
def location():
    return jsonify(columns[8:-1])

@app.route('/area')
def area():
    return jsonify(columns[4:8])


@app.route("/predict", methods=['POST'])
def predict():
    area_type = request.form['area_type']
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    balcony = int(request.form['balcony'])
    
    
    area_type_ind = columns.index(area_type.lower())
    location_ind = columns.index(location.lower())
    
    data = np.zeros(len(columns))
    data[0] = bhk
    data[1] = total_sqft
    data[2] = bath
    data[3] = balcony
    data[area_type_ind] = 1
    data[location_ind] = 1
    
    prediction = clf.predict([data])
    
    output = round(prediction[0], 2)
    
    return render_template('index.html', prediction='Price in Lakhs (INR) {}'.format(output))
    

    
if __name__=="__main__":
    app.run(debug=True)