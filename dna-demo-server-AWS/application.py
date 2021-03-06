from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from subprocess import *
import sys
import json


application = app = Flask(__name__)
api = Api(app)
@app.route("/", methods=["GET"])
def welcome():
    return "DNA Demo Proxy Server is Running"

@app.route("/check", methods=["POST"])
def change_msg():
    return "Server is hit"

@app.route("/config", methods=["GET"])
def preset():
    f = open("output.json")
    preset_data = f.read()
    return jsonify(preset_data)

@app.route("/analyze", methods=["POST"])
def rev_proxy():
    data = request.json #data from the application, contains list of coordinates [x,y]
    
    data = json.dumps(data) #Converting to json format with 'Read' as key
    data_to_process = json.loads(data)

    print(len(data_to_process["Read"]))
    data_processed = []
    for i in range(len(data_to_process["Read"])):
        data_processed.append(data_to_process["Read"][i][1])

    data_to_srv = json.dumps({"Read":data_processed})
    
    output_frm_srv = Popen(["python3","smarten-demo-srv.py", data_to_srv], stdout=PIPE,universal_newlines=True).stdout
    data_frm_server = output_frm_srv.read()
    data_frm_server = jsonify(data_frm_server)
    return data_frm_server

if __name__ == '__main__':
    app.run()
