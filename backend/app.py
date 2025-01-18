import os
from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o Flask
app = Flask(__name__)
api = Api(app)

# Configurações do MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["MONGO_DB_NAME"] = os.getenv("MONGO_DB_NAME")

# Testar a conexão com o MongoDB
try:
    client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)
    db = client[app.config["MONGO_DB_NAME"]]
    db.command("ping")  # Testar a operação 'ping'
    print(f"Conexão com o MongoDB '{app.config['MONGO_DB_NAME']}' estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    exit(1)

# Rota raiz para verificar se a API está funcionando
@app.route("/")
def home():
    return {"message": "API Movie Catalog Manager funcionando corretamente!"}, 200

# Importar rotas
from routes import initialize_routes
initialize_routes(api, db)  # Passar a instância do banco para as rotas

if __name__ == "__main__":
    app.run(debug=True)
