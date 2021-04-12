import mongoengine
import pytest
from mongoengine import connect, disconnect

from api.backend import PokemonService
from api.mongo import Pokemon, Encounter
from api.utils.exceptions import NonExistingPokemon, InvalidPayload


def stabbed_external_api_call(name_or_id):

    if name_or_id not in ['ekans', 23]:
        raise AttributeError('During tests of non existing pokemons you must use ekans or id 23')

    PokemonService.save_pokemon(
        {
            "base_experience": 58,
            "height": 20,
            "id": 23,
            "name": "ekans",
            "sprites": {
                "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/23.png",
                "back_female": None,
                "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/23.png",
                "back_shiny_female": None,
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/23.png",
                "front_female": None,
                "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/23.png",
                "front_shiny_female": None
            },
            "weight": 69}
    )


PokemonService.add_pokemon_from_external_api = stabbed_external_api_call


@pytest.fixture
def db():
    """
    This fixture will mock the MongoDB testing instance and pass it for testing. After each test is done, it will delete
    it so we will have clean database for next tests.
    :yield: connection to mocked MongoDB
    """

    # Creating new database
    connect('mongoengine', host='mongomock://localhost', alias='pokemonapi')

    # Yielding connection to tests
    yield

    # Teardown of created db
    Pokemon.drop_collection()


@pytest.fixture
def ekans():
    return {
        "base_experience": 58,
        "height": 20,
        "id": 23,
        "name": "ekans",
        "sprites": {
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/23.png",
            "back_female": None,
            "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/23.png",
            "back_shiny_female": None,
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/23.png",
            "front_female": None,
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/23.png",
            "front_shiny_female": None
        },
        "weight": 69}


@pytest.fixture
def hitmonlee():
    return {
       "base_experience": 159,
       "height": 15,
       "id": 106,
       "name": "hitmonlee",
       "sprites": {
           "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/106.png",
           "back_female": None,
           "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/106.png",
           "back_shiny_female": None,
           "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/106.png",
           "front_female": None,
           "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/106.png",
           "front_shiny_female": None
       },
       "weight": 498
   }


@pytest.fixture
def snorlax():
    return {
        "base_experience": 189,
        "height": 21,
        "id": 143,
        "name": "snorlax",
        "sprites": {
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/143.png",
            "back_female": None,
            "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/143.png",
            "back_shiny_female": None,
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png",
            "front_female": None,
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/143.png",
            "front_shiny_female": None
        },
        "weight": 4600}


@pytest.fixture
def encounter():
    return {'place': 'city',
             'note': 'Ekans was waiting on the sidewalk for someone.'}


def test_saving_pokemon_to_db(db, ekans, hitmonlee, snorlax):
    assert Pokemon.objects().count() == 0

    for pokemon in (ekans, hitmonlee, snorlax):
        Pokemon(**pokemon).save()

    assert Pokemon.objects().count() == 3
    assert set(ekans.keys()).issubset(Pokemon.objects(name='ekans').first()._fields)


def test_return_all_pokemons_is_a_list(db, ekans, hitmonlee):
    assert Pokemon.objects().count() == 0
    assert isinstance(PokemonService.get_all_pokemons(), list)
    Pokemon(**ekans).save()
    assert isinstance(PokemonService.get_all_pokemons(), list)
    Pokemon(**hitmonlee).save()
    assert isinstance(PokemonService.get_all_pokemons(), list)


def test_return_all_pokemons_has_all_specified_fields(db, ekans, snorlax):
    assert Pokemon.objects().count() == 0

    # '_id' field is renamed to 'id' on the API layer, just before returning to client.
    specified_fields = {"base_experience", "height", "_id", "name", "sprites", "weight"}
    specified_sprite_fields = {"back_default", "back_female", "back_shiny", "back_shiny_female", "front_default",
                               "front_female", "front_shiny", "front_shiny_female"}

    for pokemon in (ekans, snorlax):
        Pokemon(**pokemon).save()

    pokemons = [pokemon.to_mongo().to_dict() for pokemon in Pokemon.objects()]

    assert all(
        [specified_fields.issubset(pokemon.keys()) and
         specified_sprite_fields.issubset(pokemon['sprites'].keys())
         for pokemon
         in pokemons]
    )


def test_get_pokemon_by_name(db, snorlax):
    assert Pokemon.objects().count() == 0

    Pokemon(**snorlax).save()
    mongo_pokemon = PokemonService.get_by_name('snorlax')

    assert mongo_pokemon['weight'] == snorlax['weight']
    assert mongo_pokemon['height'] == snorlax['height']


def test_get_pokemon_by_name_if_name_doesnt_exist():
    with pytest.raises(NonExistingPokemon):
        PokemonService.get_by_name('doesnt_exist')


def test_get_pokemon_by_id(db, snorlax):
    assert Pokemon.objects().count() == 0

    Pokemon(**snorlax).save()
    mongo_pokemon = PokemonService.get_by_id(143)

    assert mongo_pokemon['weight'] == snorlax['weight']
    assert mongo_pokemon['height'] == snorlax['height']


def test_get_pokemon_by_id_if_id_doesnt_exist():
    with pytest.raises(NonExistingPokemon):
        PokemonService.get_by_id(9999)


def test_add_pokemon_encounter(db, ekans):

    Pokemon(**ekans).save()
    encounter = {'place': 'city',
                 'note': 'Ekans was waiting on the sidewalk for someone.'}

    PokemonService.add_pokemon_encounter(pokemon_id=23, encounter_json=encounter)

    mongo_encounter = Pokemon.objects(name='ekans').first().encounters[0]

    assert mongo_encounter.place == encounter['place']
    assert mongo_encounter.note == encounter['note']
    assert mongo_encounter.timestamp


# parametrize with different errors
@pytest.mark.parametrize(
    'encounter_json', [
        ({'note': 'place is unknown'}),
        ({'place': 12}),
        (dict()),
        {'place': "forest", 'day': 'tuesday'}
    ]
)
def test_add_pokemon_encounter_with_invalid_data(db, ekans, encounter_json):

    Pokemon(**ekans).save()
    with pytest.raises(InvalidPayload):
        PokemonService.add_pokemon_encounter(pokemon_id=23, encounter_json=encounter_json)


def test_get_pokemon_encounters(db, ekans):

    Pokemon(**ekans).save()
    encounter = {'place': 'city',
                 'note': 'Ekans was waiting on the sidewalk for someone.'}

    for _ in range(5):
        PokemonService.add_pokemon_encounter(23, encounter_json=encounter)

    mongo_encounters = PokemonService.get_all_encounters(23)

    assert len(mongo_encounters) == 5
    assert isinstance(mongo_encounters, list)
    assert all(['timestamp' in encounter for encounter in mongo_encounters])


def test_get_pokemon_encounters_if_id_doesnt_exist(db, encounter):
    assert Pokemon.objects().count() == 0

    PokemonService.add_pokemon_encounter(23, encounter)

    assert Pokemon.objects().count() == 1
    assert Pokemon.objects().first().name == 'ekans'
