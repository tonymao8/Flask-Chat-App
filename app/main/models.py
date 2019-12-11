from datetime import datetime

from app import database

class Instance(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    chat_enabled = database.Column(database.Boolean, nullable=False, default=True)
    homepage_title = database.Column(database.String(200), default='Chat Application')
    homepage_hex_color = database.Column(database.String(6), default='ffd0cc')
    media_file = database.Column(database.String(200), nullable=False, default='default.jpg')
    media_file_is_default = database.Column(database.Boolean, nullable=False, default=True)
    media_is_video = database.Column(database.Boolean, nullable=False, default=False)
    page_views = database.Column(database.Integer, nullable=False, default=0)

class Message(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    date_posted = database.Column(database.String(30))
    name = database.Column(database.String(100), default='')
    content = database.Column(database.String(500), default='')

database.create_all()
database.session.commit()

# Creating an "Instance" model if there is none.
if Instance.query.get(1) is None:
    database.session.add(Instance())
    database.session.commit()