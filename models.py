from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# classe médico
class Agente(db.Model):
    # nome da tabela
    __tablename__ = "Agente"
    # id do médico - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # nome do médico - string/varchar de 40 caracteres, não nulo/not null 
    nome = db.Column(db.String(40), nullable=False)
    # nascimento do médico - tipo Date, not null/não nulo
    nasc = db.Column(db.Date, nullable=False)
    # salário do médico - tipo Float, not null
    salario = db.Column(db.Float, nullable=False)
    # cpf do médico - string/varchar de 11 caracteres, unique key (chave única)
    cpf = db.Column(db.String(11), unique=True)
    # telefone do médico - string de 11 caracteres, unique key
    telefone = db.Column(db.String(11), unique=True)
    # email do médico - string de 255 caracteres, unique key
    email = db.Column(db.String(255), unique=True)
    # data de contratação do médico, Date, not null
    dataContratacao = db.Column(db.Date, nullable=False)
    # senha para login - varchar(20), not null
    senha = db.Column(db.String(20), nullable=False)

    def __init__(self, nome, nasc, salario, cpf, telefone, email, dataContratacao, senha):
        self.nome = nome
        self.nasc = nasc
        self.salario = salario
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.dataContratacao = dataContratacao
        self.senha = senha

# Classe tutor
class Cliente(db.Model):
    # nome da tabela
    __tablename__ = "Cliente"
    # id do tutor - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # nome do tutor - string de 40 caracteres, not null
    nome = db.Column(db.String(40), nullable=False)
    # nascimento do tutor - tipo Date, not null/não nulo
    nasc = db.Column(db.DateTime, nullable=False)
    # cpf do tutor - string/varchar de 11 caracteres, unique key (chave única)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    # telefone do tutor - string de 11 caracteres, unique key
    telefone = db.Column(db.String(11), unique=True, nullable=False)
    # email do tutor - string de 255 caracteres, unique key
    email = db.Column(db.String(255), unique=True, nullable=False)
    # senha para login - varchar(20), not null
    senha = db.Column(db.String(128), nullable=True)

    def __init__(self, nome, nasc, cpf, telefone, email, senha):
        self.nome = nome
        self.nasc = nasc
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha

class Dependente(db.Model):
    # nome da tabela
    __tablename__ = "Dependente"
    # id do pet - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # nome do pet - string de 40 caracteres, not null
    nome = db.Column(db.String(40), nullable=False)
    # nascimento do pet - tipo Date, not null/não nulo
    nasc = db.Column(db.DateTime, nullable=False)
    # id do dono do pet - int, not null, Foreign Key (FK)
    id_tutor = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    
    def __init__(self, nome, nasc, id_tutor):
        self.nome = nome
        self.nasc = nasc
        self.id_tutor = id_tutor

class Passagem(db.Model):
    # nome da tabela
    __tablename__ = "Passagem"
    # id do médico - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # nome do produto
    voo = db.Column(db.String(255), nullable=False)
    # preço do produto
    preco = db.Column(db.Float, nullable=False)
    # quantidade disponível
    dataViagem = db.Column(db.Integer, nullable=False)

    def __init__(self, nome, preco, qtd_disponivel):
        self.nome = nome
        self.preco = preco
        self.qtd_disponivel = qtd_disponivel
    
class Compra(db.Model):
    # nome da tabela
    __tablename__ = "Compra"
    # id do médico - inteiro, primary key, autoincrement 
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    # id do médico - inteiro, foreign key, autoincrement - referencia o id na tabela médico 
    id_agente = db.Column(db.Integer, db.ForeignKey('Agente.id'), nullable=False)
    # id do pet - inteiro, foreign key, autoincrement - referencia o id na tabela animal
    id_cliente = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    # valor pago pela consulta - float, not null 
    id_passagem = db.Column(db.Integer, db.ForeignKey('Passagem.id'), nullable=False)
    # data da consulta - date, not null
    dataVenda = db.Column(db.Date, nullable=False)

    def __init__(self, id_agente, id_cliente, id_passagem, dataVenda):
        self.id_agente = id_agente
        self.id_cliente = id_cliente
        self.id_passagem = id_passagem
        self.dataVenda = dataVenda
