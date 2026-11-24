import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs


def responder(ruta):
    """Devuelve (status, cuerpo_html) para una ruta con query string."""
    partes = urlsplit(ruta)
    if partes.path == "/":
        return 200, "<html><body><h1>Hola mundo</h1></body></html>"
    if partes.path == "/saludo":
        nombre = parse_qs(partes.query).get("nombre", [""])[0] or "desconocido"
        return 200, f"<html><body><h1>Hola, {html.escape(nombre)}</h1></body></html>"
    return 404, "<html><body><h1>No encontrado</h1></body></html>"


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
    HTTPServer(("", 8000), Handler).serve_forever()
