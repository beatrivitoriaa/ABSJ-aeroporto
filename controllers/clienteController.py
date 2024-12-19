from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash


cliente_bp = Blueprint('cliente', __name__)
    

# rota para cliente/main.html, endpoint (oq aparece no navegador) "/"
@cliente_bp.route('/home', methods=["GET", "POST"], endpoint="/home")
def main():
    # se for um get, retorna a página cliente/main.html
    if request.method == "GET":
        return render_template('cliente/main.html')
    
    # se for um post, verifica o login
    if request.method == "POST":

        # salva o email passado no form
        emailCadastrado = request.form["email"]
        # salva a senha
        senha = request.form["senha"]
        # chama a função de login e salva a resposta na variável "res"
        res = login(emailCadastrado, senha)
        print(res)
        # se a resposta for 0, significa q deu tudo certo
        if res == 0:
            # busca o cliente pelo email fornecido (a senha foi verifcada na função login)
            cliente = Cliente.query.filter_by(email=emailCadastrado).first()
            # salva os dados na session
            session["id"] = cliente.id
            session["nome"] = cliente.nome
            session["nasc"] = cliente.nasc
            session["cpf"] = cliente.cpf
            session["telefone"] = cliente.telefone
            session["email"] = cliente.email
            session["senha"] = cliente.senha
            print(session)
            # retorna a página
            return render_template('cliente/main.html', cliente=session)

        # se a reposta for 6 significa q a senha está errada
        elif res == 6:
            return render_template('cliente/login.html')
            # fazer error na interface
    
        # 7 é cliente não cadastrado
        elif res == 7:
            return render_template('cliente/login.html')
        
        


# rota para cliente/login.html, endpoint (oq aparece no navegador) "/login"
@cliente_bp.route('/login', methods=["GET"], endpoint="/login")
def loginPage():
    # retorna a página cliente/login.html
    return render_template('cliente/login.html')



# rota para cliente/cadastro.html, endpoint (oq aparece no navegador) "/cadastro"
@cliente_bp.route('/cadastro', methods=["GET", "POST"], endpoint="/cadastro")
def cadastroCliente():
        # se for get, página
        if request.method == "GET":
            return render_template('cliente/cadastro.html')

        # se for post, cadastro
        if request.method == "POST":
            # salva dados do form - nome, data de nascimento, cpf, telefone, email e senha
            name = request.form["name"] 
            nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
            cpf = request.form["cpf"]
            telefone = request.form["telefone"]
            email = request.form["email"]
            senha = request.form["senha"]

            # adicionando dados ao Modelo criado anteriormente
            cliente = Cliente(name, nasc, cpf, telefone, email, senha)

            # adicionando mudanças ao banco de dados
            db.session.add(cliente)
            db.session.commit()

            # redireciona à pagina de login (achei melhor doq mandar pra main pq já testa o login tbm)
            return redirect(url_for('cliente./login'))



# rota para cliente/update.html, endpoint (oq aparece no navegador) "/atualizar"
@cliente_bp.route('/atualizar', methods=["GET", "POST"], endpoint="/atualizar")
def update():
    # se get, página
    if request.method == "GET":
        return render_template("cliente/update.html")
    # se post, update
    elif request.method == "POST":
        id = session['id']
        print(f"ID: {id}")
        res = updateById(id)
        print(f"RES: {res}")
        return render_template("cliente/update.html")
    


@cliente_bp.route('/deletar', methods=["POST"], endpoint="/deletar")
def deleteCliente():
    try:
        deleteById(session["id"])
        sleep(3)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        return str(e)
    

@cliente_bp.route("/logout", methods=["GET"], endpoint="/logout")
def logout():
    session.clear()
    return redirect(url_for('cliente./login'))
# rota para cliente/data.html, endpoint (oq aparece no navegador) "/data"
# basicamente, dá um get em todos os clientes cadastrados
# não existe como (o clientes) chegar nessa rota via interface 
@cliente_bp.route('/data')
def getAllClientes():
    clientes = Cliente.query.all()
    print(clientes)
    return render_template('cliente/getAll.html', clientes = clientes)


#
# FUNÇÕES DO CRUD E FUNCIONALIDADE (LOGIN)
#

# create Cliente | FEITO
def createCliente():
    try:
        # salvando dados do forms
        name = request.form["name"] 
        nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        
        # instanciando o modelo criado com os dados do usuário
        cliente = Cliente(name, nasc, cpf, telefone, email)
        cliente.senha= request.form["senha"]

        # adicionando mudanças ao banco de dados
        db.session.add(cliente)

        # commitando as alterações
        db.session.commit()


        return 0

    except:

        # status code, 1, se algo der errado (o que? não sabemos) 
        return render_template("cliente/cadastro.html")


# read all | FINALIZADA
def getAllClientes():
    try:
        clientes = Cliente.query.all()
        return clientes

    except:

        # status code, 2, se algo der errado (o que? não sabemos) 
        return 2


# update by id
def updateById(idCliente):
    
    try:
        cliente = Cliente.query.filter_by(id=idCliente).first()
        
        cliente.nome = request.form["name"]
        cliente.nasc = datetime.strptime(request.form["nasc"], "%Y-%m-%d").date()
        cliente.cpf = request.form["cpf"]
        cliente.telefone = request.form["telefone"]
        cliente.email = request.form["email"]
        cliente.senha = request.form["senha"]
            
        db.session.commit()

        session["nome"] = cliente.nome  
        session["nasc"] = cliente.nasc 
        session["cpf"] = cliente.cpf 
        session["telefone"] = cliente.telefone 
        session["email"] = cliente.email 
        session["senha"] = cliente.senha
        
        return 0
    
    except:
        return 4

# delete by id
def deleteById(id):
    
    try:
        cliente = Cliente.query.filter_by(id=id).first()
        print(cliente)
        db.session.delete(cliente)
        db.session.commit()
    
        return 0

    except:

        return 5
    

# login | FINALIZADA
def login(emailCadastrado, senha):
    try:
        cliente = Cliente.query.filter_by(email=emailCadastrado).one_or_none()
        
        if cliente is not None:
        
            isPasswordCorrect = (cliente.senha == senha)
        
            if isPasswordCorrect:        
                return 0

            else:
                isPasswordCorrect = False
                return 6
        
        else:
            return 7
        
    except Exception as e:
        print(f"Error: {e}")
        return 8
