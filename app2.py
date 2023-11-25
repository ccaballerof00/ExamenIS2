from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts.chat import (ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate)
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)

load_dotenv()

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

prompt = """Usa los pedazos de contexto sobre peliculas otorgados a continuación para responder las preguntas.
Si no sabes la respuesta, hazlo saber. Las preguntas pueden estar en inglés o español.
{context}

Begin!
--------
Question: {question}
Helpful Answer:"""

messages = [
    SystemMessagePromptTemplate.from_template(prompt),
    HumanMessagePromptTemplate.from_template("{question}")
]

final_prompt = ChatPromptTemplate.from_messages(messages)

db3 = Chroma(persist_directory="db4/", embedding_function=embedding_function)

llm=ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo-0613")

question = "Dime peliculas de Leonardo Dicaprio"



@app.route('/query', methods=['POST'])
def query_movies():
    data = request.get_json()
    query_text = data.get('query')
    chain = RetrievalQA.from_chain_type(
        llm,
        retriever=db3.as_retriever(),
        chain_type_kwargs= {"prompt": final_prompt}
        )
    result = chain({"query" : query_text})
    return result

if __name__ == '__main__':
    app.run(debug=True, port=5000)