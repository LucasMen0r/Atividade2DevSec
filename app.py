from flask import Flask, render_template, request, session, redirect, url_for, abort
import re
from functools import wraps
from datetime import datetime
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

MAC_LEVELS = {
    'admin': 3,
    'gerente': 2,
    'usuario': 1
}
PBAC_POLICIES = {
    'admin_area': {
        'roles':      ['admin'],       # Apenas admins
        'start_hour': 8,               # das 08h
        'end_hour':   18,              # até 18h
        'allowed_ip': '127.0.0.1'      # simulado
    },
    'gerente_area': {
        'roles':      ['admin', 'gerente'],
        'start_hour': 7,
        'end_hour':   20,
        'allowed_ip': '127.0.0.1'
    }
}
USERS = {
    'joao@example.com':  {'nome': 'João',  'senha': 'Senha123', 'role': 'admin'},
    'maria@example.com': {'nome': 'Maria', 'senha': 'Senha123', 'role': 'gerente'},
    'jose@example.com':  {'nome': 'José',  'senha': 'Senha123', 'role': 'usuario'}
}
def require_access(area_name):
    """
    Decorator que aplica MAC (role) e PBAC (horário + IP).
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Verifica autenticação
            if 'email' not in session:
                return redirect(url_for('index'))
            user = USERS.get(session['email'])
            if not user:
                abort(403)

            policy = PBAC_POLICIES[area_name]
            role   = user['role']
            now_h  = datetime.now().hour
            ip     = request.remote_addr

            # 1) Verifica papel (MAC)
            if role not in policy['roles']:
                return "Acesso negado: papel sem permissão", 403
            # 2) Verifica horário (PBAC)
            if not (policy['start_hour'] <= now_h < policy['end_hour']):
                return "Acesso negado: fora do horário permitido", 403
            # 3) Verifica IP (PBAC)
            if ip != policy['allowed_ip']:
                return f"Acesso negado: IP não autorizado ({ip})", 403

            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome  = request.form.get('nome', '')
    email = request.form.get('email', '')
    senha = request.form.get('senha', '')

    erros = []
    if len(nome) < 3:
        erros.append('Nome deve ter pelo menos 3 caracteres.')
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        erros.append('Email inválido.')
    if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha):
        erros.append('Senha fraca.')

    if erros:
        return '<br>'.join(erros), 400

    # Autenticação simples
    user = USERS.get(email)
    if user and user['senha'] == senha:
        session['email'] = email
        return (
            f"<h2>Bem-vindo, {user['nome']}!</h2>"
            "<a href='/admin'>Área Admin</a><br>"
            "<a href='/gerente'>Área Gerente</a><br>"
            "<a href='/logout'>Sair</a>"
        )
    return 'Credenciais inválidas', 401

@app.route('/admin')
@require_access('admin_area')
def admin_area():
    return '<h3>🔒 Área restrita: Admin</h3>'

@app.route('/gerente')
@require_access('gerente_area')
def gerente_area():
    return '<h3>🔒 Área restrita: Gerente ou Admin</h3>'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
