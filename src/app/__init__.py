from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.py')

try:
    from app import models, views

    models.db.configure_mappers()
    models.db.create_all()
    models.db.session.commit()
except:
    import traceback
    traceback.print_exc()