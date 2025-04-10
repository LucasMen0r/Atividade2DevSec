from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form.get("nome", "")
    email = request.form.get("email", "")
    senha = request.form.get("senha", "")

    erros = []

    if len(nome) < 3:
        erros.append("Nome deve ter pelo menos 3 caracteres.")
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        erros.append("Email inválido.")
    if not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", senha):
        erros.append("Senha fraca.")

    if erros:
        return "<br>".join(erros), 400
    return f"<h2>Sucesso, {nome}!</h2>"

if __name__ == '__main__':
    app.run(debug=True)