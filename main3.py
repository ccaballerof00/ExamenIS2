from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['lab_x']
mongo_collection = mongo_db['data']

cursor = mongo_collection.find()

lista = []

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

for document in cursor:
    item = f"{document['title']}${document['genres']}${document['rating']}$"
    for tag in document['tags'].keys():
        item += f" {tag}"
    lista.append(item)

db = Chroma.from_texts(lista, embedding_function, persist_directory="db4")



