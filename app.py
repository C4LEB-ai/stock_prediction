from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor



# One hot encode the 'coin_name' feature
# data = pd.get_dummies(data, columns=['coin_name'])


# Create a Flask instance
app = Flask(__name__)

# Define the index page
@app.route('/')
def index():
    return render_template('./index.html')

# Define the predict page
@app.route('/predict', methods=['POST'])
def predict():
    try:
        open = float(request.form['open']) if request.form['open'] else 0.0
        high = float(request.form['high']) if request.form['high'] else 0.0
        low = float(request.form['low']) if request.form['low'] else 0.0
        date = request.form['date'] if request.form['date'] else 0.0
        volume = float(request.form['volume']) if request.form['volume'] else 0.0
        coin_name = str(request.form['coin_name'])

        # rest of the code for prediction
        
    except Exception as e:
        x = ("Error: {}".format(str(e)))
        return  render_template('index.html', data=x)



        # output validation
    if not coin_name or not open or not high or not low or not date or not volume:
        return render_template('index.html', data = "Please fill out all fields.")
    else:



        #Creating a data dictionary
        data_dict = {'Date': [date],'Open': [open], 'High': [high], 'Low': [low], 'Volume': [volume],
                                'ADA_GBP': [0], 'ATOM_GBP': [1], 'AVAX_GBP': [0], 'BNB_GBP': [0], 'BTC_GBP': [0], 'DAI_GBP': [0],
                                'DOGE_GBP': [0], 'DOT_GBP': [0], 'ETH_GBP': [0], 'FIL_GBP': [0], 'FTM_GBP': [0], 'GRC_GBP': [0],
                                'LINK_GBP': [0], 'LTC_GBP': [0], 'MATIC_GBP': [0], 'SOL_GBP': [0], 'TRX_GBP': [0], 'USDC_GBP': [0],
                                'USDT_GBP': [0], 'XRP_GBP': [0]}

        data_dict[coin_name] = [1]
        # create a new DataFrame with the same columns as the training data
        new_data = pd.DataFrame(data_dict)
        # convert the date column to a datetime data type
        new_data['Date'] = pd.to_datetime(new_data['Date'])
        # convert the date column to a float data type using Unix time (seconds since 1970-01-01)
        new_data['Date'] = (new_data['Date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        new_data['Date'] = new_data['Date'].astype(float)

        # make a prediction using the ensemble model
        model  = joblib.load('ensemble.sav')
        close_price = (f"CLOSE: {model.predict(new_data)[0]}")
        

        # Return the prediction to the user
        return render_template('index.html', data=close_price)



if __name__ == '__main__':
    app.run(debug=True)
