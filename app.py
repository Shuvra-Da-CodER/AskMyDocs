import streamlit as st
import streamlit.components.v1 as components
import uuid
from langchain.schema import Document
import fitz
from handlers.doc_handler import process_documents
from handlers.query_handler import run_query
from datetime import datetime

st.set_page_config(page_title="DocuSense", layout="wide")
GOOGLE_FORM_ACTION_URL="https://forms.gle/WDGr5iGPpLgffkJv8"
st.html(
    f"""
    <a href="{GOOGLE_FORM_ACTION_URL}" target="_blank">
        <button style="position:fixed; top:70px; right:20px; padding:8px 16px; background-color:#007BFF; color:white; border:none; border-radius:5px; cursor:pointer;">
            Give Feedback
        </button>
    </a>
    """
)


st.title("📝 DocuSense : Question Your PDFs ")


# Initialize session state
if "namespace" not in st.session_state:
    st.session_state.namespace = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []


# Sidebar UI
with st.sidebar:
    st.write("⏰ Previous Chats")
    for ns in st.session_state.chat_history:
        if st.button(f"Chat: {ns}"):
            chat = st.session_state.chat_history[ns]
            st.write(f"Docs used: {ns}")  # can map ns to doc list for more clarity
            #for turn in chat:
            st.write(f"🧑 {chat['user']}")
            st.write(f"🤖 {chat['bot']}")


# File uploader
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
# if st.button("🔄 Reset Upload"):
#     st.session_state.uploaded_docs = []
#     st.session_state.namespace = None
#     st.rerun()  # force Streamlit to reload

if len(uploaded_files)==0 and st.session_state.uploaded_docs:
    st.session_state.uploaded_docs = []
    st.session_state.namespace = None
    st.rerun()


if uploaded_files and not st.session_state.uploaded_docs:
    raw_text = ""
    filenames = []
    docs=[]
    print("RECEIVED")

    for file in uploaded_files:
        
        source_name = file.name 
        doc = fitz.open(stream=file.read(), filetype="pdf")
        print(source_name)
        filenames.append(file.name)
        print(filenames)
        text = ""
        for page in doc:
            text += page.get_text()   
        
        raw_text += text
        
       

    namespace = str(uuid.uuid4())
    st.session_state.chat_history[namespace] = []
    print(namespace)
    process_documents(raw_text, namespace)

    st.session_state.namespace = namespace
    st.session_state.uploaded_docs.extend(filenames)
    st.success("PDFs processed and indexed!")


# Ask a question
question = st.text_input("Ask a question about your documents")

if st.button("Submit") and question and uploaded_files:
    if st.session_state.namespace:
        #with st.spinner("🤖 Thinking..."):
        answer = run_query(question, st.session_state.namespace)
        st.session_state.chat_history[st.session_state.namespace].append({
            "user": question,
            "bot": answer
        })
        print('USER:',question)
        print('BOT:',answer)
    


# Scrollable chat UI with proper rendering
if st.session_state.namespace and st.session_state.namespace in st.session_state.chat_history:
    chat_html = f"""
    <div id='chat_container' style="height: 400px; overflow-y: scroll; padding-right: 8px; padding-left: 4px; background-color:#212121">
    """

    for msg in st.session_state.chat_history[st.session_state.namespace]:
        timestamp = datetime.now().strftime("%H:%M")
        chat_html += f"""
        <div style='background-color: #1f3b4d; color: #cce6ff; padding: 12px 16px; margin: 8px 0; border-radius: 12px; max-width: 75%; margin-left: auto; font-size: 16px; box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);'>
            🧑‍💬 {msg["user"]} <small style='float:right;'>{timestamp}</small>
        </div>
        <div style='background-color: #e0ffe0; color: #003300; padding: 12px 16px; margin: 8px 0; border-radius: 12px; max-width: 75%; margin-right: auto; font-size: 16px; box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);'>
            🤖 {msg["bot"]} <small style='float:right;'>{timestamp}</small>
        </div>
        """

    chat_html += """
    </div>
    <script>
        var container= document.getElementById('chat_container');
        if (container):
            container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
    </script>
    """
    st.html(chat_html)