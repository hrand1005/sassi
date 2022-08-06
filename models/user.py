from models.db import db 

class User(db.Document):
    name = db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.StringField(unique=True, required=True)
