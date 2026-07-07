from flask import Flask, jsonify

from config import NOME_SISTEMA, VERSAO


app = Flask(__name__)


@app.route("/")
def inicio():

    return jsonify({

        "sistema": NOME_SISTEMA,

        "versao": VERSAO,

        "status": "online"

    })


@app.route("/teste")
def teste():

    return jsonify({

        "mensagem": "BarberFlow funcionando!"

    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
