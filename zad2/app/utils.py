import re


def get_opening(game):
    try:
        moves = game["pgn"].split("\n")[-2]  # skip metadata and get only the line with moves
        moves = re.findall("\. [\w|\d]+ ", moves)
        moves = [move.replace(". ", "") for move in moves]
        opening = " ".join(moves[:4])
        return opening
    except KeyError:
        return  # missing most important "pgn" field