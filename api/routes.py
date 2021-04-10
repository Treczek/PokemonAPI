"""
Main module for Flask application.
"""

from flask import request
from flask_restx import Resource, fields
import logging

from api import pokemon_api, pokemon_encounters_api
from api.utils.exceptions import NonExistingPokemon
from api.services import PokemonService

pokemon_post_input = pokemon_api.model(
    'Post input', {
        'name': fields.String,
    })


@pokemon_api.route("/")
class PokemonRoutes(Resource):

    def get(self):
        """
        Return a list of all pokemons in the database
        """
        return PokemonService.get_all()

    @pokemon_api.expect(pokemon_post_input, validate=True)
    def post(self):
        """
        Return the pokemon from the database or fetch it from the external and save to the database.
        """

        json_data = request.get_json()

        # TODO Handle wrong json file
        try:
            return PokemonService.get_by_name(json_data['name'])
        except NonExistingPokemon:
            pokemon = PokemonService.fetch_from_pokeapi(json_data['name'])
            PokemonService.save_pokemon(pokemon)


@pokemon_encounters_api.route('/<id>/encounters')
class PokemonEncountersRoutes(Resource):

    def get(self, id):
        # Return all encounters
        return id

    def post(self, id):

        logging.getLogger("PokemonAPI").info('Pokemon encounter has been posted')
        # Inform the server about the encounter??
        # Request should have optional note and obligatory place.
        # Timestamp is added during object creation

        print(id)
        return id
