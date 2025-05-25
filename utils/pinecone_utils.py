from pinecone import Pinecone
from dotenv import load_dotenv
import os
load_dotenv()  # Load .env variables

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
index_name='pdf-rag'
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(index_name)

def embed_texts_to_pinecone(data, namespace):
    embeddings = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[d['text'] for d in data],
        parameters={"input_type": "passage", "truncate": "END"}
    )
    

    vectors = []
    for d, e in zip(data, embeddings):
        vectors.append({
            "id": d['id'],
            "values": e['values'],
            "metadata": {'text': d['text']}
        })

    index.upsert(
        vectors=vectors,
        namespace=namespace
    )

def embed_query(query):
    result = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    print(result[0]['values'])
    return result[0]["values"]

def query_pinecone(vector, namespace):
    print('Namespace:',namespace)
    res = index.query(
        vector=vector,
        namespace=namespace,
        top_k=3,
        include_metadata=True,
        include_values=False
    )
    print('Retrieved:-',[match["metadata"]["text"] for match in res["matches"]])
    return [match["metadata"]["text"] for match in res["matches"]]

#6d5b1c4d-085f-4fd6-974d-8a520eca1b12
#6d5b1c4d-085f-4fd6-974d-8a520eca1b12
'''
    PROBLEMS:-
2. In chat history, on clicking on a particular chat it should give me the details of the doc submitted
and the entire chat between user and bot in the main area not in the sidebar
5. Add a feedback area, where users can leave recommendations
6. FOR large pdfs use different embedding techniques
6.I want a login system, in which on logging in a person can see the history of all the chats and docs
he had submitted earlier. Howver this feature should be implemented later. So first give me the solutions of the 
questions
4. Should automatically remove vectors of that namespace if session state cleared,i.e. if page reloaded

'''