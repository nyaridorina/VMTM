from flask import Flask, jsonify, render_template
from swear_detection import start_detection, stop_detection, is_swear_detected  # Import detection functions
import threading

app = Flask(__name__)

# Thread control for the detection process
detection_thread = None
detection_active = False

def detection_task():
    """Runs the detection process in a separate thread."""
    while detection_active:
        start_detection()  # Begin detection process
        if is_swear_detected():
            # Stop detection and allow frontend to fetch the alert
            global swear_detected
            swear_detected = True

# Initialize a variable to hold detection status
swear_detected = False

@app.route('/')
def index():
    """Renders the main frontend page."""
    return render_template('index.html')

@app.route('/start-detection', methods=['GET'])
def start_detection_route():
    """Starts the detection process and initiates a background thread."""
    global detection_thread, detection_active, swear_detected
    if detection_thread is None or not detection_thread.is_alive():
        detection_active = True
        swear_detected = False
        detection_thread = threading.Thread(target=detection_task)
        detection_thread.start()
    return jsonify(success=True)

@app.route('/stop-detection', methods=['GET'])
def stop_detection_route():
    """Stops the detection process."""
    global detection_active
    detection_active = False
    if detection_thread and detection_thread.is_alive():
        detection_thread.join()  # Wait for the thread to finish
    return jsonify(success=True)

@app.route('/check-status', methods=['GET'])
def check_status():
    """Checks if a swear word was detected and resets detection status."""
    global swear_detected
    alert = swear_detected
    swear_detected = False  # Reset status after checking
    return jsonify(alert=alert)

if __name__ == '__main__':
    app.run(debug=True)
