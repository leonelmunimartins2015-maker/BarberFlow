from flask import Flask, render_template
from config import NOME_SISTEMA, VERSAO

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


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
