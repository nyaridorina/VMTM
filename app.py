from flask import Flask, request, jsonify, render_template
import os
import tempfile
from swear_detection import detect_swear_words_in_audio, convert_audio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        audio_file.save(temp_audio.name)
        temp_audio_path = temp_audio.name

    try:
        # Convert the audio to the required format
        temp_converted_audio_path = temp_audio_path + '_converted.wav'
        convert_audio(temp_audio_path, temp_converted_audio_path)

        # Detect swear words in the converted audio file
        swear_word_detected = detect_swear_words_in_audio(temp_converted_audio_path)

        # Remove the converted audio file after processing
        os.unlink(temp_converted_audio_path)

        if swear_word_detected:
            message = 'Szitokszó észlelve az audióban!'
        else:
            message = 'Nincs szitokszó az audióban.'
    finally:
        os.unlink(temp_audio_path)
    
    return jsonify({'message': message}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
