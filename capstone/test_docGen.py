import pytest
from docGen import gen

def test_navadmin_gen():
    doc = gen(2, 1, "Write me a NAVADMIN about the CNO retiring.", False)
    assert "NAVADMIN" in doc
    assert "CLASSIFICATION" in doc
    assert "SUBJ" in doc
    assert "REF" in doc