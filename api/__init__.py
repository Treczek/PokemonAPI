from flask import Flask
from flask_restx import Api, Namespace
from flask_mongoengine import MongoEngine

app = Flask(__name__)
db = MongoEngine(app)

api = Api(app, title='PokemonAPI', description='Wrapper for https://pokeapi.co/')

pokemon = Namespace('Pokemon', description='Pokemon details', path='/api/pokemon/')
api.add_namespace(pokemon)

pokemon_encounters = Namespace('Encounters', description='Pokemon encounters', path='/pokemon/')
api.add_namespace(pokemon_encounters)



