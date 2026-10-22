"use strict";

// Plain-English explanations shown under Python errors.
const FRIENDLY = {
  SyntaxError: "Python couldn't understand this line. Look for a missing bracket, quote or colon (:), on this line or the one just above it.",
  IndentationError: "The spaces at the start of this line are wrong. Code inside a def, if, for or while needs 4 more spaces than the line above it.",
  TabError: "This line mixes tabs and spaces. Use spaces only.",
  NameError: "Python doesn't know this name. Check the spelling (capitals matter!) and that the variable or function is created before it's used.",
  TypeError: "A value is the wrong type for what you're doing with it, like adding a number to a str, or calling a function with the wrong number of arguments.",
  ValueError: "The value has the right type but can't be used, like int(\"seven\").",
  ZeroDivisionError: "Your code divided by zero.",
  IndexError: "Your code asked for a list position that doesn't exist. The first item is at index 0 and the last is at len(...) - 1.",
  KeyError: "Your code looked up a dictionary key that isn't there. Try .get(key, default).",
  AttributeError: "This value doesn't have that method or attribute. Check the spelling, and what type the value is.",
  RecursionError: "A function keeps calling itself forever.",
  UnboundLocalError: "A variable is used inside a function before it has been given a value there.",
};

const $ = (selector) => document.querySelector(selector);

let state = null;
let selected = loadSelected();
let previousStatus = {};
let clockBase = 0;
let clockAt = 0;

// ---------- helpers ----------

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// Escapes text, then shows `backticks` as code.
function rich(value) {
  return esc(value).replace(/`([^`]+)`/g, "<code>$1</code>");
}

function formatTime(seconds) {
  const s = Math.max(0, Math.floor(seconds));
  const pad = (n) => String(n).padStart(2, "0");
  return `${pad(Math.floor(s / 3600))}:${pad(Math.floor((s % 3600) / 60))}:${pad(s % 60)}`;
}

function loadSelected() {
  try { return localStorage.getItem("escape-room-selected"); } catch (e) { return null; }
}

function saveSelected() {
  try { localStorage.setItem("escape-room-selected", selected); } catch (e) { /* not important */ }
}

function roomById(id) {
  return state.rooms.find((r) => r.id === id);
}

function chapterOf(roomId) {
  return state.chapters.find((c) => c.rooms.includes(roomId));
}

function chapterRooms(chapter) {
  return chapter.rooms.map(roomById);
}

// The furthest room the student can play.
function currentRoomId() {
  const open = state.rooms.filter((r) => r.status === "open");
  return (open.length ? open[open.length - 1] : state.rooms.filter((r) => r.status !== "locked").pop()).id;
}

let toastTimer = null;
function toast(message) {
  const el = $("#toast");
  el.innerHTML = rich(message);
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.hidden = true; }, 4000);
}

async function post(path) {
  const response = await fetch(path, { method: "POST", headers: { "X-Escape-Room": "1" } });
  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.ok === false) throw new Error(data.error || "The game didn't respond.");
  return data;
}

// ---------- state updates ----------

function update(newState) {
  const firstLoad = state === null;
  const newlySolved = newState.rooms.filter(
    (r) => r.status === "solved" && previousStatus[r.id] && previousStatus[r.id] !== "solved"
  );
  newState.rooms.forEach((r) => { previousStatus[r.id] = r.status; });
  state = newState;

  const chosen = selected && roomById(selected);
  if (!chosen || chosen.status === "locked") selected = currentRoomId();

  clockBase = state.play_seconds;
  clockAt = performance.now();
  render();

  if (!firstLoad && newlySolved.length) showDoor(newlySolved[newlySolved.length - 1]);
}

function render() {
  renderTop();
  renderMap();
  renderRoom();
  tick();
}

function tick() {
  if (!state) return;
  const elapsed = state.finished ? 0 : (performance.now() - clockAt) / 1000;
  $("#timer").textContent = formatTime(clockBase + elapsed);
}

function slots(rooms) {
  return rooms
    .map((r) => `<span class="slot ${r.digit != null ? "found" : ""}">${r.digit != null ? r.digit : "?"}</span>`)
    .join("");
}

function renderTop() {
  const chapter = chapterOf(selected);
  $("#code-label").textContent = `Chapter ${chapter.number} code`;
  $("#code").innerHTML = slots(chapterRooms(chapter));
  $("#trophy").hidden = !chapter.finished;
}

function renderMap() {
  $("#map").innerHTML = state.chapters.map((chapter) => {
    const rooms = chapterRooms(chapter).map((r) => {
      const icon = r.status === "solved" ? "🔓" : r.status === "open" ? "🚪" : "🔒";
      const classes = [r.status, r.id === selected ? "selected" : ""].join(" ");
      return `<li><button class="${classes}" data-room="${r.id}" ${r.status === "locked" ? "disabled" : ""}>
        <span class="icon">${icon}</span><span class="num">${r.number}</span>
        <span class="name">${r.status === "locked" ? "Locked" : esc(r.title)}</span></button></li>`;
    }).join("");
    return `<h2 class="${chapter.started ? "" : "locked"}">Chapter ${chapter.number}${chapter.finished ? " ✓" : ""}
        <span class="chapter-title">${esc(chapter.title)}</span></h2>
      <ol>${rooms}</ol>`;
  }).join("");
}

function renderRoom() {
  const r = roomById(selected);
  const result = r.result;
  const checked = result && result.checked_at
    ? ` · last checked ${new Date(result.checked_at * 1000).toLocaleTimeString()}` : "";
  $("#room").innerHTML = `
    <div class="room-head">
      <span class="room-num">Chapter ${chapterOf(r.id).number} · Room ${r.number}</span>
      <h1>${esc(r.title)}</h1>
      <span class="chip">${esc(r.concept)}</span>
      ${r.status === "solved" ? `<span class="chip solved">Escaped · digit ${r.digit}</span>` : ""}
    </div>
    <p class="story">${esc(r.story)}</p>

    <section class="card">
      <h2>Your mission</h2>
      <ul class="objectives">${r.objectives.map((o) => `<li>${rich(o)}</li>`).join("")}</ul>
    </section>

    <section class="card">
      <h2>Your code file</h2>
      <p>Open this file in any editor (VS Code, IDLE, Thonny, PyCharm…), complete the TODOs and
         <strong>save</strong>. Your code is checked every time you save.</p>
      <div class="path"><code id="path">${esc(r.path)}</code></div>
      <div class="actions">
        <button class="btn" data-act="copy">Copy path</button>
        <button class="btn" data-act="folder">Open folder</button>
        <button class="btn" data-act="check">Check now</button>
      </div>
      <p class="watching"><span class="pulse"></span>Watching <code>${esc(r.file)}</code>${checked}</p>
    </section>

    <section class="card">${renderResult(r)}</section>
    <section class="card">${renderHints(r)}</section>

    <div class="footer-actions">
      <button class="btn danger" data-act="reset">Reset room to the starter code</button>
    </div>`;
}

function banner(kind, html) {
  return `<div class="banner ${kind}">${html}</div>`;
}

function renderResult(r) {
  const res = r.result;
  let html = "<h2>Checks</h2>";
  if (!res) return html + banner("wait", "⏳ Checking your code…");

  const tests = res.tests || [];
  const passed = tests.filter((t) => t.passed).length;
  switch (res.status) {
    case "pass":
      html += banner("pass", r.status === "solved"
        ? `✅ All checks passed! This door is open. Your code digit is <strong>${r.digit}</strong>.`
        : "✅ All checks passed!");
      break;
    case "fail":
      html += banner("fail", `🔒 ${passed} of ${tests.length} checks passed. Keep going!`);
      break;
    case "syntax_error":
      html += banner("error", "🧱 Python can't read your file yet. There's a syntax error.");
      break;
    case "error":
      html += banner("error", "💥 Your file crashed while it was loading, before any checks could run.");
      break;
    case "timeout":
      html += banner("error", `⏱️ Your code ran for more than ${res.limit} seconds. Is there a loop that never ends?`);
      break;
    case "no_file":
      html += banner("error", "📄 Your file is missing. Click “Reset room” below to get a fresh copy.");
      break;
    default:
      html += banner("error", "⚠️ Something went wrong while checking your code.");
  }
  if (res.error) html += renderError(res.error);
  if (res.details) html += `<pre class="details">${esc(res.details)}</pre>`;
  if (tests.length) {
    html += `<ul class="tests">${tests.map((t) => `
      <li class="${t.passed ? "ok" : "bad"}">
        <span class="mark">${t.passed ? "✓" : "✗"}</span>
        <div><div class="tname">${esc(t.name)}</div>${t.message ? `<div class="tmsg">${rich(t.message)}</div>` : ""}</div>
      </li>`).join("")}</ul>`;
  }
  if (res.output) {
    html += `<details class="output"><summary>What your code printed</summary><pre>${esc(res.output)}</pre></details>`;
  }
  return html;
}

function renderError(e) {
  const where = e.line ? ` on line ${e.line}` : "";
  let code = "";
  if (e.code) {
    const caret = e.column ? "\n" + " ".repeat(Math.max(0, e.column - 1)) + "^" : "";
    code = `<pre>${esc(e.code + caret)}</pre>`;
  }
  const tip = FRIENDLY[e.type];
  return `<div class="error-box">
    <div class="etitle">${esc(e.type)}${where}: ${rich(e.message)}</div>
    ${code}
    ${tip ? `<p class="tip">💡 ${esc(tip)}</p>` : ""}
  </div>`;
}

function renderHints(r) {
  let html = "<h2>Hints</h2>";
  if (r.hints.length) html += `<ol class="hints">${r.hints.map((h) => `<li>${rich(h)}</li>`).join("")}</ol>`;
  if (r.hints.length < r.hints_unlocked) {
    html += `<button class="btn" data-act="hint">💡 Show hint ${r.hints.length + 1}</button>`;
  } else if (r.hints_unlocked < r.hints_total) {
    const n = r.next_hint_in;
    html += `<p class="muted">${r.hints.length ? "The next hint" : "A hint"} unlocks after ${n} more
      save${n === 1 ? "" : "s"} that ${n === 1 ? "doesn't" : "don't"} pass yet.</p>`;
  } else if (r.status !== "solved") {
    html += `<p class="muted">That's every hint. You've got this!</p>`;
  }
  return html;
}

// ---------- door and victory overlay ----------

function openOverlay(html) {
  const overlay = $("#overlay");
  $("#overlay-content").innerHTML = html;
  overlay.classList.remove("open");
  overlay.hidden = false;
  requestAnimationFrame(() => requestAnimationFrame(() => overlay.classList.add("open")));
}

function closeOverlay() {
  $("#overlay").hidden = true;
  $("#overlay").classList.remove("open");
}

function showDoor(r) {
  const chapter = chapterOf(r.id);
  if (chapter.finished) return showVictory(chapter);
  const after = state.rooms[r.number];  // numbers start at 1, so this is the room after r
  const next = after && after.status === "open" ? after : state.rooms.find((x) => x.status === "open");
  openOverlay(`
    <div class="big">🔓</div>
    <h2>Room ${r.number} escaped!</h2>
    <p>You found a digit of the escape code:</p>
    <div class="digit">${r.digit}</div>
    ${next
      ? `<button class="btn primary" data-go="${next.id}">Enter Room ${next.number}: ${esc(next.title)} →</button>`
      : `<button class="btn primary" data-close>Continue</button>`}`);
}

function showVictory(chapter) {
  const rooms = chapterRooms(chapter);
  const saves = rooms.reduce((sum, r) => sum + r.attempts, 0);
  const hints = rooms.reduce((sum, r) => sum + r.hints.length, 0);
  const nextChapter = state.chapters[chapter.number];  // numbers start at 1
  const nextRoom = nextChapter && chapterRooms(nextChapter).find((r) => r.status === "open");
  const last = !nextChapter;
  openOverlay(`
    <div class="big">🏆</div>
    <h2>${last ? "YOU ESCAPED!" : `Chapter ${chapter.number} complete!`}</h2>
    <p>${last ? "Every door is open." : `You escaped ${esc(chapter.title)}… but it isn't over yet.`}
       The chapter ${chapter.number} code is:</p>
    <div class="final-code">${slots(rooms)}</div>
    <dl class="stats">
      <dt>Total play time</dt><dd>${formatTime(chapter.seconds != null ? chapter.seconds : state.play_seconds)}</dd>
      <dt>Saves</dt><dd>${saves}</dd>
      <dt>Hints used</dt><dd>${hints}</dd>
    </dl>
    ${nextRoom
      ? `<button class="btn primary" data-go="${nextRoom.id}">On to Chapter ${nextChapter.number}: ${esc(nextChapter.title)} →</button>`
      : `<button class="btn primary" data-close>Close</button>`}`);
}

// ---------- events ----------

$("#map").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-room]");
  if (!button || button.disabled) return;
  selected = button.dataset.room;
  saveSelected();
  render();
});

$("#room").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-act]");
  if (!button) return;
  const room = roomById(selected);
  try {
    switch (button.dataset.act) {
      case "copy":
        await copyPath(room.path);
        break;
      case "folder":
        await post("/api/open-folder");
        break;
      case "check":
        await post(`/api/check/${room.id}`);
        toast("Checking…");
        break;
      case "hint":
        await post(`/api/hint/${room.id}`);
        break;
      case "reset":
        if (!confirm(`Reset “${room.title}” to the starter code?\n\nYour current code will be backed up first.`)) return;
        const data = await post(`/api/reset/${room.id}`);
        toast(data.backup ? `Room reset. Your old code was backed up to \`${data.backup}\`.` : "Room reset.");
        break;
    }
  } catch (error) {
    toast("⚠️ " + error.message);
  }
});

async function copyPath(path) {
  try {
    await navigator.clipboard.writeText(path);
    toast("Path copied. Paste it into your editor's Open File box.");
  } catch (error) {
    const range = document.createRange();
    range.selectNodeContents($("#path"));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    toast("Path selected. Press Ctrl+C (or ⌘C) to copy it.");
  }
}

$("#overlay").addEventListener("click", (event) => {
  const go = event.target.closest("[data-go]");
  if (go) {
    selected = go.dataset.go;
    saveSelected();
    closeOverlay();
    render();
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else if (event.target.closest("[data-close]")) {
    closeOverlay();
  }
});

$("#trophy").addEventListener("click", () => showVictory(chapterOf(selected)));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !$("#overlay").hidden) closeOverlay();
});

function connect() {
  const events = new EventSource("/events");
  events.onmessage = (event) => {
    $("#offline").hidden = true;
    update(JSON.parse(event.data));
  };
  events.onerror = () => { $("#offline").hidden = false; };
}

setInterval(tick, 1000);
connect();
