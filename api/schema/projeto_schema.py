from api import ma
from ..models import projeto_model
from marshmallow import fields

class ProjetoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = projeto_model.Projeto
        fields = ("id", "nome", "descricao")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
