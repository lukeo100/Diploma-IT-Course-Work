"""The local web server: serves the game page and keeps it up to date."""
import json
import queue
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .rooms import ROOM_IDS

WEB_DIR = Path(__file__).resolve().parent.parent / "web"
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
}
HEARTBEAT_SECONDS = 15
PORTS = range(8000, 8020)


class GameServer(ThreadingHTTPServer):
    daemon_threads = True
    # On Windows SO_REUSEADDR lets two servers share one port, so leave it off there.
    allow_reuse_address = sys.platform != "win32"

    def __init__(self, address, game):
        super().__init__(address, Handler)
        self.game = game


def start_server(game, host="127.0.0.1"):
    """Start on port 8000, or the next free port if that one is busy."""
    for port in PORTS:
        try:
            return GameServer((host, port), game)
        except OSError:
            continue
    sys.exit("Couldn't find a free port between {} and {}.".format(PORTS[0], PORTS[-1]))


class Handler(BaseHTTPRequestHandler):
    server_version = "PythonEscapeRoom"

    def log_message(self, format, *args):
        pass  # keep the terminal tidy for students

    @property
    def game(self):
        return self.server.game

    def host_ok(self):
        # Blocks other websites from reaching the game through DNS tricks.
        port = self.server.server_address[1]
        return self.headers.get("Host") in ("127.0.0.1:{}".format(port), "localhost:{}".format(port))

    def do_GET(self):
        if not self.host_ok():
            return self.send_error(403)
        path = urlsplit(self.path).path
        if path == "/":
            self.send_file(WEB_DIR / "index.html")
        elif path.startswith("/static/"):
            target = (WEB_DIR / path[len("/static/"):]).resolve()
            if WEB_DIR.resolve() in target.parents and target.is_file():
                self.send_file(target)
            else:
                self.send_error(404)
        elif path == "/api/state":
            self.send_json(self.game.state())
        elif path == "/events":
            self.stream_events()
        else:
            self.send_error(404)

    def do_POST(self):
        # Browsers won't send this custom header from another website without
        # a CORS preflight, which we never approve, so only the game page can
        # press these buttons.
        if not self.host_ok() or self.headers.get("X-Escape-Room") != "1":
            return self.send_error(403)
        parts = urlsplit(self.path).path.strip("/").split("/")
        try:
            if parts == ["api", "open-folder"]:
                self.game.open_folder()
                return self.send_json({"ok": True})
            if len(parts) == 3 and parts[0] == "api" and parts[2] in ROOM_IDS:
                action, rid = parts[1], parts[2]
                if action == "reset":
                    return self.send_json({"ok": True, "backup": self.game.reset_room(rid)})
                if action == "hint":
                    self.game.reveal_hint(rid)
                    return self.send_json({"ok": True})
                if action == "check":
                    self.game.recheck(rid)
                    return self.send_json({"ok": True})
        except (ValueError, OSError) as exc:
            return self.send_json({"ok": False, "error": str(exc)}, status=400)
        self.send_error(404)

    def send_file(self, path):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def stream_events(self):
        """Server-Sent Events: push the full game state whenever it changes."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        updates = self.game.subscribe()
        try:
            self.write_event(json.dumps(self.game.state()))
            while True:
                try:
                    payload = updates.get(timeout=HEARTBEAT_SECONDS)
                except queue.Empty:
                    self.wfile.write(b": still here\n\n")
                    self.wfile.flush()
                    continue
                self.write_event(payload)
        except OSError:
            pass  # the browser tab was closed
        finally:
            self.game.unsubscribe(updates)

    def write_event(self, payload):
        self.wfile.write(("data: " + payload + "\n\n").encode("utf-8"))
        self.wfile.flush()
