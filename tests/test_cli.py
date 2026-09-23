import json
from json_to_table.cli import main

def test_cli_file_to_output(tmp_path):
    source = tmp_path / "input.json"
    target = tmp_path / "out.csv"
    source.write_text(json.dumps([{"id":1,"name":"A"}]), encoding="utf-8")
    assert main([str(source), "-f", "csv", "-o", str(target)]) == 0
    assert target.read_text(encoding="utf-8") == "id,name\n1,A\n"

def test_cli_bad_json(tmp_path, capsys):
    source = tmp_path / "bad.json"
    source.write_text("{bad", encoding="utf-8")
    assert main([str(source)]) == 2
    assert "error:" in capsys.readouterr().err

def test_cli_unknown_column(tmp_path, capsys):
    source = tmp_path / "input.json"
    source.write_text('[{"a":1}]', encoding="utf-8")
    assert main([str(source), "--columns", "x"]) == 2
    assert "unknown column" in capsys.readouterr().err
