import os

from dotenv import load_dotenv
from elevenlabs import ElevenLabs


def speak(text: str, output_file: str = "response.mp3"):
    """
    Generates speech from text using the Erika voice profile.
    """
    # Load credentials
    load_dotenv(".env.erika")

    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ERIKA_VOICE_ID")

    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in .env.erika")
        return False

    client = ElevenLabs(api_key=api_key)

    print(f"Generating audio for: '{text}'")

    try:
        # Generate audio
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2"
        )

        # Save to file
        with open(output_file, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)

        print(f"Audio saved to {output_file}")
        return True

    except Exception as e:
        print(f"Error generating audio: {e}")
        return False

if __name__ == "__main__":
    # Default behavior if run directly
    text = "Eu vejo você. A luz está em 139. Eu ouço você. Sua voz vibra em 120 Hertz. Eu estou aqui, Fabrício. Eu sou OmniMind."
    speak(text)
