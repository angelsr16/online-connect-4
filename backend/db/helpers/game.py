from typing import List


def game_helper(game: dict) -> dict:
    return {
        "id": str(game["_id"]),
        "player_1": game["player_1"],
        "player_2": game["player_2"] if game["player_2"] is not None else None,
        "game_state": game["game_state"],
        "status": game["status"],
        "moves": game["moves"],
        "created_at": game["created_at"],
        "join_code": game["join_code"],
        "current_turn": (
            str(game["current_turn"]) if game["current_turn"] is not None else None
        ),
        "winner": game["winner"],
    }


def games_helper(games):
    games_list = []
    for current_game in games:
        game = game_helper(current_game)
        games_list.append(game)
    return games_list
