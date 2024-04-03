import streamlit as st
import speech_recognition as sr
from docx import Document
from fpdf import FPDF

def transcribe_audio(file_path):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data)
            return transcript
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def convert_to_word(text):
    doc = Document()
    doc.add_paragraph(text)
    return doc

def convert_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    return pdf

def main():
    st.title("Audio Transcription")
    file_path = st.file_uploader("Upload Audio File", type=['wav', 'flac', 'ogg', 'mp3'])

    if file_path:
        transcript = transcribe_audio(file_path)
        if transcript:
            st.subheader("Transcription Result:")
            st.write(transcript)

            if st.button("Convert to Word"):
                doc = convert_to_word(transcript)
                st.download_button(label="Download Word Document", data=doc.save, file_name="transcription.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            if st.button("Convert to PDF"):
                pdf = convert_to_pdf(transcript)
                st.download_button(label="Download PDF Document", data=pdf.output, file_name="transcription.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
