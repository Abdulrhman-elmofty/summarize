import streamlit as st
import PyPDF2
import io
from groq import Groq

st.title("Summarize")

client = Groq(api_key=st.secrets['Groq_Api_Key'])

files = st.file_uploader("upload your pdf", type=["pdf"]) 

if files is not None:
    pdf_reader=PyPDF2.PdfReader(io.BytesIO(files.read()))
    pdf_text = ""

    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""

    if pdf_text.strip():
        st.info(f"extracted from {len(pdf_reader.pages)} pages")
        text_from_pdf= pdf_text
    else:
        st.warning("Your PDF has no text!!")
        text_from_pdf = pdf_text
else:
    text_from_pdf = ""
text_area = st.text_area("Or paste your text here:", height=200, value=text_from_pdf)

if st.button("Summarize!"):
    if len(text_area.split()) < 10:
        st.warning("Your text is too short")
    else:
        with st.spinner("Summarizing..."):
            arabic_letters = sum(1 for c in text_area if '\u0600' <= c <= '\u06ff')
            lang = "Arabic" if arabic_letters > 10 else "English"
            response = client.chat.completions.create(
                model = "llama-3.3-70b-versalite",
                messages = [
                    {"role" : "system" , "content" : f"you are a helpful assistant, summarize the text into 4 simple sentences, in {lang} language"},
                    {"role" : "user" , "content" : text}
                ]
            )
            st.success(response.choices[0].message.content)
