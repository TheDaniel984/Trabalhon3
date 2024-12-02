from flask import Flask, jsonify

# Cria a aplicação Flask
app = Flask(__name__)

# Rota básica - Teste de funcionamento
@app.route('/')
def home():
    return jsonify({"message": "API está funcionando no localhost!"})

# Inicia o servidor local
if __name__ == '__main__':
    app.run(debug=True)
