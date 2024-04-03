import streamlit as st
import speech_recognition as sr
from io import BytesIO
from docx import Document

# Function to convert speech to text
# Function to convert speech to text
def speech_to_text(audio_file, timeout=60):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, show_all=False)
        except sr.WaitTimeoutError:
            st.error("Speech recognition timed out. Please try again.")
            return ""
    return text

# Function to generate Word document
def generate_word_document(text):
    doc = Document()
    doc.add_paragraph(text)
    return doc

def main():
    st.title("Speech to Text Converter")

    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if audio_file:
        st.audio(audio_file, format="audio/wav")

        if st.button("Transcribe"):
            text = speech_to_text(audio_file)
            st.text_area("Transcribed Text", value=text, height=200)

            if st.button("Edit"):
                edited_text = st.text_area("Edit Text", value=text, height=200)
                text = edited_text

            if st.button("Download Word Document"):
                doc = generate_word_document(text)
                doc_io = BytesIO()
                doc.save(doc_io)
                doc_io.seek(0)
                st.download_button(
                    label="Download Word Document", data=doc_io, file_name="transcription.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

if __name__ == "__main__":
    main()
