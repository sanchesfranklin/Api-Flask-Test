from flask_restful import Resource
from api import api
from ..schema import projeto_schema
from flask import request, make_response, jsonify
from ..entidades import projeto
from ..services import projeto_service

class ProjetoList(Resource):
    # Listar todas as projetos
    def get(self):
        projetos = projeto_service.listar_projetos()
        ps = projeto_schema.ProjetoSchema(many=True)
        return make_response(ps.jsonify(projetos), 200)

    # Cadastrar projeto
    def post(self):
        ps = projeto_schema.ProjetoSchema()
        validate = ps.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            projeto_novo = projeto.Projeto(nome=nome, descricao=descricao)
            result = projeto_service.cadastrar_projeto(projeto_novo)
            return make_response(ps.jsonify(result), 201)

class ProjetoDetail(Resource):

    # Listar projeto por ID
    def get(self, id):
        projeto = projeto_service.listar_projeto_id(id)
        if projeto is None:
            return make_response(jsonify("Projeto não encontrada"), 404)

        ps = projeto_schema.ProjetoSchema()
        return make_response(ps.jsonify(projeto), 200)

    # Editar projeto
    def put(self, id):
        projeto_bd = projeto_service.listar_projeto_id(id)
        if projeto_bd is None:
            return make_response(jsonify("Projeto não encontrada"), 404)

        ps = projeto_schema.ProjetoSchema()
        validate = ps.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            projeto_novo = projeto.Projeto(nome=nome, descricao=descricao)
            projeto_service.editar_projeto(projeto_bd, projeto_novo)
            projeto_atualizado = projeto_service.listar_projeto_id(id)
            return make_response(ps.jsonify(projeto_atualizado), 200)

    # Remover projeto
    def delete(self, id):
        projeto = projeto_service.listar_projeto_id(id)
        if projeto is None:
            return make_response(jsonify("Projeto não encontrado"), 404)
        projeto_service.remover_projeto(projeto)
        return make_response('', 204)

api.add_resource(ProjetoList, '/projetos')
api.add_resource(ProjetoDetail, '/projetos/<int:id>')