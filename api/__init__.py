from flask import Flask
from flask_restx import Api, Namespace
from flask_mongoengine import MongoEngine

app = Flask(__name__)
db = MongoEngine(app)

api = Api(app, title='PokemonAPI', description='Wrapper for https://pokeapi.co/')

pokemon_api = Namespace('Pokemons', description='Pokemon details', path='/api/pokemon/', validate=True)
encounter_api = Namespace('Encounters', description='Pokemon encounters', path='/pokemon/', validate=True)

api.add_namespace(pokemon_api)
api.add_namespace(encounter_api)
