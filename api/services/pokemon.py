"""
Class which handles all operations within Pokemon queries
"""
import json
import logging
from typing import List

import requests
from flask import jsonify

from api.schemas import Pokemon, Sprite, Encounter
from api.utils.exceptions import NonExistingPokemon


class PokemonService:

    @staticmethod
    def get_by_name(pokemon_name: str) -> Pokemon:
        """
        Searching database for Pokemon with given name value. Raise NonExistingPokemon error if not found.
        :param pokemon_name: name of Pokemon that needs to be returned
        :return: Pokemon Object with given name
        """

        pokemon = Pokemon.objects(name=pokemon_name).first()

        if not pokemon:
            raise NonExistingPokemon

        return jsonify(pokemon)

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

        return jsonify(pokemon)

    @staticmethod
    def get_all_pokemons() -> List[Pokemon]:
        return jsonify(Pokemon.objects())

    @staticmethod
    def get_all_encounters(pokemon_id: int) -> List[Encounter]:
        pass

    @staticmethod
    def fetch_from_pokeapi(pokemon_name_or_id: str) -> dict:
        """
        Fetching pokemon object from https://pokeapi.co/api/v2/pokemon/{pokemon_name} API.
        If it doesn't exist raise NonExistingPokemon exception
        :param pokemon_name_or_id: name of the pokemon that needs to be fetched
        :return: dictionary with Pokemon information
        """

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}/'
        response = requests.get(url)

        if response.status_code == 404:
            raise NonExistingPokemon

        # TODO handle api errors
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

        logging.getLogger('PokemonAPI').info(f"{pokemon['name']} saved to the database")

    @staticmethod
    def add_pokemon_encounter(pokemon_id: id, encounter: dict):
        """
        Find Pokemon with given id and append an encounter to Pokemon.encounters field. Save afterwards.
        :param pokemon_id: id of encountered pokemon
        :param encounter: json with encounter information. It has to be in line with EncounterJsonSchema
        """

        pokemon = PokemonService.get_by_id(pokemon_id)
        pokemon.encounters.append(encounter)
        pokemon.save()
