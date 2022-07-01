import os

from flask import Flask, render_template, request
from rest_backend import *

"""
IDEA PROGRAMU:
Użytkownik może wyszukać gracza o danym nicku w serwiasach lichess.com, chess.com i uzyskać dostępne statyski 
oraz najczęściej stosowane otwarcia szachowe 
(np. z ciekawości, albo w celu nauki gry otwarć kontrujących otwarcia przyszłego przeciwnika).

Na chess.com funkcjonalność wyświetlająca najczęstsze otwarcia jest za tzw. "paywallem", pobierając gry gracza możemy
wybrać pierwsze ruchy z rozgrywek i policzyć ich występowanie tym samym obchodząc paywall.   
Na lichess.com takiej funkcjonalności nie znalazłem.
"""


app = Flask(__name__, template_folder='templates')


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/user_stats", methods=["POST"])
def handle_stats_form():
    user_name = request.form["user_name"]
    lichess_data, chesscom_data = request_user_data(user_name)
    rendered_result = ""

    if lichess_data is not None:
        lichess_data["openings"] = lichess_mc_openings(user_name, n_games=request.form["n_games"])
        rendered_result += render_template("lichess_stats.html", **lichess_data)
    else:
        rendered_result += "<h1>Player not found on lichess</h1><br>"
    if chesscom_data is not None:
        chesscom_data["openings"] = asyncio.run(chesscom_mc_openings(user_name, n_months=int(request.form["n_months"])))
        rendered_result += render_template("chesscom_stats.html", **chesscom_data)
    else:
        rendered_result += "<h1>Player not found on chess.com</h1><br>"

    return rendered_result


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)
