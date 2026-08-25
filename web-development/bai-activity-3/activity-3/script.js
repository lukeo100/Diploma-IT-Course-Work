const titleInput = document.getElementById("titleInput");
const noteInput = document.getElementById("noteInput");
const addBtn = document.getElementById("addBtn");
const noteList = document.getElementById("noteList");
const searchInput = document.getElementById("searchInput");

// get saved notes from local storage
let notes = JSON.parse(localStorage.getItem("notes")) || [];

/*
example note object
{ 
    title: "Shopping",
    note: "Buy milk and bread",
    date: "15/03/2025"
}
*/

// save notes function
function saveNotes() {
  localStorage.setItem("notes", JSON.stringify(notes));
}

// render notes function
function render(notesToRender = notes) {
  noteList.innerHTML = "";

  // sort notes by date (newest first)
  notesToRender.sort((a, b) => {
    const dateA = new Date(a.date.split("/").reverse().join("-"));
    const dateB = new Date(b.date.split("/").reverse().join("-"));
    return dateB - dateA;
  });

  // loop through notes and create list items
  for (let i = 0; i < notesToRender.length; i++) {
    const note = notesToRender[i];
    const li = document.createElement("li");
    const header = document.createElement("div");
    header.className = "note-header";

    const titleEl = document.createElement("span");
    titleEl.className = "note-title";
    titleEl.textContent = note.title;

    const deleteBtn = document.createElement("span");
    deleteBtn.className = "delete-btn";
    deleteBtn.textContent = "Delete";

    // handle del clicked
    deleteBtn.addEventListener("click", () => {
      notes.splice(i, 1);
      saveNotes();
      render();
    });

    header.appendChild(titleEl);
    header.appendChild(deleteBtn);

    const dateEl = document.createElement("div");
    dateEl.className = "note-date";
    dateEl.textContent = note.date;

    const textEl = document.createElement("div");
    textEl.className = "note-text";
    textEl.textContent = note.note; // this is the note content

    li.appendChild(header);
    li.appendChild(dateEl);
    li.appendChild(textEl);
    noteList.appendChild(li);
  }
}

// new note button
addBtn.addEventListener("click", () => {
  const title = titleInput.value.trim();
  const note = noteInput.value.trim();

  if (title === "" || note === "") {
    alert("Please enter both a title and a note.");
    return;
  } // do not add empty notes

  const date = new Date().toLocaleDateString("en-GB"); // format date as DD/MM/YYYY
  notes.push({ title, note, date });
  saveNotes();
  render();
  titleInput.value = "";
  noteInput.value = "";
});

// clear all notes function
function clearAllNotes() {
  if (confirm("Are you sure you want to delete all notes?")) {
    notes.length = 0; // clear the notes array
    saveNotes();
    render();
  }
}

// search notes function
searchInput.addEventListener("input", () => {
  const searchTerm = searchInput.value.toLowerCase();
  const filteredNotes = notes.filter(
    (note) =>
      note.title.toLowerCase().includes(searchTerm) ||
      note.note.toLowerCase().includes(searchTerm),
  );
  // Update the noteList with filtered notes
  render(filteredNotes);
});

render(); // initial render of notes on page load
