"""
Class which handles all operations within Pokemon queries
"""
import json
from typing import List

import requests
from api.utils.exceptions import NonExistingPokemon
from api.mongo_objects import Pokemon, Sprite
from flask import jsonify


class PokemonService:

    @staticmethod
    def get_all() -> List[Pokemon]:
        return jsonify(Pokemon.objects())

    @staticmethod
    def get_by_name(pokemon_name: str) -> Pokemon:

        pokemon = Pokemon.objects(name=pokemon_name).first()

        if not pokemon:
            raise NonExistingPokemon

        return jsonify(pokemon)

    @staticmethod
    def fetch_from_pokeapi(pokemon_name: str) -> dict:
        """
        Fetching pokemon object from https://pokeapi.co/api/v2/pokemon/{pokemon_name} API.
        If it doesn't exist raise NonExistingPokemon exception
        :param pokemon_name: name of the pokemon that needs to be fetched
        :return: dictionary with Pokemon information
        """

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
        response = requests.get(url)

        if response.status_code == 404:
            raise NonExistingPokemon

        return json.loads(response.content)

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
