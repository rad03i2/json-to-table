import csv, io
import pytest
from json_to_table import TableError, convert, normalize

def test_markdown_unicode_and_missing_values():
    data = [{"name":"Radwan","city":"Mosul"},{"name":"رضوان","active":True}]
    out = convert(data)
    assert "رضوان" in out and "true" in out and "active" in out

def test_flatten_nested_and_lists_remain_json():
    out = convert([{"user":{"name":"A"},"tags":["x","y"]}], "csv", flatten_nested=True)
    rows = list(csv.reader(io.StringIO(out)))
    assert rows[0] == ["user.name", "tags"]
    assert rows[1] == ["A", '["x","y"]']

def test_column_selection_and_order():
    out = convert([{"a":1,"b":2}], "csv", columns=["b","a"])
    assert out == "b,a\n2,1\n"

def test_html_escapes_untrusted_values():
    out = convert([{"x":"<script>alert(1)</script>"}], "html")
    assert "<script>" not in out and "&lt;script&gt;" in out

def test_markdown_escapes_pipe():
    assert "a\\|b" in convert([{"x":"a|b"}])

def test_empty_array():
    assert convert([], "markdown") == "(empty table)\n"

def test_reject_scalar_array():
    with pytest.raises(TableError): normalize([1,2,3])

def test_reject_unknown_column():
    with pytest.raises(TableError): convert([{"a":1}], columns=["missing"])

def test_reject_empty_separator_when_flattening():
    with pytest.raises(TableError): convert([{"a":{"b":1}}], flatten_nested=True, separator="")
