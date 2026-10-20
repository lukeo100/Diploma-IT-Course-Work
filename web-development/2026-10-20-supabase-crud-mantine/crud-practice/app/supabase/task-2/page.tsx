"use client";

// Task 2 (Read): show each song as "Title by Artist (N stars)"
// Expected: all three songs are shown in that format.

import { useEffect, useState } from "react";
import { supabase, Song } from "@/app/lib/supabase";

const Task2 = () => {
    const [songs, setSongs] = useState<Song[]>([]);

    const loadSongs = async () => {
        // TODO: select every row from "songs", handle the error, then setSongs
        const { data, error } = await supabase.from("songs").select("*");
        if (error) {
            console.error("Error fetching songs:", error);
        } else {
            setSongs(data as Song[]);
        }
    };

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        loadSongs();
    }, []);

    return (
        <main>
            <h1>Songs</h1>
            <ul>
                {/* TODO: map over songs and show "Title by Artist (N stars)" */}
                {songs.map((song) => (
                    <li key={song.id}>
                        {song.title} by {song.artist} ({song.rating} stars)
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task2;
