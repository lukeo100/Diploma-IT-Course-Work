const taskInput = document.getElementById("taskInput");
const addTaskButton = document.getElementById("addBtn");
const removeLastButton = document.getElementById("remove-last");
const taskList = document.getElementById("taskList");
const count = document.getElementById("count");

// empty array to store tasks
const tasks = [];

// draw every task on the screen from the tasks array
function render() {
  taskList.innerHTML = ""; // clear existing tasks

  // loop through each task
  for (let i = 0; i < tasks.length; i++) {
    const task = tasks[i];
    const li = document.createElement("li"); // creates a <li> element

    const taskText = document.createElement("span");
    taskText.textContent = task; // set task text

    const deleteButton = document.createElement("span");
    deleteButton.textContent = "Delete";
    deleteButton.title = "Delete";

    // handle delete button click
    deleteButton.addEventListener("click", function () {
      tasks.splice(i, 1); // remove task from array
      render(); // re-render the list
    });

    li.appendChild(taskText);
    li.appendChild(deleteButton);
    taskList.appendChild(li);
  }

  count.textContent = tasks.length + " tasks"; // update task count
  // update first and last task display
  const firstTask = tasks.length > 0 ? tasks[0] : "None";
  const lastTask = tasks.length > 0 ? tasks[tasks.length - 1] : "None";
  document.getElementById("firstTask").textContent = firstTask;
  document.getElementById("lastTask").textContent = lastTask;
}

// new task
addTaskButton.addEventListener("click", function () {
  const task = taskInput.value.trim(); // get the input value and trim whitespace

  if (task === "") return;

  if (tasks.includes(task)) {
    alert("Task already exists!");
    return;
  }

  tasks.push(task); // add the new task to the array
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
    render(); // re-render the list
  }
});

render(); // initial render to show any existing tasks
