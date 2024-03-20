from flask import Flask, request, jsonify, render_template
import json
import os.path

app = Flask(__name__)

# Specify the desired path to save the file
data = 'data.json'

@app.route('/', methods=['POST','GET'])
def site():
    return render_template('homepage.html')

@app.route('/register', methods=['POST'])
def receive_data():
    data = request.json
    # Check if the file exists, if not create it

    # Open the file in read mode and load existing data
    with open(data, 'r') as file:
        file_data = json.load(file)

    # Check if there is an existing JSON object with the same 'Device' key
    device_index = None
    for index, item in enumerate(file_data):
        if 'Device' in item and 'Device' in data and item['Device'] == data['Device']:
            device_index = index
            break

    # If there is an existing JSON object with the same 'Device' key, overwrite it
    if device_index is not None:
        file_data[device_index] = data
    else:
        # Otherwise, append the new data
        file_data.append(data)

    # Write the modified data back to the file
    with open(data, 'w') as file:
        json.dump(file_data, file, indent=4)


    resp = jsonify(success=True)
    return resp

@app.route('/<devicename>' , methods = ['POST','GET'])
def handlecommandsandresult(devicename):

    header = request.json.get('Header')

    if header == 'Command':
        return jsonify({"Commandfordevice" : request.json.get('Commandfrom')})
    elif header == 'Result':
        return jsonify({"Resultforweb": request.json.get('Resultfrom')}) 
    else:
        resp = jsonify(success=False)
        return resp


    return

if __name__ == '__main__':
    app.run(debug=True, port=5556, use_reloader=False)

