import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restx import Api

from api.encounter import encounter_api
from api.pokemon import pokemon_api
from api.utils import create_logger


def create_app(debug=False, test=False, logger=True, mongo_config=None):
    if logger:
        create_logger('PokemonAPI')

    app = Flask(__name__)

    # Setting MongoDB instance
    if mongo_config:
        app.config.update(mongo_config)

    app.config['TESTING'] = test
    app.config['DEBUG'] = debug

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
    app = create_app(mongo_config=dict(
                        MONGODB_HOST=f"mongodb+srv://{os.environ['mongo_user']}:{os.environ['mongo_password']}"
                                     f"@cluster0.eomnv.mongodb.net/PokemonAPI?retryWrites=true&w=majority",
                        MONGODB_ALIAS="pokemon_api",
                        MONGODB_DB='PokemonAPI'))
    app.run()
