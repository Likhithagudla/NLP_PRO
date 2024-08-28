from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route("/voice", methods=['POST'])
def voice():
    """Respond to incoming phone calls."""
    response = VoiceResponse()
    response.say("Hello! Please speak after the beep.", voice='alice')
    response.record(timeout=10, transcribe=True, transcribe_callback='/transcription')
    return str(response)

@app.route("/transcription", methods=['POST'])
def transcription():
    """Handle transcribed text from the call and translate."""
    transcribed_text = request.form['TranscriptionText']
    from_language = 'en'  # You can dynamically set this based on user settings
    to_language = 'es'    # You can dynamically set this based on user settings

    # Translate the text
    translated_text = translator.translate(transcribed_text, src=from_language, dest=to_language).text

    # Respond with translated text
    response = VoiceResponse()
    response.say(f"Translation: {translated_text}", voice='alice')
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
