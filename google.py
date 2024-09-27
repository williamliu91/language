import streamlit as st
from gtts import gTTS
from googletrans import Translator
import base64

# Function to create speech from text
def create_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("speech.mp3")  # Save the audio file

# Function to get the base64 encoded audio file
def get_base64_encoded_audio(audio_file):
    with open(audio_file, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")
    return audio_base64

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background-color: #f0f4f8;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        color: #4a4a4a;
    }
    .button {
        background-color: #4CAF50; 
        color: white; 
        padding: 10px 20px; 
        border: none; 
        border-radius: 5px; 
        cursor: pointer;
        font-size: 16px;
    }
    .button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit app title and description
st.title("🌐 Multilingual Text-to-Speech App")
st.write("Type your text in English, choose a language, and listen to the translation!")

# Initialize the translator
translator = Translator()

# Sidebar for input and settings
st.sidebar.header("Input Section")
user_input = st.sidebar.text_input("Type something in English:")
language_options = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Chinese (Mandarin)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
}
language = st.sidebar.selectbox("Select language to translate to:", list(language_options.keys()))

# Initialize session state for translated text if it doesn't exist
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""

# Button to translate text
if st.sidebar.button("Translate"):
    if user_input:
        # Translate the user input to the selected language
        translated_text = translator.translate(user_input, dest=language_options[language]).text
        
        # Store translated text in session state
        st.session_state.translated_text = translated_text
        
        # Display translated text once after translation
        st.success(f"Translated Text: {translated_text}")
        
    else:
        st.warning("Please enter some text to translate!")

# Button to speak the translated text
if st.sidebar.button("Speak"):
    if st.session_state.translated_text:
        create_speech(st.session_state.translated_text, language_options[language])  # Create speech for the translated text
        
        # Get the base64 encoded audio file
        audio_base64 = get_base64_encoded_audio("speech.mp3")
        
        # Embed the audio using HTML and Streamlit's components
        st.markdown(
            f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Please translate some text first!")

# Optional: Add some instructions at the bottom
st.write("### Instructions:")
st.write("1. Type something in English.")
st.write("2. Select a language from the dropdown.")
st.write("3. Click 'Translate' to see the translation.")
st.write("4. Click 'Speak' to hear the translation!")