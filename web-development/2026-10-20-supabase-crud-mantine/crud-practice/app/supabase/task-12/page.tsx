"use client";

// Task 12 (Delete): ask for confirmation with confirm() before deleting a song
// Expected: cancelling keeps the song, OK removes it.

import { useEffect, useState } from "react";
import { supabase, Song } from "@/app/lib/supabase";

const Task12 = () => {
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

    const deleteSong = async (id: number) => {
        // TODO 1: ask with confirm() and stop if the user cancels
        if (!confirm("Are you sure you want to delete this song?")) {
            return;
        }
        // TODO 2: delete the row where id matches and check for an error
        const { error } = await supabase.from("songs").delete().eq("id", id);
        if (error) {
            console.error("Error deleting song:", error);
        } else {
            // TODO 3: reload the list
            loadSongs();
        }
    };

    return (
        <main>
            <h1>Delete a song</h1>
            <ul>
                {songs.map((song) => (
                    <li key={song.id}>
                        {song.title} by {song.artist} ({song.rating} stars){" "}
                        <button onClick={() => deleteSong(song.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task12;
