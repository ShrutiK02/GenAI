from flask import Flask, render_template, request, jsonify, send_file
from utils import transcribe_audio, get_reply, generate_tts
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        audio_file = request.files["audio"]
        transcription = transcribe_audio(audio_file)
        if transcription.startswith("Error"):
            return jsonify({"error": transcription}), 400

        reply = get_reply(transcription)
        tts_audio_path = generate_tts(reply)

        return jsonify({
            "transcription": transcription,
            "reply": reply,
            "audio_url": f"/audio/{os.path.basename(tts_audio_path)}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/audio/<filename>")
def audio(filename):
    try:
        return send_file(f"./static/audio/{filename}")
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True)
