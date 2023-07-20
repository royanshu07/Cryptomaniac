from flask import Flask, request, render_template,send_file, jsonify
import pickle
import requests
import pandas as pd
from patsy import dmatrices
from chat import get_response
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pickle
import plotly as px
import numpy as np
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predictions")
def prediction():
    return render_template('prediction.html')

@app.route("/blogs")
def blogs():
    return render_template('blogs.html')

@app.get("/support")
def index_get():
    return render_template("support2.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: CHECK IF TEXT IS VALID
    response = get_response(text)
    message = {"answer":response}
    return jsonify(message)

@app.route("/about")
def about():
    return render_template('about.html')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/predictions/<name>')
def search_crypto(name):
    print(name)
    datafile = open(f'{name}.txt', "rb")
    data = pickle.load(datafile)
    datafile.close()
    arr=np.arange(1,24)
    
    # Create a Figure object explicitly
    fig = Figure()

    # Add the plot lines to the Figure object
    ax = fig.add_subplot(111)
    ax.plot(arr, data)
    
    # Render the Figure object to an image
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    canvas.print_png(img)

    # Send the image data to the browser
    img.seek(0)
    return send_file(img, mimetype='image/png')
    # print(v)

    # name = name.capitalize() 
    # return render_template('crypt.html', name=name, v=v)

@app.route('/consultancy')
def consultancy():
    return render_template('consultancy.html')

@app.route('/pay')
def pay():
    return render_template('payment.html')

if __name__ == '__main__':
    # Start the Flask application
    app.run(debug=True)
