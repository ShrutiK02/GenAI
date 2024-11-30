import whisper
import openai
from gtts import gTTS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid  # For generating unique filenames

load_dotenv()

# Load API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the Whisper model globally
model = whisper.load_model("base")

def transcribe_audio(audio_file):
    """
    Transcribes the given audio file into text using the Whisper model.
    Args:
        audio_file: The uploaded audio file from Flask's request.files.
    Returns:
        str: The transcribed text.
    """
    try:
        # Save audio to a temp directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(base_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        filename = secure_filename(audio_file.filename)
        temp_path = os.path.join(temp_dir, filename)
        audio_file.save(temp_path)

        # Use OpenAI's Whisper for transcription
        with open(temp_path, "rb") as file:                                                                                                      transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=file
            )
        return transcription["text"]
    except Exception as e:
        return f"Error during transcription: {str(e)}"

def get_reply(prompt):
    """
    Gets a chatbot reply for a given prompt using OpenAI's GPT model.
    Args:
        prompt (str): The user's query or message.
    Returns:
        str: The chatbot's reply.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{prompt}"}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error generating reply: {str(e)}"

def generate_tts(text, output_dir="static/audio"):
    """
    Converts text to speech using gTTS and saves the audio file.
    Args:
        text (str): The input text to convert to speech.
        output_dir (str): The directory to save the audio file.
    Returns:
        str: The path to the generated audio file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        filename = f"response_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(output_dir, filename)

        # Use gTTS to generate audio
        tts = gTTS(text=text, lang="en")
        tts.save(filepath)
        return filepath
    except Exception as e:
        return f"Error generating TTS: {str(e)}"

                                                   
