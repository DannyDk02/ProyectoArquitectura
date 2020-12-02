'''
Script en el cual se realizan las acciones de la aplicación una vez haber iniciado sesion en la misma. Para esto se hizo uso de las 
siguientes funciones:
1. index(): Pagina principal en la cual se apreciaran los pedidos realizados por el usuario en caso de que los tenga junto con las opciones
de accion para lo mismo.
2. create(): Pagina en la cual se podra crear una orden en caso de desearlo o regresar al index.
3. get_pedido(): Revisa la informacion que se presente en el pedido tomando la información desde la base de datos.
4. update(): Pagina en la cual se podra modificar el pedido en caso de asi desearlo actualizando la información en la base de datos.
5. delete(): accion de ruta la cual se encargara de eliminar el pedido realizado por el usuario tanto de la aplicacion como de la base de 
datos.
6. pay(): pagina en la cual se podra confirmar el pedido realizado y seleccionar el metodo de pago para el mismo agregando esta ultima
información a la base de datos.
'''

from flask import (Blueprint, flash, g, render_template, request, url_for, redirect)
from werkzeug.exceptions import abort
from aplicacion.auth import login_require
from aplicacion.db import get_db

bp = Blueprint('aplicacion',__name__)

@bp.route('/')
@login_require
def index():
    db,c = get_db()
    c.execute('select p.id, p.description, u.username, p.delivered, p.created_at, p.amount from pedido p JOIN Usuario u on '
            'p.ordered_by = u.id where p.ordered_by=%s order by created_at desc',(g.user['id'],))
    pedidos = c.fetchall()
    return render_template('aplicacion/index.html', pedidos=pedidos)

@bp.route('/create',methods=['GET','POST'])
@login_require
def create():
    if request.method=="POST":
        description = request.form['description']
        amount = request.form['amount']
        error = None

        if not description:
            error = 'Descripcion es requerida'
        if error is not None:
            flash(error)
        else:
            db,c = get_db()
            c.execute('insert into pedido (ordered_by,description,amount,delivered)'
                    ' values (%s,%s,%s,%s)',(g.user['id'],description,amount,False))
        db.commit()
        return redirect(url_for('aplicacion.index'))

    return render_template('aplicacion/create.html')

def get_pedido(id):
    db,c = get_db()
    c.execute('select p.id, p.description, p.delivered, p.ordered_by, p.created_at, p.amount,' 
            ' u.username from Pedido p join Usuario u on p.ordered_by = u.id where p.id = %s',(id,))
    pedido = c.fetchone()
    if pedido is None:
        abort(404,'El todo de id {0} no existe'.format(id))
    return pedido

@bp.route('/<int:id>/update',methods=['GET','POST'])
@login_require
def update(id):
    pedido = get_pedido(id)
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        error = None

        if not amount:
            error = 'La cantidad es requerida'
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute('update Pedido set description = %s, amount = %s where id = %s and ordered_by = %s', (description, amount,id, g.user['id']))
            db.commit()
            return redirect(url_for('aplicacion.index'))
    return render_template('aplicacion/update.html',pedido=pedido)

@bp.route('/<int:id>/delete',methods=['POST'])
@login_require
def delete(id):
    db,c = get_db()
    c.execute('delete from Pedido where id = %s and ordered_by = %s',(id,g.user['id']))
    db.commit()
    return redirect(url_for('aplicacion.index'))

@bp.route('/<int:id>/pay',methods=['GET','POST'])
@login_require
def pay(id):
    pedido = get_pedido(id)
    if request.method == 'POST':
        pay_method = request.form['pay_method']
        delivered = True if request.form.get('delivered') == 'on' else False
        error = None

        if not pay_method:
            error = 'Metodo de pago requerido'
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute('update Pedido set pay_method = %s, delivered = %s where id = %s and ordered_by = %s', (pay_method, delivered,id, g.user['id']))
            db.commit()
            return redirect(url_for('aplicacion.index'))
    return render_template('aplicacion/pay.html',pedido=pedido)