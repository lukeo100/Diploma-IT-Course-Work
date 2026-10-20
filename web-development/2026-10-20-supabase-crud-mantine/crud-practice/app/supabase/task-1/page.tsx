"use client";

import { useEffect, useState } from "react";
import { supabase, Fruit } from "@/app/lib/supabase";

const Task1 = () => {
    const [fruits, setFruits] = useState<Fruit[]>([]);

    const loadFruits = async () => {
        // TODO: select every row from "fruits"
        const { data, error } = await supabase.from("fruits").select("*");
        if (error) {
            console.error("Error fetching fruits:", error);
        } else {
            setFruits(data as Fruit[]);
        }
    };

    useEffect(() => {
        // Safe: loadFruits only sets state after the data arrives
        // eslint-disable-next-line react-hooks/set-state-in-effect
        loadFruits();
    }, []);

    return (
        <main>
            <h1>Fruits</h1>
            <ul>
                {/* TODO: map over fruits */}
                {fruits.map((fruit) => (
                    <li key={fruit.id}>
                        {fruit.name} - {fruit.colour}
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task1;