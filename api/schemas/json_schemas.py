"""
Schemas for inputs and outputs of API. Most of them will be attached to Swagger documentation
"""

from api import pokemon_api, encounter_api
from flask_restx import fields

encounters_post = encounter_api.model('EncountersPost', {
    'place': fields.String(required=True),
    'note': fields.String()
})

encounters_get = encounter_api.model('EncountersGet', {
    'place': fields.String(required=True),
    'note': fields.String(),
    'timestamp': fields.Integer(required=True)
})

pokemons_post = pokemon_api.model('PokemonsPost', {
    'name': fields.String(required=True)
})

pokemon_sprites = pokemon_api.model('Sprites', {
    "back_default": fields.String(),
    "back_female": fields.String(),
    "back_shiny": fields.String(),
    "back_shiny_female": fields.String(),
    "front_default": fields.String(),
    "front_female": fields.String(),
    "front_shiny": fields.String(),
    "front_shiny_female": fields.String()
})

pokemons_get = pokemon_api.model('PokemonsGet', {
    'base_experience': fields.Integer(),
    'height': fields.Integer(),
    'id': fields.Integer(attribute='_id'),
    'name': fields.String(),
    'sprites': fields.Nested(pokemon_sprites),
    'weight': fields.Integer
})
