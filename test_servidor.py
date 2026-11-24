from servidor import responder


def test_raiz():
    status, cuerpo = responder("/")
    assert status == 200
    assert "Hola mundo" in cuerpo


def test_saludo_con_nombre():
    status, cuerpo = responder("/saludo?nombre=Ana")
    assert status == 200
    assert "Hola, Ana" in cuerpo


def test_saludo_sin_nombre():
    status, cuerpo = responder("/saludo")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_saludo_nombre_vacio_es_desconocido():
    status, cuerpo = responder("/saludo?nombre=")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_nombre_se_escapa():
    status, cuerpo = responder("/saludo?nombre=<script>alert(1)</script>")
    assert status == 200
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_nombre_urlencoded_se_escapa():
    _, cuerpo = responder("/saludo?nombre=%3Cscript%3E")
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_ruta_desconocida_404():
    assert responder("/otra")[0] == 404
    assert responder("/saludo/extra")[0] == 404
