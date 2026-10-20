"use client";

// Task 7 (Create): add a todo with a single task input
// Leave "done" out of the insert so the database default applies.
// Expected: "Clean my room" appears without "(done)".

import { useEffect, useState } from "react";
import { supabase, Todo } from "@/app/lib/supabase";

const Task7 = () => {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [task, setTask] = useState("");

    const loadTodos = async () => {
        // TODO: select every row from "todos", handle the error, then setTodos
        const { data, error } = await supabase.from("todos").select("*");
        if (error) {
            console.error("Error fetching todos:", error);
        } else {
            setTodos(data as Todo[]);
        }
    };

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        loadTodos();
    }, []);

    const addTodo = async () => {
        // TODO 1: return early if task is empty
        if (!task) {
            return;
        }
        // TODO 2: insert only the task
        const { error } = await supabase.from("todos").insert({ task });
        if (error) {
            console.error("Error adding todo:", error);
        } else {
            // TODO 3: clear the input and reload the list
            setTask("");
            loadTodos();
        }
    };

    return (
        <main>
            <h1>Add a todo</h1>
            <input placeholder="Task" value={task} onChange={(e) => setTask(e.target.value)} />
            <button onClick={addTodo}>Add todo</button>
            <ul>
                {todos.map((todo) => (
                    <li key={todo.id}>
                        {todo.task} {todo.done && "(done)"}
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task7;
