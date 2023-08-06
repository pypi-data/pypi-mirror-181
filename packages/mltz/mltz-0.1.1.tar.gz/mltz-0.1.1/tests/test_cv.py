import pytest
from mltz import cv

def test_answer():
    assert 1 + 1 == 2
    assert cv.enhance_cross_validate(None,None,None)
    
def test_info():
    assert cv.getInfo() == "mltz"