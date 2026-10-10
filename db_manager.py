import os,sys
base_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(base_path,".."))
from flask_app_provider import db, app

class Go_user(db.Model):
    uid = db.Column(db.String(80), primary_key=True)
    game = db.Column(db.String(1<<13),unique=False,nullable=False)
    settings = db.Column(db.String(256),unique=False,nullable=False)
    last_access = db.Column(db.Integer,unique=False,nullable=False)

with app.app_context():
    db.create_all()
