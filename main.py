import streamlit as st
from app.utils.extractor import extract_text_from_pdf, extract_text_from_image
from app.utils.embed_store import add_text_to_chroma
from app.utils.qa_engine import query_documents
from app.utils.theme_identifier import identify_themes

#Streamlit page
st.set_page_config(page_title="Document Theme Chatbot", layout="wide")
st.title(" Document Research & Theme Identifier")

# Upload PDF/image documents
uploaded_files = st.file_uploader(
    "Upload PDF or scanned image documents (multiple files allowed)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

    all_doc_names = []

    for file in uploaded_files:
        st.write("📄", file.name)
        file_bytes = file.read()
        st.write(f"File type: {file.type}")

        # Extract text from file
        if file.type == "application/pdf":
            text = extract_text_from_pdf(file_bytes)
        else:
            text = extract_text_from_image(file_bytes)

        st.write(f"Extracted text length: {len(text)} characters")

        if text.strip():
            # Show preview and embed into ChromaDB
            st.text_area(f"Extracted Text Preview - {file.name}", value=text[:500], height=150)

            with st.spinner("Embedding and storing..."):
                chunks_added = add_text_to_chroma(file.name, text)
                st.success(f"{chunks_added} chunks embedded from {file.name}")
        else:
            st.warning("No text extracted from this file.")

        all_doc_names.append(file.name)

    # Document selection UI
    st.divider()
    st.subheader(" Select Documents to Use in Research")

    selected_docs = st.multiselect(
        "Choose one or more documents to include in question answering and theme identification:",
        options=all_doc_names,
        default=all_doc_names
    )

    if selected_docs:
        # Q&A section
        st.divider()
        st.subheader(" Ask a Question About Your Uploaded Documents")

        user_query = st.text_input("Type your question below")

        if user_query:
            with st.spinner("Searching and generating answer..."):
                answer, sources = query_documents(user_query)
                st.markdown(" Answer")
                st.write(answer)

                st.markdown(" Sources Referenced")
                for src in sources:
                    st.markdown(f"- `{src}`")

            # Theme synthesis
            st.divider()
            if st.button("Identify Themes Across All Documents"):
                with st.spinner("Synthesizing themes..."):
                    answers_dict = {}

                    for file in uploaded_files:
                        if file.name in selected_docs:
                            answer, _ = query_documents(user_query)
                            answers_dict[file.name] = answer

                    summary = identify_themes(answers_dict)
                    st.markdown("###  Synthesized Themes")
                    st.write(summary)
    else:
        st.warning(" Please select at least one document to continue.")
else:
    st.info("Please upload at least one document to begin.")
