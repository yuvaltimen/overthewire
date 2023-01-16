import json
import pytest
from typer.testing import CliRunner
from wargames import (
    DB_READ_ERROR,
    __app_name__,
    __version__,
    cli,
    wargames,
)

runner = CliRunner()


@pytest.fixture
def mock_json_file(tmp_path):
    level_info = {"level": "1", "description": "Here's how I solved it...", "passwd": "12345"}
    db_file = tmp_path / "warmgames.json"
    with db_file.open("w") as db:
        json.dump(level_info, db)
        return db_file
    

def test_version():
    result = runner.invoke(cli.app, ['--version'])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
    
    
def test_add(mock_json_file, level, description, passwd, expected):
    controller = wargames.WargamesController(mock_json_file)
    assert controller.add(level, description, passwd) == expected
    read = controller._db_handler.get_level_info()
    print(f"TODO: write assert for: {read}")
    
    
    
    