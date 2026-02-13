from flask import Flask, request
import json

import pprint
from src.appointment.appointmentapi import run_optimization
from src.util.config_loader import Config

app = Flask(__name__)

@app.route('/core-stack-optimizer/optimize', methods=['GET'])
def optimize():

    try:
        simulate  = request.args.get("simulate")
        simulate = True if (simulate==True) or (simulate.lower()=="true") else False
    except:
        simulate = False
    print("Simulate is set to ",simulate)

    input_params = {"optimizationSummaryId": request.args.get("optimizationSummaryId"),
                    "locationUUID": request.args.get("locationUUID"),
                    "simulate": simulate
                    }
    print("INPUT:",input_params)
    # run_optimization(input_params)
    return run_optimization(input_params)


if __name__ == '__main__':
    config_port = Config.value("config_port")
    pprint.pprint('Server Listening to port : {}'.format(config_port))
    app.run(host='0.0.0.0', port=config_port, debug=True, threaded=True)
