const taskInput = document.getElementById("taskInput");
const addTaskButton = document.getElementById("addBtn");
const removeLastButton = document.getElementById("remove-last");
const taskList = document.getElementById("taskList");
const count = document.getElementById("count");

// empty array to store tasks
const tasks = JSON.parse(localStorage.getItem("tasks")) || [];

function saveTasks() {
  localStorage.setItem("tasks", JSON.stringify(tasks));
}

// draw every task on the screen from the tasks array
function render() {
  taskList.innerHTML = ""; // clear existing tasks

  // loop through each task
  for (let i = 0; i < tasks.length; i++) {
    const task = tasks[i];
    const li = document.createElement("li"); // creates a <li> element
    if (task.completed) {
      li.style.textDecoration = "line-through"; // mark completed tasks
    }

    const taskText = document.createElement("span");
    taskText.textContent = task.text; // set task text

    const deleteButton = document.createElement("span");
    deleteButton.textContent = "Delete";
    deleteButton.title = "Delete";

    // handle delete button click
    deleteButton.addEventListener("click", function () {
      tasks.splice(i, 1); // remove task from array
      saveTasks(); // save tasks to localStorage
      render(); // re-render the list
    });

    const markButton = document.createElement("span");
    if (task.completed) {
      markButton.textContent = "❌";
      markButton.title = "Mark as incomplete";
    } else {
      markButton.textContent = "✔️";
      markButton.title = "Mark as complete";
    }

    // handle mark button click
    markButton.addEventListener("click", function () {
      task.completed = !task.completed; // toggle completed status
      saveTasks();
      render();
    });

    li.appendChild(taskText);
    li.appendChild(markButton);
    li.appendChild(deleteButton);
    taskList.appendChild(li);
  }

  count.textContent = tasks.length + " tasks"; // update task count
  // update first and last task display
  const firstTask = tasks.length > 0 ? tasks[0] : "None";
  const lastTask = tasks.length > 0 ? tasks[tasks.length - 1] : "None";
  document.getElementById("firstTask").textContent = firstTask.text;
  document.getElementById("lastTask").textContent = lastTask.text;
}

// new task
addTaskButton.addEventListener("click", function () {
  const task = {
    text: taskInput.value.trim(),
    completed: false,
  };
  if (task.text === "") return;

  if (tasks.includes(task)) {
    alert("Task already exists!");
    return;
  }

  tasks.push(task); // add the new task to the array
  saveTasks(); // save tasks to localStorage
  render();
  taskInput.value = ""; // clear the input field
});

// press enter to add
taskInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") addTaskButton.click();
});

// remove last task
removeLastButton.addEventListener("click", function () {
  if (tasks.length > 0) {
    tasks.pop(); // remove the last task from the array
    saveTasks(); // save tasks to localStorage
    render(); // re-render the list
  }
});

// clear all tasks
function clearTasks() {
  if (confirm("Are you sure you want to clear all tasks?")) {
    tasks.length = 0; // clear the array
    saveTasks();
    render(); // re-render the list
  }
}

render(); // initial render to show any existing tasks
