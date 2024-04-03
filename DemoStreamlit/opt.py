import streamlit as st
import speech_recognition as sr
from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from moviepy.editor import VideoFileClip
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os
import tempfile

# Function to convert speech to text
def speech_to_text(_audio_data, timeout=60):
    recognizer = sr.Recognizer()
    with _audio_data as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            st.error("Speech recognition timed out. Please try again.")
            return ""
        except sr.UnknownValueError:
            st.error("Could not understand audio. Please try again with a different audio file.")
            return ""
    return text

# Function to convert video to audio
@st.cache_data()
def extract_audio(video_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(video_file.read())
        temp_file_path = temp_file.name

    video = VideoFileClip(temp_file_path)
    audio_file_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_file_path)
    
    # Close the audio file to ensure it's fully written and closed
    video.close()

    # Delete the temporary video file
    os.unlink(temp_file_path)

    return audio_file_path

# Function to generate Word document
@st.cache_data()
def generate_word_document(text):
    doc = Document()
    doc.add_paragraph(text)
    return doc

# Function to generate PDF document
@st.cache_data()
def generate_pdf_document(text):
    pdf_io = BytesIO()
    doc = SimpleDocTemplate(pdf_io, pagesize=letter)
    content = [Paragraph(text, doc.defaultTextStyle)]
    doc.build(content)
    return pdf_io

def main():
    st.title("Speech to Text Converter")

    file_type = st.radio("Select file type:", ("Audio", "Video"))

    if file_type == "Audio":
        file_uploader_label = "Upload an audio file"
        file_types = ["mp3", "wav"]
    else:
        file_uploader_label = "Upload a video file"
        file_types = ["mp4"]

    audio_file = st.file_uploader(file_uploader_label, type=file_types)

    if audio_file:
        if file_type == "Audio":
            st.audio(audio_file, format="audio/wav")
            audio_file_path = audio_file
        else:
            st.video(audio_file, format="video/mp4", start_time=0)
            audio_file_path = extract_audio(audio_file)

        if st.button("Transcribe"):
            audio_data = sr.AudioFile(audio_file_path)
            text = speech_to_text(audio_data)
            st.text_area("Transcribed Text", value=text, height=200)

            if st.button("Download Word Document"):
                doc = generate_word_document(text)
                doc_io = BytesIO()
                doc.save(doc_io)
                doc_io.seek(0)
                st.download_button(
                    label="Download Word Document", data=doc_io.getvalue(), file_name="transcription.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            if st.button("Download PDF Document"):
                pdf_io = generate_pdf_document(text)
                pdf_io.seek(0)
                st.download_button(
                    label="Download PDF Document", data=pdf_io.getvalue(), file_name="transcription.pdf", mime="application/pdf"
                )

if __name__ == "__main__":
    main()
