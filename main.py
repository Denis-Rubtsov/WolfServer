import os
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
VOICE_FOLDER = "/data/voice"
PORT = int(os.getenv("PORT", 8080))
CERT_FILE = os.getenv("SSL_CERT", "cert.pem")
KEY_FILE = os.getenv("SSL_KEY", "key.pem")
class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # раздаём голосовые файлы
            if self.path.startswith("/voice/"):
                filename = os.path.basename(self.path)
                filepath = os.path.join(VOICE_FOLDER, filename)
                if os.path.exists(filepath):
                    self.send_response(200)
                    self.send_header("Content-Type", "audio/ogg")
                    self.end_headers()
                    with open(filepath, "rb") as f:
                        self.wfile.write(f.read())
                    return
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"File not found")
                    return

            if self.path == "/":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Server's running")
                return

            # всё остальное
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

        except Exception as e:
            print("Ошибка в HTTPHandler:", e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error")

def run_http_server():
    try:
        server = HTTPServer(("0.0.0.0", PORT), HealthHandler)  # type: ignore

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

        server.socket = context.wrap_socket(server.socket, server_side=True)

        print(f"HTTPS server listening on port {PORT}")
        server.serve_forever()
    except Exception as e:
        print("Ошибка при запуске HTTP сервера:", e)

if __name__ == '__main__':
    run_http_server()