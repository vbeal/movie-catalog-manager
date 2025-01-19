import os
from flask import Flask, redirect, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configurar o app Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sua_chave_secreta")
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Configuração do MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["MONGO_DB_NAME"] = os.getenv("MONGO_DB_NAME")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta")

# Conectar ao MongoDB
try:
    client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)
    db = client[app.config["MONGO_DB_NAME"]]
    db.command("ping")  # Testar conexão
    print(f"Conexão com o MongoDB '{app.config['MONGO_DB_NAME']}' estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    exit(1)

# Rotas principais
@app.route("/")
def home():
    return redirect(url_for("login_page"))

# Adicionar rotas externas
from session_routes import initialize_session_routes
from user_routes import initialize_user_routes

initialize_session_routes(app, db)
initialize_user_routes(app, db)

# Contexto para o rodapé dinâmico
@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}

if __name__ == "__main__":
    app.run(debug=True)
