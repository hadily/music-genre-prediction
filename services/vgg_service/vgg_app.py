import os
import numpy as np
import librosa
import base64
import io
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Input
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sklearn.preprocessing import LabelEncoder


# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})

# Load the pre-trained VGG model
model_path = './models/vgg_model.h5' 
#print(f"TensorFlow version: {tf.__version__}")
vgg_model = tf.keras.models.load_model(model_path)
#print(f"Model summary: {vgg_model.summary()}")

# Define the list of genres (ensure the order matches LabelEncoder from training)
genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
encoder = LabelEncoder()
encoder.fit(genres)

# @app.route('/')
# def upload_form():
#     return render_template('upload.html')


@app.route('/')
def index():
    return "Welcome to the Music Genre Prediction App! Use /predict for predictions."

def extract_features(file_data):
    """
    Extract features from the audio file for model prediction.
    - Converts audio to a mel spectrogram.
    - Resizes the spectrogram to match the trained model's input dimensions.
    """
    try:
        y, sr = librosa.load(file_data, sr=None)
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
        
        if spectrogram.shape[1] < 128:
            spectrogram = librosa.util.fix_length(spectrogram, size=128, axis=1)
        else:
            spectrogram = spectrogram[:, :128]
        spectrogram = spectrogram[:43, :]
        spectrogram = spectrogram.reshape(1, 43, 128, 1)
        return spectrogram
    except Exception as e:
        raise ValueError(f"Feature extraction error: {str(e)}")

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the genre of an uploaded audio file.
    Accepts an audio file and returns the predicted genre.
    """
    try:
        # Check for audio file in the request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400

        # Get the audio file from the form-data
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Extract features from the audio file
        spectrogram = extract_features(audio_file)
        
        # Predict the genre using the model
        predictions = vgg_model.predict(spectrogram)
        genre_index = np.argmax(predictions, axis=1)[0]
        genre = genres[genre_index]  # Map index to genre name

        return jsonify({'genre': genre})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
