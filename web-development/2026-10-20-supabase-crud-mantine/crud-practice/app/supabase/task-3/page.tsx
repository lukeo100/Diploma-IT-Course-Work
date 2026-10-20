"use client";

// Task 3 (Read): list each task, adding "(done)" to finished ones
// Expected: three tasks, only "Finish homework" shows "(done)".

import { useEffect, useState } from "react";
import { supabase, Todo } from "@/app/lib/supabase";

const Task3 = () => {
    const [todos, setTodos] = useState<Todo[]>([]);

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

    return (
        <main>
            <h1>Todos</h1>
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

export default Task3;
