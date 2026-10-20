"use client";

// Task 11 (Delete): delete a fruit
// Expected: Grape is gone after a refresh and no longer in the Table Editor.

import { useEffect, useState } from "react";
import { supabase, Fruit } from "@/app/lib/supabase";

const Task11 = () => {
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

    const deleteFruit = async (id: number) => {
        // TODO 1: delete the row where id matches
        const { error } = await supabase.from("fruits").delete().eq("id", id);
        // TODO 2: check for an error
        if (error) {
            console.error("Error deleting fruit:", error);
        } else {
            // TODO 3: reload the list
            loadFruits();
        }
    };

    return (
        <main>
            <h1>Delete a fruit</h1>
            <ul>
                {fruits.map((fruit) => (
                    <li key={fruit.id}>
                        {fruit.name} - {fruit.colour}{" "}
                        <button onClick={() => deleteFruit(fruit.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task11;
