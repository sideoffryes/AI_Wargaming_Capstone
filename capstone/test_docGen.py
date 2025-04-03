import pytest

from docGen import gen


def test_navadmin_gen():
    doc = gen(2, 1, "Write me a NAVADMIN about the CNO retiring.", False)
    assert "NAVADMIN" in doc
    assert "CLASSIFICATION" in doc
    assert "SUBJ" in doc
    assert "REF" in doc
    
def test_opord_gen():
    doc = gen(2, 3, "Write me an OpOrd about an attack on the US Naval Academy.", False)
    assert "Orientation" in doc
    assert "Situation" in doc
    assert "Mission" in doc
    assert "Execution" in doc
    assert "Administration" in doc
    assert "Logistics" in doc
    assert "Command" in doc
    assert "Signal" in doc