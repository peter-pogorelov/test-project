import joblib
import pathlib
import numpy as np
from flask import Flask, request

MODELS_DIR = pathlib.Path('./models')

MODEL = joblib.load(MODELS_DIR.joinpath('model.pkl'))
SCALER_INPUT = joblib.load(MODELS_DIR.joinpath('scaler_input.pkl'))
SCALER_OUTPUT = joblib.load(MODELS_DIR.joinpath('scaler_output.pkl'))

app = Flask("prediction service")

@app.route('/predict_price', methods = ['GET'])
def predict():
    open_plan = request.args.get('open_plan', default=-1, type=int)
    rooms = request.args.get('rooms', default=-1, type=int)
    area = request.args.get('area', default=-1, type=float)
    renovation = request.args.get('renovation', default=-1, type=int)

    x = np.array([open_plan, rooms, area, renovation]).reshape(1, -1)
    x = SCALER_INPUT.transform(x)
    result = MODEL.predict(x)
    result = SCALER_OUTPUT.inverse_transform(result.reshape(1, -1))

    return str(result[0][0])


if __name__ == '__main__':
    app.run(debug=True)