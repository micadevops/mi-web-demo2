from servidor import responder


def test_raiz_200_hola_mundo():
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
    status, cuerpo = responder("/saludo?nombre=<script>")
    assert status == 200
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_nombre_escapado_desde_url_codificada():
    status, cuerpo = responder("/saludo?nombre=%3Cscript%3Ealert(1)%3C/script%3E")
    assert status == 200
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_ruta_desconocida_404():
    status, _ = responder("/otra")
    assert status == 404


def test_ruta_similar_404():
    status, _ = responder("/saludo/extra")
    assert status == 404
