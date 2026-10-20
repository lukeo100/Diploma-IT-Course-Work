"use client";

// Task 10 (Update): rate a song with + and - buttons that change rating by 1
// Extra: keep the rating between 1 and 5.
// Expected: clicking + on "Slow Walk" until 5 stars keeps 5 after a refresh.

import { useEffect, useState } from "react";
import { supabase, Song } from "@/app/lib/supabase";

const Task10 = () => {
    const [songs, setSongs] = useState<Song[]>([]);

    const loadSongs = async () => {
        // TODO: select every row from "songs" ordered by id, then setSongs
        const { data, error } = await supabase.from("songs").select("*").order("id");
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

    const changeRating = async (song: Song, change: number) => {
        // TODO 1: work out the new rating (extra: clamp between 1 and 5)
        const newRating = Math.max(1, Math.min(5, song.rating + change));
        // TODO 2: update the rating where id matches
        const { error } = await supabase.from("songs").update({ rating: newRating }).eq("id", song.id);
        if (error) {
            console.error("Error changing rating:", error);
        } else {
            // TODO 3: reload the list
            loadSongs();
        }
    };

    return (
        <main>
            <h1>Rate songs</h1>
            <ul>
                {songs.map((song) => (
                    <li key={song.id}>
                        {song.title} by {song.artist} ({song.rating} stars){" "}
                        <button onClick={() => changeRating(song, -1)}>-</button>
                        <button onClick={() => changeRating(song, 1)}>+</button>
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task10;
