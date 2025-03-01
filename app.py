from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODELS_URL = "http://localhost:11434/api/tags"

# Route pour afficher la page de chat
@app.route('/')
def index():
    return render_template('index.html')

# Route pour récupérer la liste des modèles
@app.route('/models', methods=['GET'])
def list_models():
    try:
        response = requests.get(OLLAMA_MODELS_URL)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return jsonify(models)
        else:
            return jsonify({"error": "Failed to fetch models"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour générer une réponse
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    model = data.get('model', 'default-model')

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return jsonify({"response": response.json().get('response')})
        else:
            return jsonify({"error": "Failed to generate response"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)