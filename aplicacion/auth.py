'''
Script en el cual se realizan las acciones tipo API_REST para realizar acciones entre la aplicacion y la base de datos. Para esto se 
desarrollan las siguientes funciones:
1. register(): Genera la ruta de registro y analiza los datos enviados por el usuario con el fin de agregar al mismo a la base de datos.
2. login(): Genera la ruta de ingreso de sesion y analiza los datos enviados por el usuario con el fin de ingresar al aplicativo, esto gracias a
verificar su existencia en la base de datos.
3. load_logged_in_user(): Se asegura de cargar los datos del usuario el cual este ingresado en la sesión
4. loggin_require(): se asegura de realizar las acciones dentro de la aplicación simepre y cuando el usuario este loggeado en su cuenta.
5. logout(): Genera la ruta de cerrar sesion devolviendolo a la ruta principal de iniciar sesion.
'''

import functools
from flask import (Blueprint, flash, g, render_template, request, url_for, session, redirect)
from werkzeug.security import check_password_hash, generate_password_hash
from aplicacion.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        
        db,c = get_db()
        error = None

        c.execute('select id from Usuario where username = %s',(username,))
        if not username:
            error = 'Nombre de usuario es requerido'
        if not password:
            error = 'Contraseña de usuario es requerida'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)

        if error is None:
            c.execute('insert into Usuario (username, password, email, address, phone) values' 
                    '(%s,%s,%s,%s,%s)',(username, generate_password_hash(password),email,address,phone))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db,c = get_db()
        error = None

        c.execute('select * from Usuario where username = %s',(username,))
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña invalida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalida'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('aplicacion.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db,c = get_db()
        c.execute('select * from Usuario where id = %s', (user_id,))
        g.user = c.fetchone()

def login_require(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))