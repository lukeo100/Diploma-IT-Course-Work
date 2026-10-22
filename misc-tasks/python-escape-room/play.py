"""Python Escape Room: run this file to start the game.

    python play.py               start the game and open it in your browser
    python play.py --no-browser  start the game without opening a browser

Everything the game saves (your code in solutions/ and progress.json) is
kept in this folder, so you can copy the whole folder to carry on elsewhere.
"""
import sys

if sys.version_info < (3, 8):
    sys.exit("The Python Escape Room needs Python 3.8 or newer.")

import threading
import webbrowser
from pathlib import Path

from escape.game import Game
from escape.rooms import CHAPTERS
from escape.server import start_server

GAME_DIR = Path(__file__).resolve().parent


def chapter_option():
    if "--chapter" not in sys.argv:
        return None
    index = sys.argv.index("--chapter")
    value = sys.argv[index + 1] if index + 1 < len(sys.argv) else ""
    if not value.isdigit() or not 1 <= int(value) <= len(CHAPTERS):
        sys.exit("--chapter needs a chapter number from 1 to {}.".format(len(CHAPTERS)))
    return int(value)


def main():
    game = Game(GAME_DIR, start_chapter=chapter_option())
    server = start_server(game)
    url = "http://127.0.0.1:{}/".format(server.server_address[1])

    print("=" * 60)
    print("  PYTHON ESCAPE ROOM")
    print("=" * 60)
    print("  Game page:   " + url)
    print("  Your code:   " + str(game.solutions_dir))
    print()
    print("  Keep this window open while you play.")
    print("  Press Ctrl+C to save and quit.")
    print("=" * 60)

    threading.Thread(target=game.watch_forever, daemon=True).start()
    if "--no-browser" not in sys.argv:
        threading.Timer(0.5, webbrowser.open, [url]).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nProgress saved. See you next time!")
    finally:
        game.save()
        server.server_close()


if __name__ == "__main__":
    main()
