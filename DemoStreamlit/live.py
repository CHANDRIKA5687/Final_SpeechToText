import streamlit as st
import threading
import speech_recognition as sr

# Function to continuously transcribe speech
def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.info("Please start speaking...")
        while getattr(threading.current_thread(), "do_run", True):
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                st.text(text)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                st.error("Error fetching results: {0}".format(e))

def main():
    st.title("Real-time Speech to Text Conversion")

    # Button to start speech recognition
    if st.button("Start Speaking"):
        st.info("Speech recognition started...")
        # Start a new thread for speech recognition
        thread = threading.Thread(target=transcribe_speech)
        thread.start()
        
        # Button to stop speech recognition
        if st.button("Stop"):
            # Set the flag to stop speech recognition
            thread.do_run = False

if __name__ == "__main__":
    main()
