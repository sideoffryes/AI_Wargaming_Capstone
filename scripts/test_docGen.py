import pytest
from docGen import gen

def test_navadmin_gen():
    doc = gen("meta-llama/Llama-3.2-1B-Instruct", "NAVADMIN", "Write me a NAVADMIN about the CNO retiring.")
    assert "NAVADMIN" in doc