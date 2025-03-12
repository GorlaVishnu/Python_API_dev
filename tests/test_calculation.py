from app.calculation import add

def test_add():
    print("testing add function")
    sum = add(5,6)
    assert sum == 8

test_add()
