from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

PUERTO = 8000


def _pagina(texto):
    return f"<html><body><h1>{texto}</h1></body></html>"


def responder(ruta_con_query):
    """Devuelve (status, html) sin necesidad de levantar el servidor."""
    partes = urlsplit(ruta_con_query)
    if partes.path == "/":
        return 200, _pagina("Hola mundo")
    if partes.path == "/saludo":
        nombre = parse_qs(partes.query).get("nombre", [""])[0] or "desconocido"
        return 200, _pagina("Hola, " + escape(nombre))
    return 404, _pagina("No encontrado")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, html = responder(self.path)
        cuerpo = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)


if __name__ == "__main__":
    HTTPServer(("", PUERTO), Handler).serve_forever()
