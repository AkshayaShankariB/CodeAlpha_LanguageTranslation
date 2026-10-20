"""CodeAlpha AI Internship - Task 1: Language Translation Tool

Run with:  streamlit run app.py
"""
import io
import os

os.environ["translators_default_region"] = "EN"  # skips a slow region check on import

import streamlit as st
import translators as ts
from deep_translator import GoogleTranslator  # only used for the language list
from gtts import gTTS

st.set_page_config(page_title="Language Translator", page_icon="🌐")
st.title("🌐 Language Translation Tool")
st.caption("Type some text, pick the languages, and translate.")


@st.cache_data
def get_languages():
    """Returns {'english': 'en', 'hindi': 'hi', ...}"""
    return GoogleTranslator().get_supported_languages(as_dict=True)


languages = get_languages()
names = sorted(languages.keys())

col1, col2 = st.columns(2)
with col1:
    source_name = st.selectbox("From", ["auto detect"] + names)
with col2:
    target_name = st.selectbox("To", names, index=names.index("spanish"))

text = st.text_area("Enter text", height=150, placeholder="Type or paste text here...")
read_aloud = st.checkbox("🔊 Read the translation aloud")

if st.button("Translate", type="primary"):
    if not text.strip():
        st.warning("Please enter some text first.")
    elif len(text) > 5000:
        st.warning("Text is too long (max 5000 characters).")
    else:
        source_code = "auto" if source_name == "auto detect" else languages[source_name]
        target_code = languages[target_name]
        try:
            with st.spinner("Translating..."):
                # Translation engine: Bing (change to "google" to try Google instead)
                result = ts.translate_text(
                    text, translator="bing",
                    from_language=source_code, to_language=target_code,
                )

            st.subheader(f"Translation ({target_name.title()})")
            # st.code shows a built-in copy button in the top-right corner
            st.code(result, language=None, wrap_lines=True)

            if read_aloud:
                try:
                    audio = io.BytesIO()
                    gTTS(text=result, lang=target_code).write_to_fp(audio)
                    st.audio(audio.getvalue(), format="audio/mp3")
                except Exception:
                    st.info("Text-to-speech isn't available for this language.")
        except Exception as e:
            st.error(f"Translation failed. Check your internet connection and try again.\n\n{e}")