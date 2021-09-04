from src.compile import *


def test_execute_code():
    rce = CodeExecutor()
    resp = rce.execute_code("python", 'print("Hello, World!")')
    resp2 = rce.execute_code("python", 'print("Hello, World!")')
    assert resp == resp2
