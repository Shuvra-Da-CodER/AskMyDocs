
---

# 📝AskMyDocs

AskMyDocs is an AI-powered tool that allows you to upload PDF documents and ask questions about their content using Retrieval-Augmented Generation (RAG). It extracts relevant information from your documents and provides clear answers via an intuitive interface.

---

## 🚀Features

* Upload one or more PDF files
* Automatically process and embed PDF contents for fast retrieval
* Ask questions in natural language about your PDFs
* Receive accurate answers generated with language models using document context
* Interactive and user-friendly Streamlit-based UI

---

## Installation

### Requirements

* Python 3.8+
* `pip`

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Shuvra-Da-CodER/AskMyDocs.git
   cd AskMyDocs
   ```

2. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the app with Streamlit:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`, upload PDFs, and start asking questions!

---

## Project Structure

* `app.py`: Main Streamlit application entry point
* `chains/`: Logic for handling document loading and querying
* `handlers/`: Modules to manage question answering and chat history
* `utils/`: Helper functions for document processing and vector management

---

## How It Works

1. PDFs are uploaded via the web interface.
2. Text is extracted and embedded into a vector store.
3. When you ask a question, the relevant document chunks are retrieved.
4. Answers are generated using a language model informed by the retrieved context.

---

## Contributing

Feel free to fork and submit pull requests. Please follow standard GitHub workflow for contributions.

---

## License

This project is licensed under the MIT License.

---

If you want me to add badges, screenshots, or any other sections (like FAQ or troubleshooting), just let me know!
