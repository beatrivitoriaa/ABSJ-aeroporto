from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


agente_bp = Blueprint('agente', __name__)


# rota para cliente/main.html, endpoint (oq aparece no navegador) "/"
@agente_bp.route('/home', methods=["GET", "POST"], endpoint="/home")
def main():
    if request.method == "GET":
        return render_template('admin/doctor/main.html')
        

# rota para cliente/cadastro.html, endpoint (oq aparece no navegador) "/cadastro"
@agente_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastroAgente():
        # se for get, página
        if request.method == "GET":
            return render_template('admin/doctor/cadastro.html')

        # se for post, cadastro
        if request.method == "POST":
            # salva dados do form - nome, data de nascimento, cpf, telefone, email e senha
            name = request.form["name"] 
            nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
            salario = request.form["salario"]
            cpf = request.form["cpf"]
            telefone = request.form["telefone"]
            crmv = request.form["crmv"]
            email = request.form["email"]
            dataContratacao = request.form["contratacao"]
            dataContratacao = datetime.strptime(request.form["contratacao"], "%Y-%m-%d").date()
            senha = ""

            # adicionando dados ao Modelo criado anteriormente
            agente = Agente(name, nasc, salario, cpf, telefone, crmv, email, dataContratacao, senha)

            # adicionando mudanças ao banco de dados 
            db.session.add(agente)
            db.session.commit()
            return render_template("admin/doctor/cadastro.html")


# rota para cliente/update.html, endpoint (oq aparece no navegador) "/atualizar"
@agente_bp.route('/atualiza', methods=["GET", "POST"], endpoint="/atualiza")
def update():
    # se get, página
    if request.method == "GET":
        agentes = getAllAgentes()
        return render_template("admin/doctor/updateCenter.html", agentes=agentes)
    


# rota para cliente/update.html, endpoint (oq aparece no navegador) "/atualizar"
@agente_bp.route('/atualizar', methods=["GET", "POST"], endpoint="/atualizar")
def update():
    # se get, página
    if request.method == "GET":
        id = int(request.args.get('id'))
        print(id)
        agente = Agente.query.filter_by(id=id).first()
        return render_template("admin/doctor/update.html", agente=agente)
    # se post, update
    elif request.method == "POST":
        cpf = request.form["cpf"]
        print(f'POST CPF {cpf}')
        agente = Agente.query.filter_by(cpf=cpf).first()
        print(f"POST MEDICO: {agente}")
        id = agente.id
        print(f"POST ID: {id}")
        res = updateById(id)
        print(f"RES: {res}")
        if res == 0:
            return render_template("admin/doctor/update.html", agente=agente)
        else:

            return render_template("admin/doctor/update.html", agente= agente)
    

@agente_bp.route('/deletar', methods=["GET", "POST"], endpoint="/deletar")
def deleteAgente():
    if request.method == "GET":
        agentes = Agente.query.all()
        return render_template("admin/doctor/delete.html", agentes=agentes)
    try:
        deleteById(request.form['id'])
        agentes = Agente.query.all()
        return render_template("admin/doctor/delete.html", agentes=agentes) 
    except Exception as e:
        print(e)
        return str(e)
    

# rota para cliente/data.html, endpoint (oq aparece no navegador) "/data"
# basicamente, dá um get em todos os Agentees cadastrados
# não existe como (o Agente) chegar nessa rota via interface 
@agente_bp.route('/data', methods=["GET"], endpoint="/data")
def getAllAgentes():
    agentes = getAllAgentes()
    return render_template('admin/doctor/getAll.html', agentes = agentes)


#
# FUNÇÕES DO CRUD E FUNCIONALIDADE (LOGIN)
#

# create Agente | FEITO
def createAgente():
    try:
        # salvando dados do forms
        nome = request.form["nome"]
        nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        salario = request.form["salario"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        crmv = request.form["crmv"]
        email = request.form["email"]
        dataContratacao = request.form["contratacao"]
        senha = ""
        
        # instanciando o modelo criado com os dados do usuário
        agente = Agente(nome, nasc, salario, cpf, telefone, crmv, email, dataContratacao, senha)
        
        # adicionando mudanças ao banco de dados
        db.session.add(agente)

        # commitando as alterações
        db.session.commit()


        return 0

    except:

        # status code, 1, se algo der errado (o que? não sabemos) 
        return render_template("cliente/cadastro.html")


# read all | FINALIZADA
def getAllAgentes():
    try:
        Agentes = Agente.query.all()
        return Agentes

    except:

        # status code, 2, se algo der errado (o que? não sabemos) 
        return 2


# update by id
def updateById(idAgente):
    
    try:
        agente = Agente.query.filter_by(id=idAgente).first()
        
        agente.nome = request.form["nome"]
        agente.nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        agente.salario = request.form["salario"]
        agente.cpf = request.form["cpf"]
        agente.telefone = request.form["telefone"]
        agente.crmv = request.form["crmv"]
        agente.email = request.form["email"]
        agente.dataContratacao = datetime.strptime(request.form["contratacao"], "%Y-%m-%d").date()
        agente.senha = ""

        db.session.commit()
        
        return 0
    
    except Exception as e:
        print(f"Exception: {e}")
        return 4

# delete by id
def deleteById(id):
    
    try:
        agente = Agente.query.filter_by(id=id).first()
        db.session.delete(agente)
        db.session.commit()
    
        return 0

    except:

        return 5
    
