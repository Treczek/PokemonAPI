import logging
from collections.abc import Mapping

from flask import request
from flask_restx import Resource, Namespace

import api.encounter.json_schema as schema
from api.backend import PokemonService
from api.utils.exceptions import NonExistingPokemon, InvalidPayload

encounter_api = Namespace('Encounters', description='Pokemon encounters', path='/api/pokemon/', validate=True)

model_encounter_post = encounter_api.model('EncounterPost', schema.encounter_post)
model_encounter_get = encounter_api.model('EncounterGet', schema.encounter_get)


@encounter_api.route('/<id>/encounters')
@encounter_api.doc(params={'id': 'Pokemon ID'})
class Encounters(Resource):

    @encounter_api.marshal_with(model_encounter_get, as_list=True)
    @encounter_api.response(200, model=model_encounter_get, description="Encounters successfully obtained.")
    @encounter_api.doc(responses={404: "Pokemon with given ID doesn't exist in the database"})
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

    @encounter_api.expect(model_encounter_post, validate=True)
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
