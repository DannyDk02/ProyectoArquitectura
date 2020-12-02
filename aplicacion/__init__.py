'''
Script con el cual se realiza la asignación de valores para las variables de entorno con las cuales se conecta a la base de datos MYSQL
y se generan los blueprints adecuados para para generar las rutas a la hora de el desarrollo de procesos. Un hola mundo para saber de
vengo y hacia donde voy.
'''

import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='mikey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )

    from . import db
    db.init__app(app)

    from . import auth
    from . import aplicacion

    app.register_blueprint(auth.bp)
    app.register_blueprint(aplicacion.bp)

    @app.route('/hola')
    def hola():
        return 'Hola mundo'
    
    return app