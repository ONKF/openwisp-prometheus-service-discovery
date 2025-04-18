#!/usr/bin/env python3

import requests
from flask import Flask, json, request, render_template

app = Flask(__name__)

def api_call(url, token):
    # do request
    response = requests.get(f"{url}", headers={"Authorization": f"Bearer {token}"})

    # raise exception on http error and parse json response
    response.raise_for_status()
    response = response.json()
    
    # do recursive call if we've got a paginated result
    if response.get('next'):
        return response.get('results') + api_call(response.get('next'), token)

    # directly return 'results' on paginaged calls
    if response.get('results'):
        return response.get('results')

    return response

def get_devices(base_url, token):
    return api_call(f"{base_url}/api/v1/controller/device/", token)

def get_organizations(base_url, token):
    return api_call(f"{base_url}/api/v1/users/organization", token)

def get_device_location(base_url, token, device):
    return api_call(f"{base_url}/api/v1/controller/device/{device}/location/", token)

def transform_to_id(input):
    result = dict()

    for obj in input:
        result[obj.get('id')] = obj

    return result

@app.route("/service-discovery", methods=['GET'])
def service_discovery():
    try:
        result = list()

        url = request.args.get('url')
        token = request.args.get('token')

        # input validation
        if not url or not token:
            return app.response_class(
                status=400,
                mimetype="application/json",
                response=json.dumps({"error": "'url' and 'token' need to be defined"})
            )

        devices = get_devices(url, token)
        organizations = transform_to_id(get_organizations(url, token))

        for device in devices:
            location = get_device_location(url, token, device.get('id')).get('location')

            result.append({
                "targets": [f"{device.get('management_ip')}:9100"],
                "labels": {
                    "instance":             f"{device.get('name')}",
                    "__meta_model":         f"{device.get('model')}",
                    "__meta_location":      f"{location.get('properties').get('name')}",
                    "__meta_latitude":      f"{location.get('geometry').get('coordinates')[0]}",
                    "__meta_longitude":     f"{location.get('geometry').get('coordinates')[1]}",
                    "__meta_organization":  f"{organizations.get(device.get('organization')).get('name')}"
                }
            })

        return app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return app.response_class(
            response=json.dumps({'error': str(e)}),
            mimetype="application/json",
            status=500
        )

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)