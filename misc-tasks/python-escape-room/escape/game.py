"""Game state: which rooms are open, watching the solution files, and telling
the web page whenever anything changes."""
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

from . import checker
from .progress import Progress
from .rooms import CHAPTERS, ROOM_IDS, ROOMS, data_files, starter_path

POLL_SECONDS = 0.5
SETTLE_SECONDS = 0.2  # give the editor time to finish writing before checking
FAILS_PER_HINT = 2


def file_signature(path):
    try:
        stat = path.stat()
    except OSError:
        return None
    return (stat.st_mtime_ns, stat.st_size)


def chapter_of(rid):
    return next(c for c in CHAPTERS if any(r["id"] == rid for r in c["rooms"]))


class Game:
    def __init__(self, game_dir, start_chapter=None):
        """start_chapter: a chapter number to open straight away (for classes that
        have already done the earlier chapters)."""
        self.game_dir = Path(game_dir)
        self.solutions_dir = self.game_dir / "solutions"
        self.progress = Progress(self.game_dir / "progress.json", ROOM_IDS)
        if start_chapter:
            self.progress.open_room(CHAPTERS[start_chapter - 1]["rooms"][0]["id"])
        self.results = {}
        self.seen = {}
        self.lock = threading.RLock()
        self.requests = queue.Queue()
        self.subscribers = []
        self.clock_mark = time.monotonic()
        self.save_warned = False
        for rid in self.progress.unlocked_ids():
            self.ensure_solution_file(rid)
        self.save()

    # ----- files -------------------------------------------------------

    def solution_path(self, rid):
        return self.solutions_dir / (rid + ".py")

    def ensure_solution_file(self, rid):
        """Give the student a starter file, plus any data files the room uses.
        Never overwrites their work."""
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
        path = self.solution_path(rid)
        if not path.exists():
            path.write_text(starter_path(rid).read_text(encoding="utf-8"), encoding="utf-8")
        for source in data_files(rid):
            target = self.solutions_dir / source.name
            if not target.exists():
                shutil.copyfile(str(source), str(target))

    def reset_room(self, rid):
        """Back up the student's file, then replace it with the starter code.
        Returns the backup's path relative to the game folder."""
        with self.lock:
            if self.progress.room(rid)["status"] == "locked":
                raise ValueError("That room is still locked.")
            path = self.solution_path(rid)
            backup = None
            if path.exists():
                backups = self.solutions_dir / "backups"
                backups.mkdir(parents=True, exist_ok=True)
                stamp = time.strftime("%Y%m%d-%H%M%S")
                backup = backups / "{}-{}.py".format(rid, stamp)
                n = 2
                while backup.exists():
                    backup = backups / "{}-{}-{}.py".format(rid, stamp, n)
                    n += 1
                shutil.copy2(str(path), str(backup))
                path.unlink()
            self.ensure_solution_file(rid)
            # Not the student's own save, so it shouldn't count as an attempt.
            self.seen[rid] = file_signature(path)
            self.results.pop(rid, None)
        self.requests.put((rid, False))
        self.broadcast()
        return backup.relative_to(self.game_dir).as_posix() if backup else None

    def open_folder(self):
        folder = str(self.solutions_dir)
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])

    # ----- watching and checking --------------------------------------

    def watch_forever(self):
        with self.lock:
            for rid in self.progress.unlocked_ids():
                self.seen[rid] = file_signature(self.solution_path(rid))
                self.requests.put((rid, False))
        while True:
            for rid, counted in self.next_jobs().items():
                self.run_check(rid, counted)

    def next_jobs(self):
        """Wait briefly, then return {room_id: counts_as_attempt} for rooms to check."""
        jobs = {}
        try:
            rid, counted = self.requests.get(timeout=POLL_SECONDS)
            jobs[rid] = counted
            while True:
                rid, counted = self.requests.get_nowait()
                jobs[rid] = jobs.get(rid, False) or counted
        except queue.Empty:
            pass
        for rid in self.changed_rooms():
            jobs[rid] = True
        return jobs

    def changed_rooms(self):
        with self.lock:
            watched = self.progress.unlocked_ids()
            changed = [rid for rid in watched
                       if file_signature(self.solution_path(rid)) != self.seen.get(rid)]
        if changed:
            time.sleep(SETTLE_SECONDS)
            with self.lock:
                for rid in changed:
                    self.seen[rid] = file_signature(self.solution_path(rid))
        return changed

    def recheck(self, rid):
        self.requests.put((rid, False))

    def run_check(self, rid, counted):
        result = checker.check(self.game_dir, rid, self.solution_path(rid))
        result["checked_at"] = time.time()
        with self.lock:
            self.flush_clock()
            self.results[rid] = result
            passed = result["status"] == "pass"
            room = self.progress.room(rid)
            if counted and room["status"] == "open" and result["status"] != "no_file":
                self.progress.record_attempt(rid, passed)
            if passed and room["status"] != "solved":
                next_id = self.progress.solve(rid)
                chapter = chapter_of(rid)
                if all(self.progress.room(r["id"])["status"] == "solved" for r in chapter["rooms"]):
                    # Remember the play time when each chapter was finished, for its victory screen.
                    self.progress.data.setdefault("chapter_seconds", {})[chapter["id"]] = self.play_seconds()
                if next_id:
                    self.ensure_solution_file(next_id)
                    self.seen[next_id] = file_signature(self.solution_path(next_id))
                    self.requests.put((next_id, False))
            self.save()
        self.broadcast()

    # ----- hints, time and saving --------------------------------------

    def hints_unlocked(self, rid):
        room = self.progress.room(rid)
        total = len(ROOMS[ROOM_IDS.index(rid)]["hints"])
        if room["status"] == "solved":
            return total
        return min(total, room["failed"] // FAILS_PER_HINT)

    def reveal_hint(self, rid):
        with self.lock:
            room = self.progress.room(rid)
            if room["status"] == "locked":
                raise ValueError("That room is still locked.")
            if room["hints_revealed"] < self.hints_unlocked(rid):
                room["hints_revealed"] += 1
                self.save()
        self.broadcast()

    def flush_clock(self):
        """Add the time since the last flush to the saved play time."""
        now = time.monotonic()
        if not self.progress.finished:
            self.progress.data["play_seconds"] += now - self.clock_mark
        self.clock_mark = now

    def play_seconds(self):
        extra = 0 if self.progress.finished else time.monotonic() - self.clock_mark
        return self.progress.data["play_seconds"] + extra

    def save(self):
        with self.lock:
            self.flush_clock()
            try:
                self.progress.save()
            except OSError as exc:
                if not self.save_warned:
                    print("Warning: couldn't save progress to {}: {}".format(self.progress.path, exc))
                    self.save_warned = True

    # ----- state for the web page --------------------------------------

    def state(self):
        with self.lock:
            rooms = []
            for number, info in enumerate(ROOMS, start=1):
                rid = info["id"]
                saved = self.progress.room(rid)
                room = {"id": rid, "number": number, "title": info["title"],
                        "chapter": info["chapter"], "status": saved["status"]}
                if saved["status"] != "locked":
                    unlocked = self.hints_unlocked(rid)
                    total = len(info["hints"])
                    room.update({
                        "concept": info["concept"],
                        "story": info["story"],
                        "objectives": info["objectives"],
                        "file": "solutions/{}.py".format(rid),
                        "path": str(self.solution_path(rid)),
                        "attempts": saved["attempts"],
                        "hints": info["hints"][:saved["hints_revealed"]],
                        "hints_unlocked": unlocked,
                        "hints_total": total,
                        "next_hint_in": FAILS_PER_HINT * (unlocked + 1) - saved["failed"] if unlocked < total else None,
                        "result": self.results.get(rid),
                    })
                if saved["status"] == "solved":
                    room["digit"] = info["digit"]
                rooms.append(room)
            chapter_seconds = self.progress.data.get("chapter_seconds", {})
            chapters = []
            for number, chapter in enumerate(CHAPTERS, start=1):
                statuses = [self.progress.room(r["id"])["status"] for r in chapter["rooms"]]
                chapters.append({
                    "id": chapter["id"],
                    "number": number,
                    "title": chapter["title"],
                    "topics": chapter["topics"],
                    "rooms": [r["id"] for r in chapter["rooms"]],
                    "started": any(s != "locked" for s in statuses),
                    "finished": all(s == "solved" for s in statuses),
                    "seconds": chapter_seconds.get(chapter["id"]),
                })
            return {
                "chapters": chapters,
                "rooms": rooms,
                "finished": self.progress.finished,
                "play_seconds": self.play_seconds(),
                "solutions_dir": str(self.solutions_dir),
            }

    def subscribe(self):
        q = queue.Queue()
        with self.lock:
            self.subscribers.append(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            if q in self.subscribers:
                self.subscribers.remove(q)

    def broadcast(self):
        payload = json.dumps(self.state())
        with self.lock:
            for q in self.subscribers:
                q.put(payload)
