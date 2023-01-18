import os
import json
import configparser
from pathlib import Path
from typing import Any, Dict, NamedTuple

from wargames.validation import validate_game
from wargames import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_PATH = Path.home() / "wargames_database/"

def get_database_path(config_file: Path) -> Path:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    try:
        db_path.mkdir(exist_ok=True)
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    response: Any
    error: int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
    
    def read(self, level: str, game: str = None) -> DBResponse:
        _GAME = None
        if game:
            _GAME = validate_game(game)
        else:
            _GAME = os.environ['WARGAMES_CURRENT_GAME']
        try:
            with self._db_path.open("r") as db:
                try:
                    full_read = json.load(db)
                    return DBResponse(full_read, SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse({}, JSON_ERROR)
        except OSError:
            return DBResponse({}, DB_READ_ERROR)
        
    def write(self, level_info: Dict[str, Any]) -> DBResponse:
        full_read, error = self.read()
        level, passwd, description = level_info
        full_read['games']['bandit']['levels'][level] = level_info
        try:
            with self._db_path.open("w") as db:
                json.dump(full_read, db)
                return DBResponse(level_info, SUCCESS)
        except OSError:
            return DBResponse(level_info, DB_WRITE_ERROR)
            