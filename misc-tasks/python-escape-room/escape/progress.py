"""Saved progress: which rooms are open or solved, attempts, hints and play time.

Stored as progress.json in the game folder.
"""
import json
import os
import time
from pathlib import Path


class Progress:
    def __init__(self, path, room_ids):
        self.path = Path(path)
        self.room_ids = list(room_ids)
        self.data = self._load()
        self._normalise()

    def _load(self):
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except (OSError, ValueError):
            pass
        # Unreadable: keep a copy so nothing is silently lost, then start fresh.
        try:
            self.path.replace(self.path.with_name("progress.corrupt.json"))
        except OSError:
            pass
        return {}

    def _normalise(self):
        self.data.setdefault("version", 1)
        self.data.setdefault("play_seconds", 0.0)
        rooms = self.data.setdefault("rooms", {})
        for rid in self.room_ids:
            room = rooms.setdefault(rid, {})
            room.setdefault("status", "locked")
            room.setdefault("attempts", 0)
            room.setdefault("failed", 0)
            room.setdefault("hints_revealed", 0)
        # The first room is always open, and so is every room after a solved one.
        previous_solved = True
        for rid in self.room_ids:
            room = rooms[rid]
            if room["status"] == "locked" and previous_solved:
                room["status"] = "open"
            previous_solved = room["status"] == "solved"

    def room(self, rid):
        return self.data["rooms"][rid]

    def unlocked_ids(self):
        return [rid for rid in self.room_ids if self.room(rid)["status"] != "locked"]

    @property
    def finished(self):
        return all(self.room(rid)["status"] == "solved" for rid in self.room_ids)

    def open_room(self, rid):
        if self.room(rid)["status"] == "locked":
            self.room(rid)["status"] = "open"

    def record_attempt(self, rid, passed):
        room = self.room(rid)
        room["attempts"] += 1
        if not passed:
            room["failed"] += 1

    def solve(self, rid):
        """Mark a room solved. Returns the id of the room this unlocks, if any."""
        room = self.room(rid)
        room["status"] = "solved"
        room["solved_at"] = time.time()
        index = self.room_ids.index(rid)
        if index + 1 < len(self.room_ids):
            next_id = self.room_ids[index + 1]
            if self.room(next_id)["status"] == "locked":
                self.room(next_id)["status"] = "open"
                return next_id
        return None

    def save(self):
        temp = self.path.with_name(self.path.name + ".tmp")
        temp.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        os.replace(str(temp), str(self.path))
