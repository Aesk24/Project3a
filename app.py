from flask import Flask, render_template, request
from charting import make_chart
from av_client import fetch_series, SERIES_OPTIONS
import pandas as pd
from datetime import datetime, date

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

#Get stocks
symbols_df = pd.read_csv("stocks.csv")
symbols = symbols_df['Symbol'].tolist()

app.route("/", methods=["GET", "POST"])
def index():
    chart_html = None
    errors = None

    return render_template("index.html", symbols=symbols, chart_html=chart_html)


app.run(host="0.0.0.0")