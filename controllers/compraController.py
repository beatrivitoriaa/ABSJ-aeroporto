from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


compra_bp = Blueprint('compra', __name__)


@compra_bp.route('/home', methods=["GET"], endpoint="/home")
def home():
    return render_template("cliente/compra/main.html")


@compra_bp.route('/marcar', methods=["GET", "POST"], endpoint="/marcar")
def marcar():
    if request.method == "GET":
        return render_template("cliente/compra/marcar.html")
    if request.method == "POST":
        agente = request.form['agente']
        data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        preco = request.form['preco']

        consulta = Compra(agente, session['id'], preco, data)

        db.session.add(consulta)
        db.session.commit()

        return 'passagem comprada!'
    

@compra_bp.route('/marcadas', methods=["GET"], endpoint="/marcadas")
def marcadas():
    if request.method == "GET":
        compradas = Compra.query.all()
        return render_template("cliente/compra/getAll.html", compras=compradas)


@compra_bp.route('/remarca', methods=["GET"], endpoint="/remarca")
def remarca():
    if request.method == "GET":
        compras = Compra.query.filter_by()
        return render_template("cliente/compra/updateCenter.html", compras=compras)


@compra_bp.route('/remarcar', methods=["GET", "POST"], endpoint="/remarcar")
def remarcar():
    id = int(request.args.get('id'))
    
    compra = Compra.query.filter_by(id=id).first()
    print(id)
    print(compra)
    if request.method == "GET":
        return render_template("cliente/compra/update.html", compra=compra)
    if request.method == "POST":
        
        compra.id_agente = request.form['agente']
        compra.dataVenda = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        
        db.session.commit()
        return "remarcado com sucesso!"


@compra_bp.route('/cancelar', methods=["GET", "POST"], endpoint="/cancelar")
def cancelar():
    if request.method == "GET":
        compras = Compra.query.all()
        return render_template("cliente/compra/delete.html", compras = compras)
    if request.method == "POST":
        id = request.form['id']
        consulta = Compra.query.filter_by(id=id).first()
        db.session.delete(consulta)
        db.session.commit()

        return "cancelada com sucesso!"