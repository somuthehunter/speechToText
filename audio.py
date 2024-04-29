import speech_recognition as sr
from pydub import AudioSegment
import os

#made by @somuthehunter(Pritam Dutta) @copyrights reserved 2024

def transcribe_audio_to_text(audio_file, chunk_duration=10000):
    recognizer = sr.Recognizer()
    text = ""

    try:
        audio = AudioSegment.from_file(audio_file)
    except FileNotFoundError:
        print(f"File '{audio_file}' not found.")
        return text
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return text

    # Determine the number of chunks based on the chunk duration
    num_chunks = len(audio) // chunk_duration + 1

    for i in range(num_chunks):
        start_time = i * chunk_duration
        end_time = min((i + 1) * chunk_duration, len(audio))
        chunk = audio[start_time:end_time]

        try:
            # Export the chunk to a temporary WAV file
            chunk.export("temp.wav", format="wav")

            # Recognize speech from the temporary WAV file
            with sr.AudioFile("temp.wav") as source:
                audio_data = recognizer.record(source)
                chunk_text = recognizer.recognize_google(audio_data, language="bn-IN")
                text += chunk_text + " "
                
                # Print progress message
                print(f"Processed chunk {i + 1}/{num_chunks}")
        except sr.UnknownValueError:
            print(f"Google Speech Recognition could not understand a chunk of audio at time {start_time}-{end_time}.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")

    return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

input_audio_file = input("Enter your file name: ")
output_text_file = input("Enter outputfile name : ")

output_text_file = f"Text/{output_text_file}"
chunk_duration = 30000  # Duration of each chunk in milliseconds (30 seconds)

# Check if the input audio file existsS
if not os.path.isfile(input_audio_file):
    print(f"Input audio file '{input_audio_file}' not found.")
else:
    transcribed_text = transcribe_audio_to_text(input_audio_file, chunk_duration)

    if transcribed_text:
        save_text_to_file(transcribed_text, output_text_file)
        print("Transcription saved to", output_text_file)
