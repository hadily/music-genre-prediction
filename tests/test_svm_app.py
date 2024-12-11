import pytest
import io
from io import BytesIO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/svm_service')))
from svm_app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict_valid_file(client):
    # Path to the test audio file
    audio_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'disco.00004.wav')
    
    # Open the audio file and send it in the POST request
    with open(audio_file_path, 'rb') as audio_file:
        data = {
            'file': (BytesIO(audio_file.read()), 'disco.00004.wav')
        }

        response = client.post('/predict', data=data, content_type='multipart/form-data')

        # Check if the response is valid
        assert response.status_code == 200
        assert b"genre" in response.data
