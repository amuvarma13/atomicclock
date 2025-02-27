from flask import Flask, jsonify
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

# Create a global counter instance
counter = AtomicCounter()

@app.route('/next', methods=['GET'])
def get_next_number():
    # Get the next unique integer
    next_num = counter.increment()
    return jsonify({"number": next_num})

if __name__ == '__main__':
    # Run with multiple workers to demonstrate thread safety
    app.run(host='0.0.0.0', port=8080, threaded=True)