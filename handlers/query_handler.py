from chains.query_chain import get_query_chain

def run_query(question: str, namespace: str) :
    chain = get_query_chain(namespace)
    return chain.invoke(question)
