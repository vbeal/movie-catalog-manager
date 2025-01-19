import os
from flask import request, jsonify
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações iniciais
bcrypt = Bcrypt()
jwt = JWTManager()

# Conectar ao banco de dados
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DB_NAME")

if not mongo_uri or not db_name:
    raise ValueError("As variáveis de ambiente MONGO_URI e MONGO_DB_NAME são obrigatórias.")

client = MongoClient(mongo_uri)
db = client[db_name]

# Registro de usuário
class Register(Resource):
    def post(self):
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Usuário e senha são obrigatórios!"}, 400

        # Verificar se o usuário já existe
        if db.users.find_one({"username": username}):
            return {"message": "Usuário já cadastrado!"}, 400

        # Criar usuário com senha criptografada
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        db.users.insert_one({"username": username, "password": hashed_password})

        return {"message": "Usuário registrado com sucesso!"}, 201

# Login do usuário
class Login(Resource):
    def post(self):
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Usuário e senha são obrigatórios!"}, 400

        # Verificar usuário no banco de dados
        user = db.users.find_one({"username": username})
        if not user or not bcrypt.check_password_hash(user["password"], password):
            return {"message": "Credenciais inválidas!"}, 401

        # Gerar token JWT
        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200
