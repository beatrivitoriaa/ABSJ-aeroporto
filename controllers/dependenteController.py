from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for


dependente_bp = Blueprint('dependente', __name__)


# rota p main
@dependente_bp.route("/", methods=["GET"], endpoint="/")
def main():
    return render_template("cliente/dependente/main.html")


# rota para cliente/cadastro.html, endpoint (oq aparece no navegador) "/cadastro"
@dependente_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastroCliente():
        # se for get, página
        if request.method == "GET":
            return render_template('cliente/dependente/cadastro.html')

        # se for post, cadastro
        if request.method == "POST":
            # salva dados do form - nome, data de nascimento, cpf, telefone, email e senha
            name = request.form["name"] 
            nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
            id_cliente = session["id"]

            # adicionando dados ao Modelo criado anteriormente
            dependente = Dependente(name, nasc, id_cliente)

            # adicionando mudanças ao banco de dados
            db.session.add(dependente)
            db.session.commit()

            # redireciona à pagina de login (achei melhor doq mandar pra main pq já testa o login tbm)
            return render_template('cliente/dependente/cadastro.html')


# rota para cliente/update.html, endpoint (oq aparece no navegador) "/atualizar"
@dependente_bp.route('/atualiza', methods=["GET"], endpoint="/atualizar")
def updateCenter():
    # se get, página
    dependentes = Dependente.query.filter_by(id_tutor=session['id']).all()
    print(dependentes)
    print(session["id"])
    if request.method == "GET":
        return render_template("cliente/dependente/updateCenter.html", dependentes=dependentes)
    # se post, update


@dependente_bp.route('/atualizarDependente', methods=["GET", "POST"], endpoint='/atualizarDependente')
def update():
    
    if request.method == "GET":
        dependente_id = int(request.args.get('dependente_id'))
        print(f"PET ID: {dependente_id}")
        dependente = Dependente.query.filter_by(id=dependente_id).first()
        print(dependente)
        return render_template('cliente/dependente/update.html', dependente=dependente)
    
    if request.method == "POST":
        dependente_id = request.args.get('id')
        print(f"PET ID POST: {dependente_id}")
        res = updateById(dependente_id)
        print(res)
        dependente = Dependente.query.filter_by(id=dependente_id).first()
        return render_template("cliente/dependente/update.html", dependente=dependente)


@dependente_bp.route('/deletar', methods=["GET", "POST"], endpoint="/deletar")
def deleteCliente():
        
    dependentes = Dependente.query.filter_by(id_tutor=session['id'])
    if request.method == "GET":
        return render_template("cliente/dependente/deleteCenter.html", dependentes = dependentes)
    
    if request.method == "POST":
        dependente_id = request.form["id"]
        res = deleteById(dependente_id)
        print(res)
        return render_template("cliente/dependente/deleteCenter.html")
    

# rota para cliente/data.html, endpoint (oq aparece no navegador) "/data"
# basicamente, dá um get em todos os clientes cadastrados
# não existe como (o cliente) chegar nessa rota via interface 
@dependente_bp.route('/data')
def getAllTutires():
    dependentes = Dependente.query.all()
    return render_template('cliente/dependente/getAll.html', dependentes = dependentes)





# create Dependente | FINALIZADA
def createDependente():
    try:
        # salvando dados do forms
        nome = request.form["name"] 
        nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        tipo = request.form["tipo"]
        raca = request.form["raca"]
        altura = request.form["altura"]
        id_tutor = session["id"]
        
        # instanciando o modelo criado com os dados do usuário
        dependente = Dependente(nome, nasc, tipo, raca, altura, id_tutor)

        # adicionando mudanças ao banco de dados
        db.session.add(dependente)

        # commitando as alterações
        db.session.commit()


        return 0

    except:

        # status code, 1, se algo der errado (o que? não sabemos) 
        return render_template("cliente/cadastro.html")


# read all | FINALIZADA
def getAllDependente():
    try:
        Dependentes = Dependente.query.all()
        return Dependentes

    except:

        # status code, 2, se algo der errado (o que? não sabemos) 
        return 2

def getDependentesByClienteId(id):
    try:
        dependentes = Dependente.query.filter_by(id_tutor=id)
        print(dependentes)
        return dependentes
    except:
        return 10
# update by id
def updateById(id):
    
    try:
        dependente = Dependente.query.filter_by(id=id).first()
        
        dependente.nome = request.form["name"]
        dependente.nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
            
        db.session.commit()
        
        return 0
    
    except:
        return 4

# delete by id
def deleteById(id):
    
    try:
        dependente = Dependente.query.filter_by(id=id).first()
        print(dependente)
        db.session.delete(dependente)
        db.session.commit()
    
        return 0

    except:

        return 5
    
