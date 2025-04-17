import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_httpauth import HTTPBasicAuth
# carrega .env
load_dotenv()  
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
# Configuração do JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# Instâncias
login_manager = LoginManager(app)
login_manager.login_view = 'login'
jwt = JWTManager(app)
auth = HTTPBasicAuth()
# Cada usuário tem: id, nome, username, senha_hash
USERS = {
    1: {'nome': 'Alice', 'username': 'alice', 'password_hash': generate_password_hash('Senha123')},
    2: {'nome': 'Bob',   'username': 'bob',   'password_hash': generate_password_hash('Senha123')},
}
def get_user_by_username(username):
    for uid, data in USERS.items():
        if data['username'] == username:
            user = User()
            user.id = uid
            user.name = data['nome']
            user.password_hash = data['password_hash']
            return user
    return None

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    if int(user_id) in USERS:
        user = User()
        user.id = int(user_id)
        user.name = USERS[int(user_id)]['nome']
        return user
    return None

@auth.verify_password
def verify_password(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        return user
# — Página inicial com links para as três abordagens
@app.route('/')
def index():
    return render_template('login.html')
# — Sessão / Flask-Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password_hash, pwd):
            login_user(user)
            return redirect(url_for('dashboard'))
        return "Credenciais inválidas", 401
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
# — JWT / Token-based
@app.route('/jwt-login', methods=['GET','POST'])
def jwt_login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password_hash, pwd):
            token = create_access_token(identity=user.id)
            return jsonify(access_token=token)
        return jsonify(msg="Credenciais inválidas"), 401
    return render_template('jwt_login.html')

@app.route('/jwt-protected')
@jwt_required()
def jwt_protected():
    uid = get_jwt_identity()
    return jsonify(logged_in_as=USERS[uid]['nome'])
# — Basic HTTP Auth para API simples
@app.route('/basic-protected')
@auth.login_required
def basic_protected():
    return jsonify(mensagem=f"Olá, {auth.current_user().name}! Este é um recurso protegido.")

if __name__ == '__main__':
    app.run(debug=True)
