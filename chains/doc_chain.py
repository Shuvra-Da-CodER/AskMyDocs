from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda
from utils.pinecone_utils import embed_texts_to_pinecone

def get_document_chain(namespace: str):
    def process(text):
        chunk_size=1000
        chunks_num=len(text)//chunk_size
        if chunks_num>=75:
            chunk_size=len(text)//75
        overlap=0.1*chunk_size
        print('text length',len(text))
        print('chunksize',chunk_size)
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap )
        chunks = splitter.split_text(text)
        print(len(chunks))

        
        data=[]

        for i, doc in enumerate(chunks):
            dict={}
            text=doc
            dict['id']=f'vec{i}'
            dict['text']=text
            data.append(dict)
        
        print(len(data))

        embed_texts_to_pinecone(data, namespace)
        return "Documents embedded and stored."
    
    return RunnableLambda(process)
