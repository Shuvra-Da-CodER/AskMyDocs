from chains.doc_chain import get_document_chain

def process_documents(text, namespace: str):
    chain = get_document_chain(namespace)
    chain.invoke(text)
