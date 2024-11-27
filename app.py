from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
BACKEND_API_URL = os.getenv('BACKEND_API_URL')

@app.route('/')
def index():
    response = requests.get(f"{BACKEND_API_URL}/movies/top-rated")
    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        data = response.json()  # Converte para JSON apenas se o status for 200
    else:
        data = {"error": f"Erro ao conectar ao back-end: {response.status_code}"}
    return render_template('index.html', data=data)



@app.route('/movie', methods=['GET'])
def movie():
    movie_id = request.args.get('id')  # Obtém o nome do filme da URL
    
    if not movie_id:
        return jsonify({"error": "Nome do filme é necessário"}), 400  # Se o nome não for fornecido
    
    try:
        response = requests.get(f"{BACKEND_API_URL}/movies/search/{movie_id}")
        
        if response.status_code == 200:
            data = response.json()  # Dados retornados pela API do backend
            # Se 'data' já for uma lista, passe-a diretamente para o template
            return render_template('movie_details.html', data=data)  # Passa 'data' diretamente
        else:
            return jsonify({"error": f"Erro ao buscar o filme: {response.status_code}"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro de conexão: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)