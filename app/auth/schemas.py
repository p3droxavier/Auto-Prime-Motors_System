from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
  nome = fields.Str(required=True, validate=validate.Length(min=5))
  email = fields.Str(required=True)
  senha = fields.Str(required=True, validate=validate.Length(min=5))
  cpf = fields.Str(required=True, validate=validate.Length(equal=11))
  cargo = fields.Str(required=True)
  setor = fields.Str(required=True)
  telefone = fields.Str()
  endereco = fields.Str()
  data_admissao = fields.Date(required=True, format='%Y-%m-%d')
  salario = fields.Decimal(required=True, as_string=True)
  foto = fields.Str()
  
  
class LoginSchema(Schema):
  nome = fields.Str(required=True, validate=validate.Length(min=5))
  cpf = fields.Str(required=True, validate=validate.Length(equal=11))
  cargo = fields.Str(required=True)
  setor = fields.Str(required=True)
  senha = fields.Str(required=True, validate=validate.Length(min=5))