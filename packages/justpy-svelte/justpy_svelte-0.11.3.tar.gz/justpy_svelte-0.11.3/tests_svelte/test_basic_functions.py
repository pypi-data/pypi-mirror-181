import pytest
import justpy as jp


def test_import_justpy():
    import_succeded = False
    try:
        import justpy

        import_succeded = True
    except Exception as e:
        print(e)
        pass
    assert import_succeded


def test_build_app():
    app = jp.build_app()
    assert app is not None


@pytest.fixture
def jpapp():
    app = jp.build_app()
    return app


def test_addroute():
    app = jp.build_app()
    from starlette.responses import PlainTextResponse

    def plaintext(request):
        return PlainTextResponse("Plaintext")

    app.router.add_route("/plaintext", plaintext, "plaintext")

    print("pls print", app.router.routes)
    assert app.router.routes is not None


def test_justpy_func(jpapp):
    def jpfunc(request):
        wp = jp.WebPage()
        return wp

    pre_add_route_count = len(jpapp.router.routes)
    jpapp.add_jproute("/", jpfunc)

    assert len(jpapp.router.routes) == pre_add_route_count + 1
