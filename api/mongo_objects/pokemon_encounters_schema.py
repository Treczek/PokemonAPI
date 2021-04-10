from api import db
from datetime import datetime


class PokemonEncounter(db.Document):

    note = db.StringField()
    place = db.StringField(required=True)

    @property
    def timestamp(self):
        return int(datetime.timestamp(self.id.generation_time)) if self.id else None
