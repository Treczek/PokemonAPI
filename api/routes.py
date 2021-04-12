"""
Main module for Flask application.
"""

import logging

from flask import request
from flask_restx import Resource
from collections.abc import Mapping

from api import pokemon_api, encounter_api
from api.backend import PokemonService
from api.utils.exceptions import NonExistingPokemon, InvalidPayload
import api.schemas as schema


@pokemon_api.route("/")
class Pokemons(Resource):

    @pokemon_api.marshal_with(schema.pokemons_get, as_list=True, code=200)
    @pokemon_api.response(200, "All pokemons saved in the database successfully returned.")
    def get(self):
        """
        Return a list of all pokemons in the database. If there is none Pokemons in the database, return empty list.
        """
        return PokemonService.get_all_pokemons()

    @pokemon_api.expect(schema.pokemons_post, validate=True)
    @pokemon_api.marshal_with(schema.pokemons_get, code=200)
    @pokemon_api.doc(responses={200: 'Pokemon with posted name exists in the database and was returned to the client',
                                201: 'Pokemon with posted name was created in the database.',
                                404: 'Pokemon was not found. Confirm if its name exists.'})
    def post(self):
        """
        Return the pokemon from the database or fetch it from the external and save to the database.
        """
        json_data = request.get_json()

        if not isinstance(json_data, Mapping):
            encounter_api.abort(400, "Payload must be a JSON type.")

        try:
            return PokemonService.get_by_name(json_data['name'])
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


@encounter_api.route('/<id>/encounters')
@encounter_api.doc(params={'id': 'Pokemon ID'})
class Encounters(Resource):

    @encounter_api.marshal_with(schema.encounters_get, as_list=True)
    @encounter_api.doc(responses={200: "Encounters successfully obtained.",
                                  404: "Pokemon with given ID doesn't exist in the database"})
    def get(self, id):
        """
        Return list of all encounters for given pokemon id.
        """

        try:
            encounters = PokemonService.get_all_encounters(pokemon_id=id)
        except NonExistingPokemon:
            encounter_api.abort(404)
        else:
            return encounters

    @encounter_api.expect(schema.encounters_post, validate=True)
    @encounter_api.doc(responses={201: 'Encounter was successfully attached to the Pokemon.',
                                  400: 'Payload has not met validation schema for Encounter object',
                                  404: 'Pokemon was not found. Confirm if its name exists.'})
    def post(self, id):
        """
        Attach new encounter to the Pokemon with given id.
        If pokemon doesn't exist in the database, it will be fetched from the external API.
        """
        encounter_json = request.get_json()

        if not isinstance(encounter_json, Mapping):
            encounter_api.abort(400, "Payload must be a JSON type.")

        # Informing the server about the encounter
        logging.getLogger("PokemonAPI").info(f'Pokemon encounter has been posted to the server: {request.get_json()}')

        try:
            PokemonService.add_pokemon_encounter(pokemon_id=id, encounter_json=encounter_json)
        except InvalidPayload as exc:
            encounter_api.abort(400, message=exc.args[0])
        except NonExistingPokemon:
            encounter_api.abort(404, message="Pokemon was never encountered.")
        else:
            return None, 201

    @encounter_api.hide
    def delete(self):
        encounter_api.abort(405)

    @encounter_api.hide
    def put(self):
        encounter_api.abort(405)

    @encounter_api.hide
    def patch(self):
        encounter_api.abort(405)
