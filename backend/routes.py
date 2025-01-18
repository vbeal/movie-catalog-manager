from flask_restful import Resource
from flask import request
from bson.objectid import ObjectId  # Para lidar com IDs do MongoDB

class MovieList(Resource):
    def __init__(self, db):
        self.db = db

    def get(self):
        """Lista todos os filmes no banco de dados."""
        movies = self.db.movies.find()
        return [
            {
                "_id": str(movie["_id"]),
                "title": movie["title"],
                "genre": movie["genre"],
                "year": movie["year"]
            }
            for movie in movies
        ], 200

    def post(self):
        """Adiciona um novo filme ao banco de dados."""
        data = request.json
        result = self.db.movies.insert_one(data)
        return {"message": "Filme adicionado com sucesso!", "id": str(result.inserted_id)}, 201

class MovieDetail(Resource):
    def __init__(self, db):
        self.db = db

    def put(self, movie_id):
        """Atualiza um filme existente pelo ID."""
        data = request.json
        result = self.db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": data})
        if result.modified_count > 0:
            return {"message": "Filme atualizado com sucesso!"}, 200
        return {"message": "Nenhuma alteração foi realizada."}, 404

    def delete(self, movie_id):
        """Exclui um filme pelo ID."""
        result = self.db.movies.delete_one({"_id": ObjectId(movie_id)})
        if result.deleted_count > 0:
            return {"message": "Filme removido com sucesso!"}, 200
        return {"message": "Filme não encontrado."}, 404

# Inicializar rotas
def initialize_routes(api, db):
    api.add_resource(MovieList, "/movies", resource_class_args=(db,))
    api.add_resource(MovieDetail, "/movies/<string:movie_id>", resource_class_args=(db,))
