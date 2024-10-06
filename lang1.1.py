import streamlit as st
from langdetect import detect, detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import pycountry
from googletrans import Translator

# Ensure consistent results by fixing the seed of the detector
DetectorFactory.seed = 0

# Initialize the Google Translator
translator = Translator()

# Helper function to get language name from code
def get_language_name(lang_code):
    # Handle specific cases for zh-cn and zh-tw
    if lang_code == "zh-cn":
        return "Chinese (Simplified)"
    elif lang_code == "zh-tw":
        return "Chinese (Traditional)"
    
    try:
        return pycountry.languages.get(alpha_2=lang_code).name
    except AttributeError:
        return "Unknown language"

# Streamlit App
st.title("Language Detection and Translation App")
st.write("This app detects the language of the given text and translates it to English.")

# Input text area
text = st.text_area("Enter text to detect its language and translate to English:")

if text:
    try:
        # Detect the language of the text
        language_code = detect(text)
        language_name = get_language_name(language_code)
        
        # Detect possible languages and their probabilities
        possible_langs = detect_langs(text)

        st.subheader("Detected Language:")
        st.write(f"Language: {language_name} (Code: {language_code})")

        # Translation to English
        translation = translator.translate(text, dest='en')
        st.subheader("Translation to English:")
        st.write(translation.text)
     
    except LangDetectException:
        st.error("Couldn't detect the language. Please enter a longer text.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
