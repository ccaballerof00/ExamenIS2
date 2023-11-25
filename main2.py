import chromadb
from chromadb.utils import embedding_functions
from pymongo import MongoClient

ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-large")
chroma_client = chromadb.PersistentClient(path="db3/")
chroma_collection = chroma_client.get_or_create_collection(name="Students", embedding_function=ef)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['lab_x']
mongo_collection = mongo_db['data']

cursor = mongo_collection.find()

lista = []
ids = []

i=0

for document in cursor:
    item = f"{document['title']}${document['genres']}${document['rating']}$"
    for tag in document['tags'].keys():
        item += f" {tag}"
    lista.append(item)
    ids.append(str(i))
    i += 1

chroma_collection.add(
    documents = lista,
    ids = ids
)



results = chroma_collection.query(
    query_texts=["Recommend me movies with Leonardo Dicaprio"],
    n_results=5
)

print(results)