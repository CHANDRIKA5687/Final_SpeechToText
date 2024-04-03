import streamlit as st
import speech_recognition as sr
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to convert speech to text
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Function to generate PDF
def generate_pdf(text):
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    pdf_canvas.drawString(100, 750, text)
    pdf_canvas.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

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

            if st.button("Download PDF"):
                pdf_data = generate_pdf(text)
                st.download_button(
                    "Download PDF", pdf_data, file_name="transcript.pdf", mime="application/pdf"
                )

if __name__ == "__main__":
    main()
