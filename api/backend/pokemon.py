"""
Class which handles all operations within Pokemon queries
"""
import json
import logging
from datetime import datetime

import requests
from flask import jsonify, Response
from mongoengine.errors import FieldDoesNotExist

from api.schemas import Pokemon, Sprite, Encounter
from api.utils.exceptions import NonExistingPokemon, InvalidPayload
from api.utils import replace_id_field_in_response


class PokemonService:

    @staticmethod
    def get_by_name(pokemon_name: str) -> Pokemon:
        """
        Searching database for Pokemon with given name value. Raise NonExistingPokemon error if not found.
        :param pokemon_name: name of Pokemon that needs to be returned
        :return: Pokemon Object with given name
        """

        pokemon = Pokemon.objects.exclude("encounters").filter(name=pokemon_name).first()

        if not pokemon:
            raise NonExistingPokemon

        response = jsonify(pokemon)
        return replace_id_field_in_response(response)

    @staticmethod
    def get_by_id(pokemon_id: int) -> Pokemon:
        """
        Searching database for Pokemon with given id value. Raise NonExistingPokemon error if not found.
        :param pokemon_id: id of Pokemon that needs to be returned
        :return: Pokemon Object with given id
        """

        pokemon = Pokemon.objects(id=pokemon_id).first()

        if not pokemon:
            raise NonExistingPokemon

        return pokemon

    @staticmethod
    def get_all_pokemons() -> Response:
        """
        Return all Pokemons saved in the database in a required format.
        :return: Response object containing list of all Pokemon documents saved in the database
        """

        list_of_all_pokemons = Pokemon.objects.exclude('encounters')
        response = jsonify(list_of_all_pokemons)

        return replace_id_field_in_response(response)

    @staticmethod
    def get_all_encounters(pokemon_id: int) -> Response:
        """
        Return all encounters for given pokemon id.
        :return: Response object containing list of encounter jsons
        """
        return jsonify(PokemonService.get_by_id(pokemon_id).encounters)

    @staticmethod
    def add_pokemon_from_external_api(pokemon_name_or_id: str) -> dict:
        """
        Fetching pokemon object from https://pokeapi.co/api/v2/pokemon/{pokemon_name} API.
        If its exists -> save it to the datavase, if not, raise NonExistingPokemon error.
        :param pokemon_name_or_id: name of the pokemon that needs to be fetched
        """

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}/'
        response = requests.get(url)

        if response.status_code == 404:
            raise NonExistingPokemon

        PokemonService.save_pokemon(pokemon=json.loads(response.content))

    @staticmethod
    def save_pokemon(pokemon: dict) -> Pokemon:
        """
        Create Pokemon object from given dictionary.
        If dictionary contain keys that are not specified in the schema, they will be omitted.
        :param pokemon: dictionary with Pokemon information.
        """

        Pokemon(
            id=pokemon['id'],
            name=pokemon['name'],
            weight=pokemon['weight'],
            height=pokemon['height'],
            base_experience=pokemon['base_experience'],
            sprites=Sprite.pick_specified_fields(pokemon['sprites'])
        ).save()

        logging.getLogger('PokemonAPI').info(f"{pokemon['name']} created in the database")

    @staticmethod
    def add_pokemon_encounter(pokemon_id: id, encounter_json: dict):
        """
        Find Pokemon with given id and append an encounter to Pokemon.encounters field. Save afterwards.
        :param pokemon_id: id of encountered pokemon
        :param encounter_json: json with encounter information. It has to be in line with EncounterJsonSchema
        """

        try:
            encounter = Encounter(**encounter_json)
        except FieldDoesNotExist as exc:
            raise InvalidPayload(exc.args[0])  # Passing detailed message about the payload error

        try:
            pokemon = PokemonService.get_by_id(pokemon_id)
        except NonExistingPokemon:
            PokemonService.add_pokemon_from_external_api(pokemon_id)
            pokemon = PokemonService.get_by_id(pokemon_id)

        encounter.timestamp = int(datetime.now().timestamp())
        pokemon.encounters.append(encounter)
        pokemon.save()
