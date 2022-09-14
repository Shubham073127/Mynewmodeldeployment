import pickle
import pandas as pd
import numpy as np
from forex_python.converter import CurrencyRates 
from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route("/predict",methods=["POST"])
def predict():
    Material=int(request.form.get('Material'))
    print(Material)
    Valid_to = int(request.form.get('Valid_to'))
    print(Valid_to)
    
    Valid_From = int(request.form.get('Valid_From'))
    print(Valid_From)
    
    Proc_status = float(request.form.get('Proc_status'))
    print(Proc_status)
    
    Unit = request.form.get('Unit')
    if(Unit == 'AUD'):
        Unit=0
    elif(Unit == 'CAD'):
        Unit=1
    elif(Unit == 'CHF'):
        Unit=2
    elif(Unit == 'DKK'):
        Unit=3
    elif(Unit == 'EUR'):
        Unit=4
    elif(Unit == 'GBP'):
        Unit=5
    elif(Unit == 'HKD'):
        Unit=6
    elif(Unit == 'ILS'):
        Unit=7
    elif(Unit == 'JPY'):
        Unit=8
    elif(Unit == 'KRW'):
        Unit=9
    elif(Unit == 'MXN'):
        Unit=10
    elif(Unit == 'MYR'):
        Unit=11
    elif(Unit == 'NWD'):
        Unit=12
    elif(Unit == 'NZD'):
        Unit=13
    elif(Unit == 'SEK'):
        Unit=14
    elif(Unit == 'SGD'):
        Unit=15
    elif(Unit == 'THB'):
        Unit=16
    elif(Unit == 'USD'):
        Unit=17
    elif(Unit == 'ZAR'):
        Unit=18
    print(Unit)
    
    exchange_rate = Unit
    c = CurrencyRates()
    if(exchange_rate == 0):
        exchange_rate=c.get_rate('AUD', 'USD')
        symbol ='AUD'
    elif(exchange_rate == 1):
        exchange_rate=c.get_rate('CAD', 'USD')
        symbol = 'CAD'
    elif(exchange_rate == 2):
        exchange_rate=c.get_rate('CHF', 'USD')
        symbol = 'CHF'
    elif(exchange_rate == 3):
        exchange_rate=c.get_rate('DKK', 'USD')
        symbol = 'DKK'
    elif(exchange_rate == 4):
        exchange_rate=c.get_rate('EUR', 'USD')
        symbol = 'EUR'
    elif(exchange_rate == 5):
        exchange_rate=c.get_rate('GBP', 'USD')
        symbol = 'GBP'
    elif(exchange_rate == 6):
        exchange_rate=c.get_rate('HKD', 'USD')
        symbol = 'HKD'
    elif(exchange_rate == 7):
        exchange_rate=c.get_rate('ILS', 'USD')
        symbol = 'ILS'
    elif(exchange_rate == 8):
        exchange_rate=c.get_rate('JPY', 'USD')
        symbol = 'JPY'
    elif(exchange_rate == 9):
        exchange_rate=c.get_rate('KRW', 'USD')
        symbol = 'KRW'
    elif(exchange_rate == 10):
        exchange_rate=c.get_rate('MXN', 'USD')
        symbol = 'MXN'
    elif(exchange_rate == 11):
        exchange_rate=c.get_rate('MYR', 'USD')
        symbol = 'MYR'
    elif(exchange_rate == 12):
        exchange_rate=c.get_rate('NZD', 'USD')
        symbol = 'NZD'
    elif(exchange_rate == 13):
        exchange_rate=c.get_rate('SEK', 'USD')
        symbol = 'SEK'
    elif(exchange_rate == 14):
        exchange_rate=c.get_rate('SGD', 'USD')
        symbol = 'SGD'
    elif(exchange_rate == 15):
        exchange_rate=c.get_rate('THB', 'USD')
        symbol = 'THB'
    elif(exchange_rate == 16):
        exchange_rate=0.033 ## TWD to USD
        symbol = 'TWD'
    elif(exchange_rate == 17):
        exchange_rate=1.0
        symbol = 'USD'
    elif(exchange_rate== 18):
        exchange_rate=c.get_rate('ZAR', 'USD')
        symbol = 'ZAR'
    print(exchange_rate)
    model_data = [Material, Valid_to, Valid_From, Proc_status, Unit, exchange_rate]
    data = np.array(model_data).reshape(1,-1)
    Model_choice = request.form.get('Model_choice')
    if Model_choice == 'dtr':
        selection = 'Decision Tree Regressor'
        dtr = pickle.load(open('Price Optimization_dt.pkl', 'rb'))
        prediction = dtr.predict(data)
        print(prediction)
        pred_conv = prediction / exchange_rate
        print(pred_conv)
        adjr2 = round(0.9913677561692442*100, 3)
        rmsle = round(0.1616324417118822, 3)
    elif Model_choice == 'rfr':
        selection = 'Random Forest Regressor'
        rfr = pickle.load(open('Price Optimization.pkl', 'rb'))
        prediction = rfr.predict(data)
        print(prediction)
        pred_conv = prediction / exchange_rate
        print(pred_conv)
        adjr2 = round(0.9864314615240412*100, 3)
        rmsle = round(0.15488977788772007, 3)
    
    
    
    
    return render_template('index.html', material = Material, pred_conv=pred_conv, symbol=symbol, selection = selection, valid_to=Valid_to, valid_from=Valid_From, model_accuracy=adjr2, rmsle=rmsle)
    return redirect(url_for("index"))
