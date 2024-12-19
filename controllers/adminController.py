from models import *
from time import sleep
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, session, url_for, flash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=["GET", "POST"], endpoint="/admin/login")
def loginAdm():
    if request.method == "GET":
        return render_template('admin/login.html')
    

@admin_bp.route('/home', methods=["GET", "POST"], endpoint="/home")
def homeAdmin():
    if request.method == "GET":
        return render_template('admin/main.html')
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if email == "vh2g@mail.com":

            if senha == "1amazingCode1":
                session["id"] = 0
                session["nome"] = "vh2g"
                session["email"] = "vh2g@mail.com"
                session["senha"] = "1amazingCode1"
                return render_template("admin/main.html")
            
            else:
                return render_template('cliente/login.html')
        
        else:
            return render_template("cliente/login.html")

@admin_bp.route('/logout', methods=["GET"], endpoint="/logout")
def logoutAdmin():
    session.clear()
    return render_template("index.html")