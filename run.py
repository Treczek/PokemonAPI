from api import app
from api.routes import Pokemons, Encounters
from api.utils import create_logger

if __name__ == '__main__':
    create_logger('PokemonAPI')
    app.run(debug=True)
