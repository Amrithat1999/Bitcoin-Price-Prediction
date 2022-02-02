from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd

app = Flask(__name__)
d=pd.read_csv('bitstampUSD_1-min_data_2012-01-01_to_2018-11-11.csv')
model = pickle.load(open("bitcoin.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("bitcoin.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Departure Date
        Timestamp = request.form["Timestamp"]
        day = int(pd.to_datetime(Timestamp, format="%Y-%m-%dT%H:%M").day)
        month = int(pd.to_datetime(Timestamp, format="%Y-%m-%dT%H:%M").month)
        year = int(pd.to_datetime(Timestamp, format="%Y-%m-%dT%H:%M").year)

        Open = float(request.form["Open"])
        High = float(request.form["High"])
        Low = float(request.form["Low"])
        Close = float(request.form["Close"])
        Volume_BTC = float(request.form["Volume_BTC"])
        Volume_Currency = float(request.form["Volume_Currency"])

        prediction = model.predict([[Open,High,Low,Close,Volume_BTC,Volume_Currency,day,month,year]])

        output = round(prediction[0], 2)

        return render_template('bitcoin.html', prediction_text="Bitcoin price is.₹ {}".format(output))

    return render_template("bitcoin.html")

if __name__ == "__main__":
    app.run(debug=True)
