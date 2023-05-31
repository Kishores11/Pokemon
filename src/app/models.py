from app import app
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db, compare_type=True)


@dataclass
class Pokemon(db.Model):
    rank: int = db.Column(db.Integer, nullable=False)
    name: str = db.Column(db.Text, primary_key=True)
    type_1: str = db.Column(db.Text, nullable=False)
    type_2: str = db.Column(db.Text, nullable=True)
    total: str = db.Column(db.Text, nullable=False)
    hp: str = db.Column(db.Text, nullable=False)
    attack: str = db.Column(db.Text, nullable=False)
    defence: str = db.Column(db.Text, nullable=False)
    # sp_atk: str = db.Column(db.Text, nullable=False)
    # sp_def: str = db.Column(db.Text, nullable=False)
    speed: str = db.Column(db.Text, nullable=False)
    generation: str = db.Column(db.Text, nullable=False)
    legendary: str = db.Column(db.Text, nullable=False)
