# Voice agent example using Deepgram's SDK and Groq as LLM
# Import dependencies and set up the main function
import os
import wave

import numpy as np
import sounddevice as sd
import soundfile as sf

from pynput import keyboard
from deepgram import DeepgramClient
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Define function Push-to-talk recording
def record_on_spacebar(samplerate):
    print("Hold SPACEBAR to record...")

    recording = []
    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='float32')

    def on_press(key):
        try:
            if key == keyboard.Key.space:
                if not stream.active:
                    print("Recording...")
                    stream.start()
        except:
            pass

    def on_release(key):
        if key == keyboard.Key.space:
            print("Recording stopped.")
            stream.stop()
            return False  # Stop listener

    with stream:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            while listener.running:
                if stream.active:
                    data, _ = stream.read(1024)
                    recording.append(data)

    if len(recording) == 0:
        return None

    audio = np.concatenate(recording, axis=0)
    return audio

def main():
    try:
        print("\nInitializing demo (STATEFUL AI AGENT)...")
    
        # Initialize Deepgram client
        dg_client = DeepgramClient(
            api_key=os.environ.get("DEEPGRAM_API_KEY"),
        )

        # Initialize Groq client
        groq_client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        # Conversation memory
        conversation_history = [
            {"role": "system", "content": "You are a helpful and concise conversational voice assistant."}
        ]

        # Audio files
        input_path = "../input_audio/groq_request.wav"
        output_path = "../output_audio/groq_response.wav"

        # Audio settings
        samplerate = 16000

        while True:
            # ========================
            # STEP 1: Record from mic
            # ========================
            print("\n---> STEP 1: Recording...")
            audio = record_on_spacebar(samplerate)

            if audio is None:
                print("No audio captured, try again.")
                continue

            # Save to WAV
            sf.write(input_path, audio, samplerate)

            #==============================
            # STEP 2: Transcribe WAV (STT)
            #==============================
            print("---> STEP 2: Transcribing with Deepgram STT...")

            # Open the audio file and reate a transcription of the audio file
            with open(input_path, "rb") as file:
                transcription = dg_client.listen.v1.media.transcribe_file(
                    request=file.read(),
                    model="nova-3",
                    smart_format=True,
                )
            print("Speech-to-Text done!")

            groq_request = transcription.results.channels[0].alternatives[0].transcript.strip()

            print(f"Groq request: '{groq_request}'")

            # ===================================
            # STEP 3: Send request to LLM (Groq)
            # ===================================
            print("---> STEP 3: Requesting chat completion to Groq...")

            conversation_history.append({
                "role": "user",
                "content": groq_request
            })

            chat_completion = groq_client.chat.completions.create(
                messages=conversation_history,
                model="llama-3.3-70b-versatile",
            )

            groq_response = chat_completion.choices[0].message.content.strip()
            print(f"Groq response: '{groq_response}'")

            # Save assistant response to memory
            conversation_history.append({
                "role": "assistant",
                "content": groq_response
            })

            # =======================
            # STEP 4: Text to Speech
            # =======================
            print("---> STEP 4: Generating audio with Deepgram TTS...")

            response = dg_client.speak.v1.audio.generate(
                text=groq_response,
                model="aura-2-odysseus-en",
                encoding="linear16",
                sample_rate=16000
            )

            # Collect audio chunks
            audio_bytes = b"".join(response)

            sample_rate = 16000
            silence_duration = 0.5  # seconds

            # Generate silence (int16 = 2 bytes per sample) - This is to avoid to starting playing audio without any pause
            num_samples = int(sample_rate * silence_duration)
            silence = np.zeros(num_samples, dtype=np.int16)

            # Convert original audio to numpy
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

            # Add fade - This is to avoid "clicking" noise when adding silence
            audio_np = audio_np.astype(np.float32)

            fade_duration = 0.01  # 10 ms fade-in
            fade_samples = int(sample_rate * fade_duration)

            fade_in = np.linspace(0, 1, fade_samples)
            audio_np[:fade_samples] *= fade_in

            audio_np = audio_np.astype(np.int16)

            # Prepend silence
            audio_with_silence = np.concatenate([silence, audio_np])

            # Write WAV file
            with wave.open(output_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit = 2 bytes
                wf.setframerate(sample_rate)
                wf.writeframes(audio_with_silence.tobytes())

            print("Text-to-Speech done!")

            # ===================
            # STEP 5: Play audio
            # ===================
            print("---> STEP 5: Playing audio...")

            data, samplerate = sf.read(output_path)
            sd.play(data, samplerate)
            sd.wait()

            # Exit condition
            if groq_request.lower() in ["exit", "quit", "goodbye", "exit.", "quit.", "goodbye."]:
                print("Exiting conversation...")
                print("\nDemo complete!\n")
                break

    except Exception as e:
        print(f"Exception: {e}")
        return

if __name__ == "__main__":
    main()
