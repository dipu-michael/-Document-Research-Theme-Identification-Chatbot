import streamlit as st
from app.utils.extractor import extract_text_from_pdf, extract_text_from_image
from app.utils.embed_store import add_text_to_chroma
from app.utils.qa_engine import query_documents
from app.utils.theme_identifier import identify_themes

st.set_page_config(page_title="Document Theme Chatbot", layout="wide")
st.title("📚 Wasserstoff AI Intern Task: Document Research & Theme Identifier")

# Initialize session state to store text and embedding status
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = {}

if "embedded_docs" not in st.session_state:
    st.session_state.embedded_docs = set()

uploaded_files = st.file_uploader(
    "Upload PDF or scanned image documents (multiple files allowed)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

    all_doc_names = []

    for file in uploaded_files:
        file_bytes = file.read()
        all_doc_names.append(file.name)

        # Only process file once
        if file.name not in st.session_state.processed_docs:
            st.write(f"📄 Extracting from {file.name}...")
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file_bytes)
            else:
                text = extract_text_from_image(file_bytes)

            st.session_state.processed_docs[file.name] = text.strip()
        else:
            text = st.session_state.processed_docs[file.name]

        # Show extracted text preview
        st.text_area(f"📝 Extracted Text - {file.name}", value=text[:500], height=150)

    st.divider()
    st.subheader("📑 Select Documents to Work With")

    selected_docs = st.multiselect(
        "Choose documents for embedding and theme analysis:",
        options=all_doc_names,
        default=all_doc_names
    )

    # Embed button
    if st.button("🔁 Embed Selected Documents into Vector DB"):
        with st.spinner("Embedding and storing..."):
            for name in selected_docs:
                if name not in st.session_state.embedded_docs:
                    chunks = add_text_to_chroma(name, st.session_state.processed_docs[name])
                    st.success(f"✅ {chunks} chunks embedded from {name}")
                    st.session_state.embedded_docs.add(name)
                else:
                    st.info(f"🔒 {name} already embedded.")

    # Q&A section
    st.divider()
    st.subheader("🔍 Ask a Question")

    user_query = st.text_input("Type your question here")

    if user_query:
        with st.spinner("Searching and answering..."):
            answer, sources = query_documents(user_query)
            st.markdown("### 💬 Answer")
            st.write(answer)

            st.markdown("### 📄 Sources")
            for src in sources:
                st.markdown(f"- `{src}`")

    # Theme synthesis
    st.divider()
    if st.button("🧠 Identify Common Themes Across Selected Documents"):
        with st.spinner("Synthesizing themes..."):
            answers_dict = {}
            for name in selected_docs:
                answer, _ = query_documents(f"What is the main idea in {name}?")
                answers_dict[name] = answer

            summary = identify_themes(answers_dict)
            st.markdown("### 🧵 Synthesized Themes")
            st.write(summary)
else:
    st.info("Please upload at least one document to begin.")
