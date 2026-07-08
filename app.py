from flask import Flask, render_template, request
from config import NOME_SISTEMA, VERSAO
from firebase import iniciar_firebase
from datetime import datetime, timedelta

app = Flask(__name__)

db = iniciar_firebase()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/clientes")
def clientes():
    return render_template("clientes.html")


@app.route("/lista_clientes")
def lista_clientes():

    clientes = []

    if db:
        dados = db.collection("clientes").stream()

        for cliente in dados:
            clientes.append(cliente.to_dict())

    return render_template(
        "lista_clientes.html",
        clientes=clientes
    )


@app.route("/agenda")
def agenda():

    agendamentos = []

    if db:
        dados = db.collection("agendamentos").stream()

        for agendamento in dados:
            agendamentos.append(agendamento.to_dict())

    return render_template(
        "agenda.html",
        agendamentos=agendamentos
    )


@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():

    nome = request.form["nome"]
    telefone = request.form["telefone"]

    if db:
        db.collection("clientes").add({
            "nome": nome,
            "telefone": telefone,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

        mensagem = "Cliente salvo no Firebase!"

    else:
        mensagem = "Firebase não conectado."


    return f"""
    <h1>💈 {mensagem}</h1>
    <p>Nome: {nome}</p>
    <p>Telefone: {telefone}</p>
    <br>
    <a href="/clientes">Voltar</a>
    """


@app.route("/cadastrar_agendamento", methods=["POST"])
def cadastrar_agendamento():

    nome = request.form["nome"]
    servico = request.form["servico"]
    data = request.form["data"]
    hora = request.form["hora"]
    duracao = int(request.form["duracao"])


    if db:

        novo_inicio = datetime.strptime(
            f"{data} {hora}",
            "%Y-%m-%d %H:%M"
        )

        novo_fim = novo_inicio + timedelta(
            minutes=duracao
        )


        existentes = db.collection("agendamentos").stream()


        for item in existentes:

            ag = item.to_dict()


            if ag.get("data") == data:

                inicio_existente = datetime.strptime(
                    f"{ag['data']} {ag['hora']}",
                    "%Y-%m-%d %H:%M"
                )


                duracao_existente = int(
                    ag.get("duracao", 30)
                )


                fim_existente = inicio_existente + timedelta(
                    minutes=duracao_existente
                )


                if novo_inicio < fim_existente and novo_fim > inicio_existente:

                    return """
                    <h1>❌ Horário ocupado!</h1>
                    <p>Já existe um atendimento nesse período.</p>
                    <a href="/agenda">Voltar</a>
                    """


        db.collection("agendamentos").add({

            "nome": nome,
            "servico": servico,
            "data": data,
            "hora": hora,
            "duracao": duracao

        })


        mensagem = "Agendamento salvo!"


    else:

        mensagem = "Firebase não conectado."


    return f"""
    <h1>💈 {mensagem}</h1>

    <p>Cliente: {nome}</p>
    <p>Serviço: {servico}</p>
    <p>Data: {data}</p>
    <p>Horário: {hora}</p>
    <p>Duração: {duracao} minutos</p>

    <br>

    <a href="/agenda">
    Voltar para agenda
    </a>
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
