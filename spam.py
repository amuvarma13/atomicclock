import requests
import threading

def make_request():
    try:
        response = requests.get("http://34.27.188.237:8080/next")
        if response.status_code == 200:
            print(f"Got number: {response.json()['number']}")
        else:
            print(f"Request failed with status {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Create and start multiple threads
threads = []
for _ in range(100):  # Making 100 concurrent requests
    thread = threading.Thread(target=make_request)
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All requests completed")