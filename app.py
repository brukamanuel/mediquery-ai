import streamlit as st
import os
import html

from src.search_engine import search_answer


st.set_page_config(
    page_title="MediQuery AI",
    page_icon="🩺",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
    }

    .block-container {
        max-width: 900px;
        padding-top: 35px;
    }

    .title {
        text-align: center;
        color: white;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 17px;
        margin-bottom: 24px;
    }

    .chat-card {
        background-color: white;
        color: #111827;
        padding: 18px 22px;
        border-radius: 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        line-height: 1.7;
        font-size: 16px;
        width: 85%;
        word-wrap: break-word;
    }

    .user-card {
        margin-left: auto;
        border-top-right-radius: 5px;
    }

    .bot-card {
        margin-right: auto;
        border-top-left-radius: 5px;
    }

    .label {
        font-size: 13px;
        color: #cbd5e1;
        margin-bottom: 4px;
        font-weight: 600;
    }

    .source-text {
        font-size: 12px;
        color: #64748b;
        margin-top: 14px;
    }

    .recommendation-box {
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 10px;
        margin-top: 14px;
        font-size: 13px;
        color: #475569;
    }

    .recommendation-title {
        font-weight: 700;
        margin-bottom: 5px;
        color: #334155;
    }

    div[data-testid="stTextInput"] input {
        background-color: white !important;
        color: #111827 !important;
        border-radius: 14px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 14px !important;
        font-size: 16px !important;
    }

    div.stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border-radius: 14px;
        border: none;
        padding: 12px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 14px;
        border: none;
    }

    @media (max-width: 768px) {
        .chat-card {
            width: 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title">MediQuery AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Intelligent Medical Assistant<br><i>Your everyday AI medical research companion.</i></div>',
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    if message["role"] == "user":
        safe_text = html.escape(message["content"])

        st.markdown(
            f"""
            <div class="label">You</div>
            <div class="chat-card user-card">{safe_text}</div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="label">MediQuery</div>
            <div class="chat-card bot-card">{message["content"]}</div>
            """,
            unsafe_allow_html=True
        )


with st.form("chat_form", clear_on_submit=True):

    question = st.text_input(
        "Medical Question",
        placeholder="Example: What are symptoms of diabetes?"
    )

    submitted = st.form_submit_button("Send")


col1, col2 = st.columns([1, 1])

with col2:

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


if submitted and question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.spinner("Analyzing medical documents..."):
        answer, score, source, recommendations = search_answer(question)

    safe_answer = html.escape(answer)

    if source is None:

        bot_response = (
            f"{safe_answer}"
            f"<div class='source-text'>Match score: {round(score, 3)}</div>"
        )

    else:

        unique_sources = []

        for item in recommendations:

            if item["source"] not in unique_sources:
                unique_sources.append(item["source"])

        recommendation_html = ""

        if unique_sources:

            recommendation_html = (
                "<div class='recommendation-box'>"
                "<div class='recommendation-title'>Related passages</div>"
            )

            for source_name in unique_sources[:3]:

                recommendation_html += f"<div>{html.escape(source_name)}</div>"

            recommendation_html += "</div>"

        bot_response = (
            f"{safe_answer}"
            f"<div class='source-text'>Source: {html.escape(source)} · Match score: {round(score, 3)}</div>"
            f"{recommendation_html}"
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )

    st.rerun()


with st.expander("How MediQuery AI Works"):

    st.markdown(
        """
        **1. PDF Text Extraction**  
        Medical PDF files are read using PyMuPDF and converted into raw text.

        **2. Text Chunking**  
        The extracted text is divided into smaller passages. This helps the system search more accurately instead of comparing the question with an entire long document.

        **3. TF-IDF Vectorization**  
        Each text passage is converted into numerical form using TF-IDF. This gives higher importance to meaningful terms and lower importance to very common words.

        **4. Cosine Similarity**  
        The user question is converted into the same vector format and compared with all document passages using cosine similarity.

        **5. Answer Extraction**  
        The system selects the most relevant sentence from the best matching passage.

        **6. Source Tracking**  
        The response includes the source PDF and a match score showing how close the retrieved passage was to the user question.
        """
    )


with st.expander("Document Upload"):

    upload_folder = "data/medical_pdfs"

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        saved_filenames = []

        for uploaded_file in uploaded_files:

            save_path = os.path.join(upload_folder, uploaded_file.name)

            saved_filenames.append(html.escape(uploaded_file.name))

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        st.success(
            "PDF files saved successfully. Refresh or restart the app to include them in search."
        )

        st.markdown(
            "Saved files: " + ", ".join(saved_filenames)
        )