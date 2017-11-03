import http.server
import os
from time import sleep
import config as cfg
import sequence as s

class StoppableHTTPServer(http.server.HTTPServer):
    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # Clean-up server (close socket, etc.)
            self.server_close()
            MANAGER.stop()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Construct a server response.
        try:
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()

            if self.path == "/get/sequences/html":
                for file in os.listdir(cfg.SEQUENCE_DIR):
                    btnclass = "default"
                    if not MANAGER.currentsequence is None and MANAGER.currentsequence.name == file:
                        btnclass = "primary"

                    self.wfile.write(bytearray(
                        ('<button class="btn btn-' + btnclass + '">' + file + '</button>').encode()
                        ))
            elif self.path == "/get/sequences/":
                for file in os.listdir(cfg.SEQUENCE_DIR):
                    self.wfile.write(bytearray((file + "\n").encode()))
            elif self.path == "/get/current/":
                self.wfile.write(b"")
                return
                if MANAGER.currentsequence is not None:
                    self.wfile.write(bytearray(MANAGER.currentsequence.name.encode()))
                else:
                    self.wfile.write(b"")
            elif self.path == "/stop/":
                self.wfile.write(b"")
                return
                MANAGER.stopcurrentsequence()
                MANAGER.clear()
            elif str(self.path).startswith("/set/"):
                self.wfile.write(b"")
                return
                name = str(self.path)[5:]
                self.wfile.write(b"")
                path = os.path.join(cfg.SEQUENCE_DIR, name)
                MANAGER.runsequence(s.Sequence.parsefile(path))
            else:
                if self.path.endswith(".js") or self.path.endswith(".css"):
                    super(Handler, self).do_GET()
                else:
                    f = open(cfg.HTML_FILE, "rb")
                    self.wfile.write(f.read())
                f.close()

            return
        except Exception as ex:
            print(ex)
            self.send_response(500)

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()

            if self.path == "/set/":
                self.wfile.write(b"")

                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                post_string = post_data.decode("utf-8")

                seq = s.Sequence.parsestring(post_string)
                MANAGER.runsequence(seq)
            else:
                self.wfile.write(b"")
        except Exception as ex:
            print(ex)
            self.send_response(500)

MANAGER = s.SequenceManager()

if __name__ == '__main__':
    print('Server listening on port {}...'.format(cfg.PORT))
    HTTPD = StoppableHTTPServer(('', cfg.PORT), Handler)
    HTTPD.run()
