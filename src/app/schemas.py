from marshmallow import Schema, fields

class PokemonSchema(Schema):
    id = fields.Integer()
    rank = fields.Integer()
    name = fields.String()
    type_1 = fields.String()
    type_2 = fields.String()
    total = fields.Integer()
    hp = fields.Integer()
    attack = fields.Integer()
    defence = fields.Integer()
    speed = fields.Integer()
    generation = fields.Integer()
    legendary = fields.Boolean()