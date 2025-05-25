from pinecone import Pinecone
from dotenv import load_dotenv
import os
load_dotenv()

api_key=os.environ["PINECONE_API_KEY"]
index_name='pdf-rag'
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)
stats = index.describe_index_stats()
namespaces = stats["namespaces"].keys()

# Loop through and delete all vectors in each
for ns in namespaces:
    index.delete(delete_all=True, namespace=ns)

print("✅ All namespaces have been cleared.")