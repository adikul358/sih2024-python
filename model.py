import pandas as pd
import numpy as np
import joblib
import random

regressor = joblib.load("regressor.pkl")
NewDataSet = joblib.load("newdata.pkl")
sc = joblib.load("sc.pkl")

def predict_power_consumption(date_str):
    date = pd.to_datetime(date_str, format="%Y-%m-%d %H:%M")
    
    last_60_days = NewDataSet.tail(60).values
    input_data = np.append(last_60_days, np.zeros(1))  # Append a placeholder for the prediction date
    input_data = input_data.reshape(-1, 1)
    input_data = sc.transform(input_data)
    
    X_input = []
    for i in range(60, len(input_data)):
        X_input.append(input_data[i-60:i])
    
    X_input = np.array(X_input)
    X_input = np.reshape(X_input, (X_input.shape[0], X_input.shape[1], 1))
    
    predicted_value = regressor.predict(X_input)
    predicted_value = sc.inverse_transform(predicted_value)
    
    return predicted_value[-1, 0]
    # return random.randrange(20*100000, 180*100000) / 100000

# # Example usage
# date_str = "15-09-2024 00.00"  # Replace with your desired date and time
# predicted_power = predict_power_consumption(date_str)
# print(f"Predicted Power Consumption for {date_str}: {predicted_power} MW")
