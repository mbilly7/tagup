from flask import Flask, request
from markupsafe import escape
import json

app = Flask(__name__)

dataset = []

@app.route("/data", methods=["POST"])
def post_data():
    request_data = request.get_json()
    global dataset

    dataset += request_data

    return "DATA COLLECTED."

def get_count_and_avg(li, sensor_id):
    sum = 0
    count = 0
    for r in li:
        if "value" in r and r["sensor"] == sensor_id:
            sum += r["value"]
            count += 1

    return count, sum / count


@app.route("/statistics/<sensor_id>", methods=["GET", "DELETE"])
def get_or_delete_data(sensor_id):
    global dataset
    if request.method == "GET":
        matching = {}

        if "sensor" not in dataset[0]:
            return "NO DATA TO SEARCH."

        for r in reversed(dataset):
            if r["sensor"] == escape(sensor_id):
                matching["last_measurement"] = r["timestamp"]
                break
        
        if "last_measurement" not in matching:
            matching["last_measurement"] = "null"
            matching["count"] = 0
            matching["avg"] = 0
        else:
            matching["count"], matching["avg"] = get_count_and_avg(dataset, sensor_id)

        return json.dumps(matching)
    elif request.method == "DELETE":
        length = len(dataset)
        new_list = []
        for i in range(length):
            if "sensor" not in dataset[i] or dataset[i]["sensor"] != sensor_id:
                new_list.append(dataset[i])

        dataset = new_list

    return ("", 204)

@app.route("/healthz", methods = ["GET"])
def get_health():
    return ("", 204)

if __name__ == "__main__":
    app.run(debug = True, port = 8080)