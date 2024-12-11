import os
import pickle
import librosa
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tempfile

app = Flask(__name__)
CORS(app)


@app.route('/')
def upload_form():
    return render_template('upload.html')

model_path = "./models/genre_model.pkl"

# Define a custom temp directory where the Flask app has write permissions
TEMP_DIR = './temp'

# Function to extract Mel spectrogram features
def extractMelSpectrogram_features(file_bytes):
    # Create a temporary file in the custom temp directory
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir=TEMP_DIR) as temp_file:
        temp_file.write(file_bytes)
        temp_file.flush()
        signal, rate = librosa.load(temp_file.name, sr=None)
    
    hop_length = 512
    n_fft = 2048
    n_mels = 128
    S = librosa.feature.melspectrogram(y=signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    S_DB = librosa.power_to_db(S, ref=np.max).flatten()[:1280]
    return S_DB

def predict_genre(file_bytes, clf):
    mel_features = extractMelSpectrogram_features(file_bytes)
    genre_label = clf.predict([mel_features])[0]  # Assuming this directly gives the genre name
    return genre_label  # No need to use index anymore

try:
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract the file from the incoming request
    file = request.files.get('file')  # Assuming 'file' is the name of the input field in the HTML form
    
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Read the file as bytes
    file_bytes = file.read()

    # Call the predict_genre function with the file bytes and the clf model
    try:
        genre = predict_genre(file_bytes, clf)
        return jsonify({"genre": genre}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
