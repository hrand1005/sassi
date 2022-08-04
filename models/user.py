from models.db import db 
from typing import Type

class User(db.Document):
    user_id = db.IntField()
    name = db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.StringField(unique=True, required=True)
