from models.db import db 

NAME_MIN_LENGTH = 4
NAME_MAX_LENGTH = 20

class User(db.Document):
    user_id = db.IntField()
    name = db.StringField(min_length=NAME_MIN_LENGTH,
                          max_length=NAME_MAX_LENGTH,
                          required=True)
    # hashed, obviously :)
    password = db.StringField(required=True)
    email = db.StringField()

    def to_json(self):
        return {"id": self.user_id,
                "name": self.name,
                "email": self.email}
