import streamlit as st
from deep_translator import GoogleTranslator

st.title("Translator")
st.write("Write your text to translate")

lang = {
    "English" : "en",
    "العربيه" : "ar",
    "French" : "fr",
    "italian" : "it",
    "spanish" : "es"
}

col1 , col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source Language", list(lang.keys()), index=1)
with col2:
    target_lang = st.selectbox("Target Language", list(lang.keys()), index=0)

text_input = st.text_area("Enter your text", height=150, placeholder="Write your text...")

if st.button("Translate",use_container_width=True):
    if text_input == "":
        st.warning("Enter your text first...")
    else:
        try:
            translated = GoogleTranslator(source=lang[source_lang], target=lang[target_lang]).translate(text_input)
            st.text_area("Translated text", value=translated, height=100)
        except:
            st.error("There is an error for connection please try again...")

st.markdown("---")
st.caption("Streamlit | Deep_Translator")
