import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restx import Api

from api.encounter import encounter_api
from api.pokemon import pokemon_api
from api.utils import create_logger


def create_app(logger=True, mongo_config=None):
    if logger:
        create_logger('PokemonAPI')

    app = Flask(__name__)

    # Setting MongoDB instance
    if mongo_config:
        app.config.update(mongo_config)

    MongoEngine(app)

    api = Api(app,
              title='PokemonAPI',
              description='Wrapper for https://pokeapi.co/',
              contact_email='tomek.reczek@gmail.com')

    api.add_namespace(pokemon_api)
    api.add_namespace(encounter_api)

    return app


if __name__ == '__main__':
    create_logger('PokemonAPI')
    app = create_app()
    app.run(debug=True)
