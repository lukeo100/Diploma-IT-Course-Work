"use client";

// Task 5 (Create): add a fruit
// Skip the insert if either field is empty. Otherwise insert, clear the
// inputs and reload.
// Expected: adding Mango / orange shows it in the list, still there after refresh.

import { useEffect, useState } from "react";
import { supabase, Fruit } from "@/app/lib/supabase";

const Task5 = () => {
    const [fruits, setFruits] = useState<Fruit[]>([]);
    const [name, setName] = useState("");
    const [colour, setColour] = useState("");

    const loadFruits = async () => {
        // TODO: select every row from "fruits", handle the error, then setFruits
        const { data, error } = await supabase.from("fruits").select("*");
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

    const addFruit = async () => {
        // TODO 1: return early if name or colour is empty
        if (!name || !colour) {
            return;
        }
        // TODO 2: insert the new fruit into "fruits"
        const { error } = await supabase.from("fruits").insert({ name, colour });
        if (error) {
            console.error("Error adding fruit:", error);
        } else {
            // Clear the inputs and reload the list
            setName("");
            setColour("");
            loadFruits();
        }
    };

    return (
        <main>
            <h1>Add a fruit</h1>
            <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <input placeholder="Colour" value={colour} onChange={(e) => setColour(e.target.value)} />
            <button onClick={addFruit}>Add fruit</button>
            <ul>
                {fruits.map((fruit) => (
                    <li key={fruit.id}>
                        {fruit.name} - {fruit.colour}
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task5;
