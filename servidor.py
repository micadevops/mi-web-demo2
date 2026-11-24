import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs

PUERTO = 8000


def responder(ruta_con_query):
    """Devuelve (status, html) para una ruta, sin necesitar el servidor."""
    partes = urlsplit(ruta_con_query)
    if partes.path == "/":
        return 200, "<html><body><h1>Hola mundo</h1></body></html>"
    if partes.path == "/saludo":
        nombre = parse_qs(partes.query).get("nombre", [""])[0].strip()
        if not nombre:
            nombre = "desconocido"
        seguro = html.escape(nombre)
        return 200, f"<html><body><h1>Hola, {seguro}</h1></body></html>"
    return 404, "<html><body><h1>404 No encontrado</h1></body></html>"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, cuerpo = responder(self.path)
        datos = cuerpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


if __name__ == "__main__":
    HTTPServer(("", PUERTO), Handler).serve_forever()
