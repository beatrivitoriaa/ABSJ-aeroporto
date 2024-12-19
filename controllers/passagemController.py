from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


passagem_bp = Blueprint('passagem', __name__)

@passagem_bp.route('/home', methods=["GET"], endpoint="/home")
def home():
    return render_template("admin/passagens/main.html")

@passagem_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastro():
    if request.method == "GET":
        return render_template("admin/passagens/cadastro.html")
    if request.method == "POST":
        res = createPassagem()
        if res == 0:
            return render_template("admin/passagens/cadastro.html")
        else:
            return render_template("admin/passagens/cadastro.html")


@passagem_bp.route('/data', methods=["GET"], endpoint="/data")
def getAll():
    passagens = Passagem.query.all()
    return render_template('admin/passagens/getAll.html', passagens=passagens)


@passagem_bp.route('/atualiza', methods=["GET"], endpoint="/atualiza")
def atualiza():
    if request.method == "GET":
        passagens = Passagem.query.all()
        return render_template('admin/passagens/updateCenter.html', passagens=passagens)

@passagem_bp.route('/atualizar', methods=["GET", "POST"], endpoint="/atualizar")
def atualizar():
    try:
        if request.method == "GET":
            id = int(request.args.get('id'))
            passagem = Passagem.query.filter_by(id=id).first()
            return render_template('admin/passagens/update.html', passagem=passagem)
        if request.method == "POST":
            id = request.form['id']
            passagem = Passagem.query.filter_by(id=id).first()
            
            passagem.nome = request.form['nome']
            passagem.preco = request.form['preco']
            passagem.estoque = request.form['estoque']

            db.session.commit()

            return render_template('admin/passagens/update.html', passagem=passagem)
        
    except Exception as e:
        print(f"ERRO {e}")
        return render_template('admin/passagens/update.html')


@passagem_bp.route('/deletar', methods=["GET", "POST"], endpoint="/deletar")
def deletar():
    try:
        if request.method == "GET":
            passagens = Passagem.query.all()
            return render_template('admin/passagens/delete.html', passagens=passagens)
        if request.method == "POST":
            id = int(request.form['id'])
            res = deleteById(id)
            print(f'RES: {res}')
            passagens = Passagem.query.all()
            return render_template('admin/passagens/delete.html', passagens=passagens)
                  
    except Exception as e:
        print(f"ERROR: {e}")
        return render_template('admin/passagens/delete.html')

            
def createPassagem():
    try:
        voo = request.form["voo"]
        preco = request.form["preco"]
        dataViagem = request.form["dataViagem"]

        passagem = Passagem(voo, preco, dataViagem)

        db.session.add(passagem)
        db.session.commit()

        return 0
    
    except Exception as e:
        print(f"error: {e}")
        return 5
    

def deleteById(id):
    try:
        passagem = Passagem.query.filter_by(id=id).first()
        
        db.session.delete(passagem)
        db.session.commit()

        return 0
    
    except Exception as e:
        print(e)
        return 10