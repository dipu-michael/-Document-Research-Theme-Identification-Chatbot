# 📚 Wasserstoff AI Intern Task: Document Research & Theme Identification Chatbot

This project is a Streamlit-based AI chatbot that performs intelligent research across a large set of uploaded documents. It extracts content from PDFs and scanned images, stores them in a vector database, and answers user queries using GPT-4. It can also identify and summarize **common themes** across multiple documents.

---

## 🚀 Features

✅ Upload PDFs and scanned images  
✅ OCR for scanned files using Tesseract  
✅ GPT-4 Q&A on document content  
✅ Sources cited in answers  
✅ Vector search using ChromaDB  
✅ Theme identification across selected documents  
✅ Extra credit: Select/deselect specific files for querying  

---

## 🧠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **AI/LLM**: [OpenAI GPT-4](https://platform.openai.com/)  
- **Embedding**: `text-embedding-3-small`  
- **OCR**: `pytesseract`, `pdf2image`, `PyMuPDF`  
- **Vector DB**: [ChromaDB](https://www.trychroma.com/)  
- **Environment Management**: `dotenv`  
- **Language**: Python 3.10+

---

## 📂 Folder Structure

AiInternTask/
├── main.py # Streamlit app
├── .gitignore # Git exclusions
├── .env 
├── app/
│ └── utils/
│ ├── extractor.py # OCR + text extraction
│ ├── embed_store.py # ChromaDB embedding
│ ├── qa_engine.py # GPT-based Q&A
│ └── theme_identifier.py# Theme summarization
├── samples/          e
│   ├── doc1.pdf
│   ├── scan1.jpg
│   └── notice2.png


---

## ⚙️ Setup Instructions

### 1. Clone the Repo

git clone https://github.com/dipu-michael/wasserstoff.git
cd wasserstoff


