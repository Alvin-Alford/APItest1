from flask import Flask, request, jsonify, render_template
from flask_httpauth import HTTPBasicAuth
import json
import os.path
import time


app = Flask(__name__)
auth = HTTPBasicAuth()

history = {} 

correct_password = "315a35988098506619f3d728619755c24403b5eb"
# Specify the desired path to save the file

data = 'data.json'

timevalue = time.ctime(time.time())

@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    return jsonify({"message": "Login successful!"}), 200


@app.route('/', methods=['POST','GET'])
def site():
    return render_template('homepage.html')

@app.route('/register', methods=['POST'])
@auth.login_required
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

@app.route('/devicelist')
@auth.login_required
def get_devices():
  # Load data from JSON file
  try:
    with open('data.json', 'r') as f:
      data = json.load(f)
  except FileNotFoundError:
    return jsonify({'error': 'data.json not found'}), 404

  # Mask passwords before returning data
  return jsonify(data)

# Replace with your actual user data storage and validation logic
@auth.verify_password
def verify_password(password):
    global correct_password
    if password == correct_password:
        return True

    return False


@app.route('/connections', methods = ['GET'])
@auth.login_required
def renderconnectionspage():

    return render_template('connectionspage.html')


@app.route('/<devicename>/terminal', methods=['POST', 'GET'])
@auth.login_required
def handlecommandsandresult(devicename):
  if request.method == 'GET':
    # Retrieve command history for this device
    device_history = history.get(devicename, [])
    return render_template('terminal.html', devicename=devicename, history=device_history)

  header = request.json.get('Header')

  if header == 'Command':
    command = request.json.get('Commandfrom')
    history.setdefault(devicename, []).append({'Command': command})
    return jsonify({"Commandfordevice": command})
  elif header == 'Result':
    result = request.json.get('Resultfrom')
    # Assuming the last command for the device is the relevant one
    last_command_index = len(history.get(devicename, [])) - 1
    if last_command_index >= 0:
      history[devicename][last_command_index]['Result'] = result
    return jsonify({"Resultforweb": result}) 
  else:
    resp = jsonify({"Error" : "Wrong header"})
    return resp




if __name__ == '__main__':
    app.run(debug=True, port=5556, use_reloader=True)
