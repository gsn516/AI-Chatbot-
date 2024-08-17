import spacy
import random
from google.cloud import texttospeech
from pymongo import MongoClient, errors
import os
from data import get_lab_result, get_prescription, get_billing

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"YOUR GOOGLE CLOUD .json file path"

class IntentRecognizer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.intents = {
            'greeting': ['hello', 'hi', 'hey'],
            'appointment': ['appointment', 'book', 'schedule'],
            'doctors': ['doctor', 'specialist'],
            'lab_results': ['lab results', 'test results'],
            'prescription': ['prescription', 'medication'],
            'billing': ['billing', 'invoice', 'charges'],
            'visiting_hours': ['visiting hours', 'hospital hours'],
            'emergency': ['emergency', 'urgent'],
            'other': ['other', 'issue']
        }
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['hospital2']
        self.text_to_speech_client = texttospeech.TextToSpeechClient()
        self.response_map = {
            'doctors': self.get_doctors,
            'appointment': self.book_appointment,
            'lab_results': self.get_lab_results,
            'prescription': self.get_prescription,
            'billing': self.get_billing,
            'visiting_hours': self.get_visiting_hours,
            'emergency': self.get_emergency,
            'other': self.handle_other,
            'greeting': self.handle_greeting
        }
        self.ensure_doctors_exist()

    def recognize_intent(self, text):
        doc = self.nlp(text.lower())
        for token in doc:
            for intent, keywords in self.intents.items():
                if token.text in keywords:
                    return intent
        return 'other'

    def handle_greeting(self):
        return 'Hi, how can I assist you?'

    def get_response(self, text):
        intent = self.recognize_intent(text)
        if intent in self.response_map:
            return self.response_map[intent]()
        else:
            return 'I am not sure how to help with that.'

    def handle_request(self, message, category):
        if category in ['appointment', 'reference']:
            return {'text': "How can I assist you with your appointment or reference?", 'audio': 'response.mp3', 'showForm': category}
        
        if message.lower() in ['hi', 'hello', 'hey', 'kalyan']:
            text_response = "Hello! How can I assist you today?"
            audio_response = self.text_to_speech(text_response)
            return {'text': text_response, 'audio': audio_response, 'showForm': ''}
        
        if category in self.response_map:
            text_response = self.response_map[category](category, message)
            audio_response = self.text_to_speech(text_response)
            return {'text': text_response, 'audio': audio_response, 'showForm': ''}
        
        return {'text': "I'm sorry, I don't understand that request.", 'audio': 'error.mp3', 'showForm': ''}

    def text_to_speech(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = self.text_to_speech_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        audio_file = f"static/response_{random.randint(1000, 9999)}.mp3"
        with open(audio_file, "wb") as out:
            out.write(response.audio_content)
        return audio_file

    def ensure_doctors_exist(self):
        # Clear the collection to avoid duplicates
        self.db.doctors.delete_many({})
        
        # Add new doctors
        doctors = [
            {"name": "Dr. John Doe", "specialization": "Cardiologist, Time slot 9AM"},
            {"name": "Dr. Jane Smith", "specialization": "Neurologist, Time slot 9:15AM"},
            {"name": "Dr. Emily Davis", "specialization": "Orthopedic, Time slot 9:30AM"},
            {"name": "Dr. Michael Brown", "specialization": "Pediatrician, Time slot 9:45AM"},
            {"name": "Dr. Sarah Johnson", "specialization": "Dermatologist, Time slot 10:00AM"}
        ]
        self.db.doctors.insert_many(doctors)

    def get_doctors(self, category, message):
        doctors = self.db.doctors.find()
        response = "Here are the doctors:\n"
        for doctor in doctors:
            response += f"{doctor['name']} - {doctor['specialization']}\n"
        return response

    def book_appointment(self, category, message):
        # Extract doctor name from the message
        doctor_name = self.extract_doctor_name(message)
        
        if not doctor_name:
            doctor_name = "Unknown Doctor"
        
        reference_number = random.randint(1000, 9999)
        return f"Appointment booked successfully with {doctor_name}. Your reference number is {reference_number}."

    def get_lab_results(self, category, message):
        reference_number = self.extract_reference_number(message)
        return get_lab_result(reference_number)

    def get_prescription(self, category, message):
        reference_number = self.extract_reference_number(message)
        return get_prescription(reference_number)

    def get_billing(self, category, message):
        reference_number = self.extract_reference_number(message)
        return get_billing(reference_number)

    def get_visiting_hours(self, category, message):
        return "Visiting hours are Morning 9AM to Evening 5PM."

    def get_emergency(self, category, message):
        return "Please immediately call 112."

    def handle_other(self, category, message):
        return "If you forget your reference number or have any questions, please call us at +91 1234567890."

    def extract_reference_number(self, message):
        doc = self.nlp(message)
        for token in doc:
            if token.like_num:
                return token.text
        return ""

    def extract_doctor_name(self, message):
        doc = self.nlp(message)
        doctor_names = [doctor['name'] for doctor in self.db.doctors.find()]
        for token in doc:
            if token.text in doctor_names:
                return token.text
        return ""


