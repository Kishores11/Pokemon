# from flask import Flask


# app = Flask(__name__)
# app.config.from_pyfile('config.py')

# try:
#     from app import models, views

#     models.db.configure_mappers()
#     # models.db.create_all()
#     # models.db.session.commit()
# except:
#     import traceback
#     traceback.print_exc()


from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    return app

app = create_app()

try:
    from app import models, views
    models.db.configure_mappers()
    # models.db.create_all()
    # models.db.session.commit()
except Exception as e:
    import traceback
    traceback.print_exc()