import json
import threading
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from modules import hardware_control, database_operations, port_operations
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        bit = int(request.form['bit'])
        state = request.args.get('state')
        if state in ['on', 'off']:
            hardware_control.update_control_signal(bit, state)
        
        pin = str(request.form['pin']) 
        status = request.args.get('status')
        if status in ['on', 'off']:
            hardware_control.simulate_input_pins(pin, status)
    return render_template('index.html')

@app.route('/pin_status')
def pin_status():
    pin_status = app.config.get('pin_status', {})
    return jsonify(pin_status)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/save_config', methods=['POST'])
def save_config():
    # Check if request.form is not None
    if not request.form:
        flash('No data received.', 'error')
        return redirect(url_for('home'))
    
    # Convert form data to dictionary and save to file
    try:
        data = request.form.to_dict()
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        config.update(data)
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    except FileNotFoundError:
        # If config.json doesn't exist, create it with the new data
        with open('config.json', 'w') as config_file:
            json.dump(data, config_file, indent=4)
    except Exception as e:
        flash(f'Error saving data: {str(e)}', 'error')
        return redirect(url_for('home'))
    
    # Redirect to home page or show success message
    flash('Data saved successfully!', 'success')
    return redirect(url_for('home'))



if __name__ == '__main__':
    # Start background thread to listen pin status
    pin_status_thread = threading.Thread(target=hardware_control.listen_input_pins, daemon=True)
    pin_status_thread.start()
    # database_operations.store_data_transaksi(1)
    
    # Start Flask server
    app.run(debug=True, port=5000)