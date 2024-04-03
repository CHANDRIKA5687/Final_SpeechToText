import streamlit as st
import speech_recognition as sr

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak something...")
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)
        st.write("Live Transcription Result:")
        st.write(text)
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError as e:
        st.error("Could not request results; {0}".format(e))

def main():
    st.title("Speech to Text Converter")

    option = st.radio("Select transcription option:", ("Upload File", "Live Transcription"))

    if option == "Upload File":
        file_type = st.radio("Select file type:", ("Audio", "Video"))

        if file_type == "Audio":
            file_uploader_label = "Upload an audio file"
            file_types = ["mp3", "wav"]
        else:
            file_uploader_label = "Upload a video file"
            file_types = ["mp4"]

        audio_file = st.file_uploader(file_uploader_label, type=file_types)

        if audio_file:
            st.audio(audio_file, format="audio/wav")

            if st.button("Transcribe"):
                # Add transcription code here
                pass

    elif option == "Live Transcription":
        speech_to_text()

if __name__ == "__main__":
    main()
