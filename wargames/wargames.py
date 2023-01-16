from pathlib import Path
from typing import Any, Dict, NamedTuple
from jsonschema import validate

from wargames import DB_READ_ERROR
from wargames.database import DatabaseHandler

class LevelSolutionInfo(NamedTuple):
    details: Dict[str, Any]
    error: int


    
class WargamesController:
    def __init__(self, db_path: Path):
        self._db_handler = DatabaseHandler(db_path)
        
    def add(self, level_info: Dict[str, Any]) -> LevelSolutionInfo:
        print(level_info)
        write = self._db_handler.write(level_info)
        return LevelSolutionInfo(level_info, write.error)
    
    def read(self) -> LevelSolutionInfo:
        read = self._db_handler.read()
        return LevelSolutionInfo(read.level_info, read.error)
    