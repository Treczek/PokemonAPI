from collections.abc import Mapping

from flask import request
from flask_restx import Resource, Namespace, marshal

import api.pokemon.json_schema as schema
from api.backend import PokemonService
from api.utils.exceptions import NonExistingPokemon

pokemon_api = Namespace('Pokemons', description='Pokemon details', path='/api/pokemon', validate=True)

model_pokemon_post = pokemon_api.model('PokemonsPost', schema.pokemon_post)
model_pokemon_sprites = pokemon_api.model('Sprites', schema.pokemon_sprites)
model_pokemon_get = pokemon_api.model('PokemonsGet', schema.pokemon_get)


@pokemon_api.route("/")
class Pokemons(Resource):

    @pokemon_api.marshal_with(model_pokemon_get, as_list=True, code=200)
    @pokemon_api.response(200, model=model_pokemon_get, description="All pokemons saved in the database successfully "
                                                                    "returned.")
    def get(self):
        """
        Return a list of all pokemons in the database. If there is none Pokemons in the database, return empty list.
        """
        return PokemonService.get_all_pokemons()

    @pokemon_api.expect(model_pokemon_post, validate=True)
    @pokemon_api.doc(responses={200: 'Pokemon with posted name exists in the database and was returned to the client',
                                201: 'Pokemon with posted name was created in the database.',
                                404: 'Pokemon was not found. Confirm if its name exists.'})
    def post(self):
        """
        Return the pokemon from the database or fetch it from the external and save to the database.
        """
        json_data = request.get_json()

        if not isinstance(json_data, Mapping):
            pokemon_api.abort(400, "Payload must be a JSON type.")

        try:
            return marshal(PokemonService.get_by_name(json_data['name']), model_pokemon_get), 200
        except NonExistingPokemon:
            try:
                PokemonService.add_pokemon_from_external_api(json_data['name'])
            except NonExistingPokemon:
                pokemon_api.abort(404, f"{json_data['name']} was not found in the database and external API.")
            return None, 201

    @pokemon_api.hide
    def delete(self):
        pokemon_api.abort(405)

    @pokemon_api.hide
    def put(self):
        pokemon_api.abort(405)

    @pokemon_api.hide
    def patch(self):
        pokemon_api.abort(405)
