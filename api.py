import json
from flask import Flask, request, Response
from flask_cors import CORS
from datetime import datetime, timedelta
import model

app = Flask(__name__)
CORS(app)

MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def genDateArr(freq):
    dates = [datetime.now()]

    # Get next 6 months
    if (freq == "monthly"):
        for i in range(1,5):
            dates.append(dates[i-1] + timedelta(MONTH_DAYS[dates[i-1].month-1]))
        print("monthly", dates)

    # Get next 12 weeks
    elif (freq == "weekly"):
        for i in range(1,11):
            dates.append(dates[i-1] + timedelta(7))
        print("weekly", dates)

    # Get next 60 days
    elif (freq == "daily"):
        for i in range(1,29):
            dates.append(dates[i-1] + timedelta(1))
        print("daily", dates)

    return [x.strftime("%Y-%m-%d %H:%M") for x in dates]

@app.route('/api/predict', methods=['GET'])
def predict():
    print(request.headers)
    date = request.args.get("date")
    prediction = { "power_consumption": str(model.predict_power_consumption(date)) }
    resp = Response(response=json.dumps(prediction), status=200, mimetype="application/json")
    return resp

@app.route('/api/trendline', methods=['GET'])
def trend():
    print(request.headers)
    freq = request.args.get("freq")
    data = {}
    for x in genDateArr(freq):
        data[x] = str(model.predict_power_consumption(x))
    resp = Response(response=json.dumps(data), status=200, mimetype="application/json")
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5003)