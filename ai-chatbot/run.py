from flask import Flask, request, jsonify, send_from_directory, send_file
from intent_recognizer import IntentRecognizer
import random
import os

# Set the Google Cloud Text-to-Speech credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"YOUR GOOGLE CLOUD .json file path"

app = Flask(__name__, static_folder='static')
intent_recognizer = IntentRecognizer()

@app.route('/')
def serve_index():
    return send_from_directory(directory='.', path='index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    category = data.get('category', '')

    # Handle request using IntentRecognizer
    response_data = intent_recognizer.handle_request(message, category)

    return jsonify({
        'response': response_data['text'],
        'audio': response_data['audio'],
        'showForm': response_data.get('showForm', '')
    })

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_file(f'static/{filename}')

@app.route('/appointment', methods=['POST'])
def book_appointment():
    user_data = request.json
    doctor_name = user_data.get('doctor', 'Unknown Doctor')

    # Generate a reference number
    reference_number = f"{random.randint(1000, 9999)}"

    # Add reference number to user data
    user_data['reference_number'] = reference_number

    # Insert appointment data into MongoDB
    intent_recognizer.db.appointments.insert_one(user_data)

    # Create response
    response = f"Appointment booked successfully with {doctor_name}. Your reference number is {reference_number}."
    audio_response = intent_recognizer.text_to_speech(response)

    return jsonify({'response': response, 'audio': audio_response})

if __name__ == '__main__':
    app.run(debug=True)

