from servidor import responder


def test_raiz():
    status, cuerpo = responder("/")
    assert status == 200
    assert "Hola mundo" in cuerpo
    assert "<html" in cuerpo.lower()


def test_saludo_con_nombre():
    status, cuerpo = responder("/saludo?nombre=Ana")
    assert status == 200
    assert "Hola, Ana" in cuerpo


def test_saludo_sin_nombre():
    status, cuerpo = responder("/saludo")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_saludo_nombre_vacio_o_sin_valor():
    status, cuerpo = responder("/saludo?otro=1")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_escape_html():
    status, cuerpo = responder("/saludo?nombre=<script>alert(1)</script>")
    assert status == 200
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_escape_html_urlencoded():
    status, cuerpo = responder("/saludo?nombre=%3Cscript%3E")
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_ruta_desconocida_404():
    status, _ = responder("/otra")
    assert status == 404


def test_subruta_de_saludo_404():
    status, _ = responder("/saludo/extra")
    assert status == 404
