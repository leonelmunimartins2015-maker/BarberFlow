from flask import Flask, render_template, request
from config import NOME_SISTEMA, VERSAO
from firebase import iniciar_firebase
from datetime import datetime, timedelta

app = Flask(__name__)

db = iniciar_firebase()


def pegar_configuracao():

    inicio = "11:00"
    fim = "18:00"

    if db:

        dados = db.collection("configuracoes").limit(1).stream()

        for item in dados:

            config = item.to_dict()

            inicio = config.get(
                "inicio_expediente",
                inicio
            )

            fim = config.get(
                "fim_expediente",
                fim
            )

    return inicio, fim



def pegar_agendamentos():

    lista = []

    if db:

        dados = db.collection("agendamentos").stream()

        for item in dados:

            ag = item.to_dict()

            lista.append(ag)

    return lista



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

    inicio, fim = pegar_configuracao()

    agendamentos = pegar_agendamentos()


    return render_template(
        "agenda.html",
        agendamentos=agendamentos,
        inicio_expediente=inicio,
        fim_expediente=fim
    )



@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():

    nome = request.form["nome"]
    telefone = request.form["telefone"]


    if db:

        db.collection("clientes").add({

            "nome": nome,
            "telefone": telefone,
            "data": datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )

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

    data_original = request.form["data"]

    data_obj = datetime.strptime(
        data_original,
        "%Y-%m-%d"
    )

    data = data_obj.strftime(
        "%d/%m/%Y"
    )


    hora = request.form["hora"]

    duracao = int(
        request.form["duracao"]
    )


    novo_inicio = datetime.strptime(
        f"{data} {hora}",
        "%d/%m/%Y %H:%M"
    )


    novo_fim = novo_inicio + timedelta(
        minutes=duracao
    )



    if db:


        existentes = pegar_agendamentos()


        for ag in existentes:


            if ag.get("data") == data:


                inicio_existente = datetime.strptime(
                    f"{ag['data']} {ag['hora']}",
                    "%d/%m/%Y %H:%M"
                )


                fim_existente = (
                    inicio_existente +
                    timedelta(
                        minutes=int(
                            ag.get("duracao",30)
                        )
                    )
                )


                if novo_inicio < fim_existente and novo_fim > inicio_existente:


                    return """
                    <h1>❌ Horário ocupado!</h1>
                    <p>Já existe atendimento nesse período.</p>
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
