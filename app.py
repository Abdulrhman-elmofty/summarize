import streamlit as st
from groq import Groq
import PyPDF2
import io


st.title("Summarize")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


uploaded_file = st.file_uploader(
    "Or upload a PDF file",
    type=["pdf"]
)

text_from_pdf = ""

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(
        io.BytesIO(uploaded_file.read())
    )

    pdf_text = ""

    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""

    if pdf_text.strip():
        st.info(
            f"Text extracted from PDF ({len(pdf_reader.pages)} pages)"
        )
        text_from_pdf = pdf_text
    else:
        st.warning("No text was found in the file")


text = st.text_area(
    "Write your text here...",
    height=200,
    value=text_from_pdf
)


if st.button("Summarize!"):
    if len(text.split()) < 10:
        st.warning("The text is too short!")
    else:
        with st.spinner("Summarizing..."):

            # Detect language
            arabic_letters = sum(
                1
                for c in text
                if "\u0600" <= c <= "\u06FF"
            )

            language = (
                "Arabic"
                if arabic_letters > 5
                else "English"
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are a helpful assistant for kids. "
                            f"Summarize the text in 3-4 simple sentences. "
                            f"You MUST respond in {language} only. "
                            f"Do NOT use any other language."
                        ),
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
            )

            summary = response.choices[0].message.content

            st.success(summary)
