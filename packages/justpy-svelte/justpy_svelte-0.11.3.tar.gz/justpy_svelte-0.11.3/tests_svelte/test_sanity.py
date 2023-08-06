import pytest
import justpy as jp


def test_import_justpy():
    import_succeded = False
    try:
        import justpy

        import_succeded = True
    except:
        pass
    assert import_succeded


test_import_justpy()
