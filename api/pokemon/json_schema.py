from flask_restx import fields, Model

pokemon_post = {
    'name': fields.String(required=True)
}

pokemon_sprites = Model("Sprites", {
    "back_default": fields.String(),
    "back_female": fields.String(),
    "back_shiny": fields.String(),
    "back_shiny_female": fields.String(),
    "front_default": fields.String(),
    "front_female": fields.String(),
    "front_shiny": fields.String(),
    "front_shiny_female": fields.String()
})

pokemon_get = {
    'base_experience': fields.Integer(),
    'height': fields.Integer(),
    'id': fields.Integer(attribute='_id'),
    'name': fields.String(),
    'sprites': fields.Nested(pokemon_sprites),
    'weight': fields.Integer
}
