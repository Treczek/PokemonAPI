"""
Main module for Flask application.
"""

from flask import request
from flask_restx import Resource
import logging

from api import pokemon, pokemon_encounters
from api.utils.exceptions import NonExistingPokemon
from api.services import PokemonService


@pokemon.route("/")
class PokemonRoutes(Resource):

    def get(self):
        """
        Return a list of all pokemons in the database
        """
        return PokemonService.get_all_pokemons()

    @pokemon.doc(responses={200: 'Pokemon with posted name exists in the database and was returned to the client',
                            201: 'Pokemon with posted name was created in the database.',
                            404: 'Pokemon was not found. Confirm if its name exists.'})
    def post(self):
        """
        Return the pokemon from the database or fetch it from the external and save to the database.
        """

        json_data = request.get_json()

        try:
            return PokemonService.get_by_name(json_data['name'])
        except NonExistingPokemon:

            try:
                pokemon_json = PokemonService.fetch_from_pokeapi(json_data['name'])
            except NonExistingPokemon:
                pokemon.abort(404)

            PokemonService.save_pokemon(pokemon_json)
            return None, 201

    @pokemon.hide
    def delete(self):
        pokemon.abort(405)

    @pokemon.hide
    def put(self):
        pokemon.abort(405)

    @pokemon.hide
    def patch(self):
        pokemon.abort(405)


@pokemon_encounters.route('/<id>/encounters')
@pokemon_encounters.doc(params={'id': 'Pokemon ID'})
class PokemonEncountersRoutes(Resource):

    def get(self, id):
        # Return all encounters
        return PokemonService.get_all_encounters(pokemon_id=id)

    @pokemon.doc(responses={201: 'Encounter was successfully attached to the Pokemon.',
                            404: 'Pokemon was not found. Confirm if its name exists.'})
    def post(self, id):
        # Informing the server about the encounter
        logging.getLogger("PokemonAPI").info('Pokemon encounter has been posted')

        # Request should have optional note and obligatory place.
        encounter_data = request.get_json()
        PokemonService.add_pokemon_encounter(pokemon_id=id, encounter=encounter_data)
        return None, 201

    @pokemon_encounters.hide
    def delete(self):
        pokemon_encounters.abort(405)

    @pokemon_encounters.hide
    def put(self):
        pokemon_encounters.abort(405)

    @pokemon_encounters.hide
    def patch(self):
        pokemon_encounters.abort(405)
