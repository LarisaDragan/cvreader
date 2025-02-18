
# create the croma client
import chromadb
chroma_client = chromadb.Client()


# create a collection
collection = chroma_client.create_collection(name="extracted_information")