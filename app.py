import chromadb
from flask import Flask, request, jsonify
from chromadb.utils import embedding_functions

app = Flask(__name__)

ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-large")
chroma_client = chromadb.PersistentClient(path="db3/")
chroma_collection = chroma_client.get_or_create_collection(name="Students", embedding_function=ef)

@app.route('/query', methods=['POST'])
def query_movies():
    data = request.get_json()
    query_text = data.get('query')
    
    if not query_text:
        return jsonify({"error": "Se debe enviar un query."}), 400

    results = chroma_collection.query(
        query_texts=[query_text],
        n_results=5,
        include=["documents"]
    )
    documents = results.get("documents", [])
    movies = []
    for doc in documents:
        for movie in doc:
            info = movie.split("$")
            name = info[0]
            genres = info[1]
            rating = info[2]
            tags = info[3] if len(info) >= 3 else []
            body = {
                "name": name,
                "rating": round(float(rating), 2),
                "genres": [],
                "tags": [],
            }
            for genre in genres.split('|'):
                body['genres'].append(genre)
            for tag in tags.split(' '):
                if tag:
                    body['tags'].append(tag)
            movies.append(body)
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True, port=5001)