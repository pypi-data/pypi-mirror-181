import pytest
import justpy


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
    import justpy as jp

    app = jp.build_app()
    assert app is not None


def test_addroute():
    app = jp.build_app()
    from starlette.responses import PlainTextResponse

    def plaintext(request):
        return PlainTextResponse("Plaintext")

    app.router.add_route("/plaintext", plaintext, "plaintext")

    print("pls print", app.router.routes)
    assert app.router.routes is None
