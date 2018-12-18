import http.server
import os
import re

import config as cfg
from sequencePlaylist import SequencePlaylist

if not cfg.NO_PI:
    from neopixelSequencePlayer import NeopixelSequencePlayer
from sequence import Sequence
from sequencePlayerWindow import SequencePlayerWindow

if cfg.REQUIRES_AUTH or cfg.USE_ADMIN_AUTH:
    import base64


class StoppableHTTPServer(http.server.HTTPServer):
    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # Clean-up server (close socket, etc.)
            print("Stopping server")
            self.server_close()
            PLAYER.stop()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super(Handler, self).__init__(request, client_address, server)
        self.isuser = False
        self.isadmin = False

    def do_GET(self):
        # Construct a server response.
        try:
            if not self.check_auth():
                return

            if self.path.endswith(".js") or \
                    self.path.endswith(".css") or \
                    self.path.endswith(".ico") or \
                    self.path.endswith(".png" or \
                                       self.path.endswith(".jpg")):
                f = self.send_head()
                if f:
                    self.copyfile(f, self.wfile)
                    f.close()
            else:
                if self.path == "/auth" and not self.isuser:
                    self.send_response(401)
                    self.send_header(
                        'WWW-Authenticate',
                        'Basic realm="Authenticate"')
                    self.end_headers()
                    return
                else:
                    self.send_response(200)
                    self.send_header('Content-type', "text/html")
                    self.end_headers()

                if self.path == "/get/sequences/html/":
                    for file in os.listdir(cfg.SEQUENCE_DIR):
                        btnclass = "default"
                        if not PLAYER.currentplaylist is None and PLAYER.currentplaylist.name == file:
                            btnclass = "primary"

                        self.wfile.write(bytearray(
                            ('<button class="btn btn-' + btnclass + '">' + file + '</button>').encode()
                        ))
                elif self.path == "/get/playlists/html/":
                    for file in os.listdir(cfg.PLAYLIST_DIR):
                        btnclass = "default"
                        if not PLAYER.currentplaylist is None and PLAYER.currentplaylist.name == file:
                            btnclass = "primary"

                        self.wfile.write(bytearray(
                            ('<button class="btn btn-' + btnclass + '">' + file + '</button>').encode()
                        ))
                elif self.path == "/get/sequences/":
                    for file in os.listdir(cfg.SEQUENCE_DIR):
                        self.wfile.write(bytearray((file + "\n").encode()))
                elif self.path == "/get/playlists/":
                    for file in os.listdir(cfg.PLAYLIST_DIR):
                        self.wfile.write(bytearray((file + "\n").encode()))
                elif self.path == "/get/current/":
                    if PLAYER.currentplaylist is not None:
                        self.wfile.write(bytearray(PLAYER.currentplaylist.name.encode()))
                    else:
                        self.wfile.write(b"")
                elif self.path == "/stop/":
                    self.wfile.write(b"")
                    PLAYER.stopcurrentplaylist()
                    PLAYER.clear()
                elif str(self.path).startswith("/set/sequence/"):
                    name = str(self.path)[14:]
                    self.wfile.write(b"")
                    path = os.path.join(cfg.SEQUENCE_DIR, name)
                    try:
                        PLAYER.runsequence(Sequence.parsefile(path))
                    except FileNotFoundError:
                        print("Sequence '{0}' does not exist!".format(path))
                elif str(self.path).startswith("/set/playlist/"):
                    name = str(self.path)[14:]
                    self.wfile.write(b"")
                    path = os.path.join(cfg.PLAYLIST_DIR, name)
                    try:
                        PLAYER.runplaylist(SequencePlaylist.parsefile(path))
                    except FileNotFoundError:
                        print("Playlist '{0}' does not exist!".format(path))
                else:
                    f = open(cfg.HTML_FILE, "r").read()
                    self.wfile.write(
                        self.parsefile(f).encode('utf-8')
                    )
        except Exception as ex:
            print("ERROR: {0}".format(ex))
            self.send_response(500)
            self.end_headers()
            if cfg.VERBOSE_LOGGING:
                raise ex

    def do_POST(self):
        try:
            if not self.check_auth(True):
                return

            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()

            self.wfile.write(b"")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_string = post_data.decode("utf-8")

            if self.path == "/set/sequence/":
                seq = Sequence.parsestring(post_string)
                PLAYER.runsequence(seq)
            elif self.path == "/set/playlist/":
                playlist = SequencePlaylist.parsestring(post_string)
                PLAYER.runplaylist(playlist)
        except Exception as ex:
            print("ERROR: {0}".format(ex))
            self.send_response(500)
            self.end_headers()
            if cfg.VERBOSE_LOGGING:
                raise ex

    def log_message(self, format, *args):
        if cfg.VERBOSE_LOGGING:
            http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)

    def check_auth(self, adminonly=False):
        success = True
        admincorrect = False
        usercorrect = False

        authheader = self.headers['Authorization']
        if authheader and \
                authheader.startswith('Basic'):
            credentials = authheader.split(' ')[1]
            decoded = base64.b64decode(bytes(credentials, 'utf8')).decode('utf-8')
            user, password = decoded.split(":")

            admincorrect = \
                user == cfg.AUTH_ADMIN_USER and \
                password == cfg.AUTH_ADMIN_PASS

            usercorrect = \
                user == cfg.AUTH_USER and \
                password == cfg.AUTH_PASS

        if cfg.REQUIRES_AUTH or \
                adminonly and cfg.USE_ADMIN_AUTH:
            success = (adminonly and admincorrect) or \
                      (not adminonly and (admincorrect or usercorrect))

        if not success:
            if cfg.VERBOSE_LOGGING:
                print("Showing login prompt to user")
            message = "The christmastree requires login" if not adminonly \
                else "For this part you need to login as admin"
            self.send_response(401)
            self.send_header(
                'WWW-Authenticate',
                'Basic realm="' + message + '"')
            self.end_headers()

        self.isuser = usercorrect or admincorrect
        self.isadmin = not cfg.USE_ADMIN_AUTH or admincorrect

        if success and cfg.VERBOSE_LOGGING:
            print("is user: {0}, is admin: {1}".format(self.isuser, self.isadmin))

        return success

    def parsefile(self, file):
        result = file
        if not self.isadmin:
            regex = re.compile(r"(\#admin.*\#end)", re.IGNORECASE | re.DOTALL)
            result = re.sub(regex, '', result)
        else:
            result = result.replace("#admin", "")
            result = result.replace("#end", "")
        return result


if not os.path.exists(cfg.SEQUENCE_DIR):
    os.makedirs(cfg.SEQUENCE_DIR)
if not os.path.exists(cfg.PLAYLIST_DIR):
    os.makedirs(cfg.PLAYLIST_DIR)

if cfg.NO_PI:
    PLAYER = SequencePlayerWindow()
else:
    PLAYER = NeopixelSequencePlayer()

if cfg.STARTUP_SEQUENCE:
    if cfg.VERBOSE_LOGGING:
        print("Going to run the startup sequence")
    path = os.path.join(cfg.SEQUENCE_DIR, cfg.STARTUP_SEQUENCE)
    try:
        PLAYER.runsequence(Sequence.parsefile(path))
    except FileNotFoundError:
        print("Startup sequence '{0}' does not exist!".format(path))

if __name__ == '__main__':
    print('Server listening on port {0}...'.format(cfg.PORT))
    HTTPD = StoppableHTTPServer(('', cfg.PORT), Handler)
    HTTPD.run()
