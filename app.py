import joblib
import pathlib
import numpy as np
from flask import Flask, request, abort

CURRENT_DIR = pathlib.Path(__file__).absolute().parent
MODELS_DIR = CURRENT_DIR.joinpath('models')

MODEL_DEFAULT = joblib.load(MODELS_DIR.joinpath('rf_default.bin'))
MODEL_LOG = joblib.load(MODELS_DIR.joinpath('rf_log.bin'))

SCALER_X = joblib.load(MODELS_DIR.joinpath('sc_X.bin'))
SCALER_Y = joblib.load(MODELS_DIR.joinpath('sc_y.bin'))
SCALER_Y_LOG = joblib.load(MODELS_DIR.joinpath('sc_y_log.bin'))

app = Flask("prediction service")

@app.errorhandler(500)
def internal_error(error):
    return "500 error"

@app.route('/predict_price', methods = ['GET'])
def predict():
    if not('open_plan' in request.args and 'rooms' in request.args \
        and 'area' in request.args and 'renovation' in request.args):
        abort(500)

    model_type = request.args.get('model_version', default=1, type=int)
    open_plan = request.args.get('open_plan', type=int)
    rooms = request.args.get('rooms', type=int)
    area = request.args.get('area', type=float)
    renovation = request.args.get('renovation', type=int)

    if model_type == 1:
        x = np.array([open_plan, rooms, area, renovation]).reshape(1, -1)
        x = SCALER_X.transform(x)
        result = MODEL_DEFAULT.predict(x)
        
        result = SCALER_Y.inverse_transform(result.reshape(1, -1))

        return str(result[0][0])
    elif model_type == 2:
        x = np.array([open_plan, rooms, area, renovation]).reshape(1, -1)
        x = SCALER_X.transform(x)
        result = MODEL_LOG.predict(x)
        result = SCALER_Y_LOG.inverse_transform(result.reshape(1, -1))

        return str(np.exp(result[0][0]))
    else:
        abort(500)


if __name__ == '__main__':
    app.run(debug=False)