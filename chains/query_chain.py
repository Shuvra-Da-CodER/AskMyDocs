from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from utils.pinecone_utils import embed_query, query_pinecone
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

prompt = PromptTemplate.from_template("""
You are a helpful assistant
If the user greets you (e.g., says "hi", "hello","how are you",etc), just greet them 
warmly and in a polite way like you are their brother.
HOWEVER NO NEED TO GREET THEM MUCH, ONLY do so IF THEY GREET YOU
                                      
ONLY Use the following context to answer the question:

{context}

Question: {question}
                                      
Chat history:-
{chat_history}                                     

If you don''t know the ans just tell that the provided text doesnt give any such information
""")

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
parser=StrOutputParser()

def get_query_chain(namespace: str):
    embed = RunnableLambda(embed_query)
    retrieve = RunnableLambda(lambda vector: query_pinecone(vector, namespace))
    format_ctx = RunnableLambda(lambda chunks: "\n".join(chunks))
    def debug_context(x):
        print(f"Context: {x}")
        return x
    def get_history(_):
        history_list = st.session_state.get("chat_history", {}).get(namespace, [])
        return "\n".join([
            f"User: {m['user']}\nBot: {m['bot']}" 
            for m in history_list
        ])
    history=RunnableLambda(get_history)
    debug_context_lambda = RunnableLambda(debug_context)
    parallel = RunnableParallel({
        "question": RunnablePassthrough(),
        "context": embed | retrieve | format_ctx | debug_context_lambda,
        "chat_history":history
    })

    return parallel | prompt | llm | parser
