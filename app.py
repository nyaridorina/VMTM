from flask import Flask, jsonify, render_template
from swear_detection import start_detection, stop_detection, is_swear_detected

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main frontend page."""
    return render_template('index.html')

@app.route('/start-detection', methods=['GET'])
def start_detection_route():
    """Starts the detection process."""
    start_detection()  # Begin detection process
    return jsonify(success=True)

@app.route('/stop-detection', methods=['GET'])
def stop_detection_route():
    """Stops the detection process."""
    stop_detection()  # Stop the detection process
    return jsonify(success=True)

@app.route('/check-status', methods=['GET'])
def check_status():
    """Checks if a swear word was detected."""
    alert = is_swear_detected()
    return jsonify(alert=alert)

if __name__ == '__main__':
    # Run the app on all available IP addresses (0.0.0.0) and port 5000
    # In a development setting, it's better to run on '127.0.0.1' for security
    app.run(host='0.0.0.0', port=5000)
