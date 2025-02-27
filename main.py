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

# Create a global counter instance
counter = AtomicCounter()

@app.route('/next', methods=['GET'])
def get_next_number():
    # Get the next unique integer
    next_num = counter.increment()
    return jsonify({"number": next_num})

@app.route('/reset', methods=['POST'])
def reset_counter():
    # Get optional value from request, default to 0
    new_value = request.json.get('value', 0) if request.json else 0
    try:
        new_value = int(new_value)
        current_value = counter.reset(new_value)
        return jsonify({
            "status": "success", 
            "message": f"Counter reset to {current_value}",
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