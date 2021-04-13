import json

import pytest

from api.mongo import Pokemon
from app import create_app


@pytest.fixture
def test_client():

    flask_app = create_app(test=True,
                           mongo_config=dict(
                               db='mongoengine_mock',
                               host='mongomock://localhost',
                               alias='pokemon_api'
                           ))

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client

    Pokemon.drop_collection()


def test_get_all_pokemons(test_client):

    response = test_client.get('/api/pokemon/')
    assert response.status_code == 200

    returned_data = json.loads(response.data)
    assert isinstance(returned_data, list)


def test_post_new_pokemon(test_client):
    assert Pokemon.objects().count() == 0

    response = test_client.post('/api/pokemon/', json={"name": "ekans"})
    assert response.status_code == 201
    assert json.loads(response.data) is None

    pokemon_in_db = json.loads(test_client.get('/api/pokemon/').data)
    assert pokemon_in_db[0]['name'] == 'ekans'


def test_post_new_pokemon_which_doesnt_exist(test_client):
    assert Pokemon.objects().count() == 0

    response = test_client.post('/api/pokemon/', json={"name": "doesnt_exist"})
    assert response.status_code == 404

    assert Pokemon.objects().count() == 0


def test_post_new_pokemon_which_already_exists(test_client):
    assert Pokemon.objects().count() == 0

    test_client.post('/api/pokemon/', json={"name": "ekans"})
    response = test_client.post('/api/pokemon/', json={"name": "ekans"})

    assert response.status_code == 200
    assert {'base_experience', 'name', 'height', 'weight', 'sprites', 'id'}.issubset(json.loads(response.data))


@pytest.mark.parametrize(
    'payload',
    [
        {"name": 20},
        dict(),
        {"extra_field": "extra"},
        'String',
        200

    ]
)
def test_post_new_pokemon_with_invalid_payload(test_client, payload):
    response = test_client.post('/api/pokemon/', json=payload)
    assert response.status_code == 400


def test_post_new_encounter(test_client):
    assert Pokemon.objects().count() == 0

    test_client.post('/api/pokemon/', json={"name": "ekans"})
    response = test_client.post('/pokemon/23/encounters', json={"place": "city"})

    assert response.status_code == 201
    assert Pokemon.objects(name='ekans').first().encounters[0]['place'] == 'city'


@pytest.mark.parametrize(
    'payload',
    [
        {"place": 20},
        dict(),
        {"no_place": 'extra'},
        'String',
        200
    ]
)
def test_post_new_encounter_with_invalid_payload(test_client, payload):
    response = test_client.post('/pokemon/23/encounters', json=payload)
    assert response.status_code == 400


def test_get_all_encounters(test_client):
    assert Pokemon.objects().count() == 0

    test_client.post('api/pokemon/', json={"name": "ekans"})
    test_client.post('/pokemon/23/encounters', json={"place": "city"})

    response = test_client.get(r'/pokemon/23/encounters')
    returned_data = json.loads(response.data)

    assert isinstance(returned_data, list)
    assert len(returned_data) == 1
    assert 'timestamp' in returned_data[0]
    assert returned_data[0]['place'] == 'city'


def test_get_all_encounters_for_missing_id(test_client):
    assert Pokemon.objects().count() == 0

    response = test_client.get('/pokemon/23/encounters')
    assert response.status_code == 404


def test_if_other_http_methods_are_not_usable(test_client):
    for method in ('delete', 'put', 'patch'):
        response_encounters = getattr(test_client, method)('/pokemon/23/encounters')
        response_pokemons = getattr(test_client, method)('api/pokemon/')
        assert response_encounters.status_code == response_pokemons.status_code == 405
