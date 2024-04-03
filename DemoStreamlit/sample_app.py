import streamlit as st
import speech_recognition as sr

def live_transcription():
    st.write("Live Transcription")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak something...")
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)
        st.success("Transcription: " + text)
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError as e:
        st.error("Could not request results; {0}".format(e))

def file_transcription(audio_file):
    st.write("File Transcription")
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)
    with audio_data as source:
        audio_file = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_file)
        st.success("Transcription: " + text)
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError as e:
        st.error("Could not request results; {0}".format(e))

def main():
    st.title("Speech to Text Converter")

    transcription_mode = st.radio("Select transcription mode:", ("Live Transcription", "File Transcription"))

    if transcription_mode == "Live Transcription":
        live_transcription()
    else:
        audio_file = st.file_uploader("Upload an audio or video file", type=["mp3", "wav", "mp4"])
        if audio_file:
            file_transcription(audio_file)

if __name__ == "__main__":
    main()
