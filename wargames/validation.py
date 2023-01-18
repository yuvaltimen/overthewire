

def validate_game(game: str) -> str:
    if game in {
        "bandit",
        "natas",
        "leviathan",
        "krypton",
        "narnia",
        "behemoth",
        "utumno",
        "maze",
        "vortex",
        "manpage",
        "drifter",
        "formulaone",
    }:
        return game
    else:
        raise Exception("No such game: " + game)
        