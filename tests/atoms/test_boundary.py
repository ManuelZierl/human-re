from human_re import Boundary, Not


def test_boundary_compile():
    assert Boundary().compile().pattern == "\b"


def test_not_boundary():
    assert Not(Boundary()).compile().pattern == "\B"
