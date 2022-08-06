from models.db import db 
from models.user import User

class Event(db.Document):
    user = db.ReferenceField(User, required=True, reverse_delete_rule=db.CASCADE)
    title = db.StringField(required=True)
    description = db.StringField(max_length=1000)
    time = db.DateTimeField(required=True)
    public = db.BooleanField(default=False)
