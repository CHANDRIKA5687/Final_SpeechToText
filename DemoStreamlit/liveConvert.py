import streamlit as st

def main():
    st.title("Real-time Speech Recognition")

    # Embed the HTML file with speech recognition in an iframe
    st.markdown("<iframe id='speech-recognition-frame' src='speech_recognition.html' width='0' height='0'></iframe>", unsafe_allow_html=True)

    # Create a Streamlit text element to display the transcript
    transcript_text = st.empty()

    # Define a JavaScript function to handle messages from the iframe
    js_code = """
    <script>
        window.addEventListener('message', function(event) {
            const message = event.data;
            if (message && message.transcript) {
                const transcript = message.transcript;
                document.getElementById('transcript').innerText = transcript;
            }
        });
    </script>
    """

    # Inject the JavaScript code into the Streamlit app
    st.markdown(js_code, unsafe_allow_html=True)

    # Display the transcript received from the iframe
    st.subheader("Transcript:")
    transcript = st.empty()
    transcript.markdown("<div id='transcript'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
