import justpy as jp

@jp.app.route("/greet/{name}")
@jp.app.response
def greeting_function(request):
    wp = jp.WebPage(template_file="svelte.html")
    name = f"""{request.path_params["name"]}"""
    wp.add(jp.P(text=f"Hello there, {name}!", classes="text-5xl m-2"))
    return wp


from starlette.testclient import TestClient
client = TestClient(jp.app)
response = client.get('/greet/san') 
