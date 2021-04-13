import os
from app import create_app

mongo_config = dict(MONGODB_HOST=f"mongodb+srv://{os.environ['mongo_user']}:{os.environ['mongo_password']}"
                                 f"@cluster0.eomnv.mongodb.net/PokemonAPI?retryWrites=true&w=majority",
                    MONGODB_ALIAS="pokemon_api",
                    MONGODB_DB='PokemonAPI')

app = create_app(mongo_config=mongo_config)
