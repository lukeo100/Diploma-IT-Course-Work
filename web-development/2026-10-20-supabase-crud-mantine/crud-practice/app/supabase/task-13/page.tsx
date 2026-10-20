"use client";

// Task 13 (Delete): "Clear finished" removes all todos where done is true
// in ONE query. This page starts from the Task 9 page.
// Expected: after ticking two todos and clicking "Clear finished",
// only the unticked todos remain.

import { useEffect, useState } from "react";
import { supabase, Todo } from "@/app/lib/supabase";

const Task13 = () => {
    const [todos, setTodos] = useState<Todo[]>([]);

    const loadTodos = async () => {
        // TODO: select every row from "todos" ordered by id, then setTodos
        const { data, error } = await supabase.from("todos").select("*").order("id");
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

    const toggleTodo = async (todo: Todo) => {
        // TODO: same as Task 9
        const { error } = await supabase.from("todos").update({ done: !todo.done }).eq("id", todo.id);
        if (error) {
            console.error("Error toggling todo:", error);
        } else {
            loadTodos();
        }
    };

    const clearFinished = async () => {
        // TODO 1: delete every row where done is true
        const { error } = await supabase.from("todos").delete().eq("done", true);
        // TODO 2: check for an error
        if (error) {
            console.error("Error clearing finished todos:", error);
        } else {
            // TODO 3: reload the list
            loadTodos();
        }
    };

    return (
        <main>
            <h1>Clear finished todos</h1>
            <button onClick={clearFinished}>Clear finished</button>
            <ul>
                {todos.map((todo) => (
                    <li key={todo.id}>
                        <input type="checkbox" checked={todo.done} onChange={() => toggleTodo(todo)} />{" "}
                        {todo.task}
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task13;
