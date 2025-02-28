from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

# Using a class to encapsulate the counter and lock
class AtomicCounter:
    def __init__(self, initial_value=0):
        self.value = initial_value
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.value += 1
            return self.value
    
    def reset(self, value=0):
        with self.lock:
            self.value = value
            return self.value

# Create three independent counter instances
default_counter = AtomicCounter()
created_counter = AtomicCounter()
crashed_counter = AtomicCounter()

# Endpoints for the default counter
@app.route('/next', methods=['GET'])
def get_next_number():
    next_num = default_counter.increment()
    return jsonify({"number": next_num})

@app.route('/value', methods=['GET'])
def get_current_value():
    with default_counter.lock:
        current_value = default_counter.value
    return jsonify({"number": current_value})

@app.route('/reset', methods=['GET'])
def reset_counter():
    new_value = request.args.get('value', 0)
    try:
        new_value = int(new_value)
        current_value = default_counter.reset(new_value)
        return jsonify({
            "status": "success", 
            "message": f"Default counter reset to {current_value}",
            "value": current_value
        })
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Invalid value provided. Please provide an integer."
        }), 400

# Endpoints for the "created" counter
@app.route('/created/next', methods=['GET'])
def get_next_created():
    next_num = created_counter.increment()
    return jsonify({"number": next_num})

@app.route('/created/value', methods=['GET'])
def get_value_created():
    with created_counter.lock:
        current_value = created_counter.value
    return jsonify({"number": current_value})

@app.route('/created/reset', methods=['GET'])
def reset_created():
    new_value = request.args.get('value', 0)
    try:
        new_value = int(new_value)
        current_value = created_counter.reset(new_value)
        return jsonify({
            "status": "success", 
            "message": f"Created counter reset to {current_value}",
            "value": current_value
        })
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Invalid value provided. Please provide an integer."
        }), 400

# Endpoints for the "crashed" counter
@app.route('/crashed/next', methods=['GET'])
def get_next_crashed():
    next_num = crashed_counter.increment()
    return jsonify({"number": next_num})

@app.route('/crashed/value', methods=['GET'])
def get_value_crashed():
    with crashed_counter.lock:
        current_value = crashed_counter.value
    return jsonify({"number": current_value})

@app.route('/crashed/reset', methods=['GET'])
def reset_crashed():
    new_value = request.args.get('value', 0)
    try:
        new_value = int(new_value)
        current_value = crashed_counter.reset(new_value)
        return jsonify({
            "status": "success", 
            "message": f"Crashed counter reset to {current_value}",
            "value": current_value
        })
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Invalid value provided. Please provide an integer."
        }), 400

if __name__ == '__main__':
    # Run with multiple workers to demonstrate thread safety
    app.run(host='0.0.0.0', port=8080, threaded=True)
