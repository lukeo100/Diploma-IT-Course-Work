"use client";

// Task 4 (Sorting and filtering): three lists on one page
//   1. fruits A to Z
//   2. songs by rating, highest first
//   3. todos where done is false
// Expected: fruits sorted A to Z, "Blue Sky" is the first song,
// "Finish homework" is missing from the todo list.

import { useEffect, useState } from "react";
import { supabase, Fruit, Song, Todo } from "@/app/lib/supabase";

const Task4 = () => {
    const [fruits, setFruits] = useState<Fruit[]>([]);
    const [songs, setSongs] = useState<Song[]>([]);
    const [todos, setTodos] = useState<Todo[]>([]);

    const loadAll = async () => {
        // TODO: fruits ordered by name
        const { data: fruitsData, error: fruitsError } = await supabase.from("fruits").select("*").order("name", { ascending: true });
        if (fruitsError) {
            console.error("Error fetching fruits:", fruitsError);
        } else {
            setFruits(fruitsData as Fruit[]);
        }
        // TODO: songs ordered by rating, highest first
        const { data: songsData, error: songsError } = await supabase.from("songs").select("*").order("rating", { ascending: false });
        if (songsError) {
            console.error("Error fetching songs:", songsError);
        } else {
            setSongs(songsData as Song[]);
        }
        // TODO: todos filtered to done = false
        const { data: todosData, error: todosError } = await supabase.from("todos").select("*").eq("done", false);
        if (todosError) {
            console.error("Error fetching todos:", todosError);
        } else {
            setTodos(todosData as Todo[]);
        }
    };

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        loadAll();
    }, []);

    return (
        <main>
            <h1>Sorting and filtering</h1>

            <h2>Fruits (A to Z)</h2>
            <ul>
                {fruits.map((fruit) => (
                    <li key={fruit.id}>
                        {fruit.name} - {fruit.colour}
                    </li>
                ))}
            </ul>

            <h2>Songs (highest rating first)</h2>
            <ul>
                {songs.map((song) => (
                    <li key={song.id}>
                        {song.title} by {song.artist} ({song.rating} stars)
                    </li>
                ))}
            </ul>

            <h2>Todos (not done)</h2>
            <ul>
                {todos.map((todo) => (
                    <li key={todo.id}>
                        {todo.task}
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task4;
