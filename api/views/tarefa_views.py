from flask_restful import Resource
from api import api
from ..schema import tarefa_schema
from flask import request, make_response, jsonify
from ..entidades import tarefa
from ..services import tarefa_service

class TarefaList(Resource):
    # Listar todas as Tarefas
    def get(self):
        tarefas = tarefa_service.listar_tarefas()
        ts = tarefa_schema.TarefaSchema(many=True)
        return make_response(ts.jsonify(tarefas), 200)

    # Cadastrar Tarefa
    def post(self):
        ts = tarefa_schema.TarefaSchema()
        validate = ts.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            titulo = request.json["titulo"]
            descricao = request.json["descricao"]
            data_expiracao = request.json["data_expiracao"]
            tarefa_nova = tarefa.Tarefa(titulo=titulo, descricao=descricao, data_expiracao=data_expiracao)
            result = tarefa_service.cadastrar_tarefa(tarefa_nova)
            return make_response(ts.jsonify(result), 201)

class TarefaDetail(Resource):

    # Listar Tarefa por ID
    def get(self, id):
        tarefa = tarefa_service.listar_tarefa_id(id)
        if tarefa is None:
            return make_response(jsonify("Tarefa não encontrada"), 404)

        ts = tarefa_schema.TarefaSchema()
        return make_response(ts.jsonify(tarefa), 200)

    # Editar Tarefa
    def put(self, id):
        tarefa_bd = tarefa_service.listar_tarefa_id(id)
        if tarefa_bd is None:
            return make_response(jsonify("Tarefa não encontrada"), 404)

        ts = tarefa_schema.TarefaSchema()
        validate = ts.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            titulo = request.json["titulo"]
            descricao = request.json["descricao"]
            data_expiracao = request.json["data_expiracao"]
            tarefa_nova = tarefa.Tarefa(titulo=titulo, descricao=descricao,data_expiracao=data_expiracao)
            tarefa_service.editar_tarefa(tarefa_bd, tarefa_nova)
            tarefa_atualizada = tarefa_service.listar_tarefa_id(id)
            return make_response(ts.jsonify(tarefa_atualizada), 200)

    # Remover Tarefa
    def delete(self, id):
        tarefa = tarefa_service.listar_tarefa_id(id)
        if tarefa is None:
            return make_response(jsonify("Tarefa não encontrada"), 404)
        tarefa_service.remover_tarefa(tarefa)
        return make_response('', 204)

api.add_resource(TarefaList, '/tarefas')
api.add_resource(TarefaDetail, '/tarefas/<int:id>')