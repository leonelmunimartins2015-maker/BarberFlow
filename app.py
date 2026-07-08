from flask import Flask, render_template, request
from config import NOME_SISTEMA, VERSAO

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/clientes")
def clientes():
    return render_template("clientes.html")


@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():

    nome = request.form["nome"]
    telefone = request.form["telefone"]

    return f"""
    <h1>Cliente cadastrado!</h1>
    <p>Nome: {nome}</p>
    <p>Telefone: {telefone}</p>
    <br>
    <a href="/clientes">Voltar</a>
    """


@app.route("/teste")
def teste():
    return {
        "sistema": NOME_SISTEMA,
        "versao": VERSAO,
        "status": "online"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
