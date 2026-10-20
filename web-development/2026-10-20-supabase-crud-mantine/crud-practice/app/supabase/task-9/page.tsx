"use client";

// Task 9 (Update): tick off a todo
// A checkbox bound to "done". Clicking it saves the opposite value.
// Expected: ticking "Buy milk" persists after refresh, and unticking persists too.

import { useEffect, useState } from "react";
import { supabase, Todo } from "@/app/lib/supabase";

const Task9 = () => {
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
        // TODO 1: update "done" to the opposite value where id matches
        const { error } = await supabase.from("todos").update({ done: !todo.done }).eq("id", todo.id);
        if (error) {
            console.error("Error toggling todo:", error);
        } else {
            // TODO 2: reload the list
            loadTodos();
        }
    };

    return (
        <main>
            <h1>Tick off todos</h1>
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

export default Task9;
