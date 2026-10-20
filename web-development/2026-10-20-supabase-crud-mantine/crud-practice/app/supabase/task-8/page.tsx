"use client";

// Task 8 (Update): rename a fruit
// Tip from the task: order by id when loading so rows do not jump after updates.
// Expected: renaming Lime to Lemon still shows Lemon after a refresh.

import { useEffect, useState } from "react";
import { supabase, Fruit } from "@/app/lib/supabase";

const Task8 = () => {
    const [fruits, setFruits] = useState<Fruit[]>([]);

    const loadFruits = async () => {
        // TODO: select every row from "fruits" ordered by id, then setFruits
        const { data, error } = await supabase.from("fruits").select("*").order("id");
        if (error) {
            console.error("Error fetching fruits:", error);
        } else {
            setFruits(data as Fruit[]);
        }
    };

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        loadFruits();
    }, []);

    const renameFruit = async (id: number) => {
        const newName = prompt("New name?");
        // TODO 1: return early if newName is empty or null
        if (!newName) {
            return;
        }
        // TODO 2: update the name where id matches
        const { error } = await supabase.from("fruits").update({ name: newName }).eq("id", id);
        if (error) {
            console.error("Error renaming fruit:", error);
        } else {
            // TODO 3: reload the list
            loadFruits();
        }
    };

    return (
        <main>
            <h1>Rename a fruit</h1>
            <ul>
                {fruits.map((fruit) => (
                    <li key={fruit.id}>
                        {fruit.name} - {fruit.colour}{" "}
                        <button onClick={() => renameFruit(fruit.id)}>Rename</button>
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task8;
