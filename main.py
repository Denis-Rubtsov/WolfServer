import os
from http.server import HTTPServer, BaseHTTPRequestHandler
VOICE_FOLDER = "/data/voice"
PORT = int(os.getenv("PORT", 8080))
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

            # healthcheck
            if self.path == "/":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Bot is running!")
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
        print(f"HTTP server listening on port {PORT}")
        server.serve_forever()
    except Exception as e:
        print("Ошибка при запуске HTTP сервера:", e)

if __name__ == '__main__':
    run_http_server()
    #threading.Thread(target=run_http_server).start()