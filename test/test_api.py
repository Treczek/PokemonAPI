import pytest
from run import create_app
import json
from api.mongo import Pokemon
from mongoengine.connection import disconnect_all, connect


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


def test_get_all_pokemons(test_client):

    respond = json.loads(test_client.get('/api/pokemon/').data)
    assert isinstance(respond, list)

    Pokemon


def test_post_new_pokemon(test_client):
    response = test_client.post('/api/pokemon/', json={"name": "ekans"})
    assert response.status_code == 201
    assert test_client.get('/api/pokemon/', json={"name": "ekans"})


def test_post_new_pokemon_which_doesnt_exist():
    pass


def test_post_new_pokemon_which_already_exists():
    pass


def test_post_new_pokemon_with_invalid_payload():
    pass


def test_post_new_encounter_if_server_message_is_emitted(capsys):
    pass


def test_post_new_encounter():
    pass


def test_post_new_encounter_with_invalid_payload():
    pass


def test_get_all_encounters():
    pass


def test_get_all_encounters_for_missing_id():
    pass


def test_if_other_http_methods_are_not_usable():
    pass
