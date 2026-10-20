"use client";

// Task 6 (Create): add a song with title, artist and rating inputs
// Convert the rating to a number before inserting.
// Expected: a song added with rating 5 appears as "(5 stars)".

import { useEffect, useState } from "react";
import { supabase, Song } from "@/app/lib/supabase";

const Task6 = () => {
    const [songs, setSongs] = useState<Song[]>([]);
    const [title, setTitle] = useState("");
    const [artist, setArtist] = useState("");
    const [rating, setRating] = useState("");

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

    const addSong = async () => {
        // TODO 1: return early if a field is empty
        if (!title || !artist || !rating) {
            return;
        }
        // TODO 2: convert rating to a number, then insert into "songs"
        const numericRating = parseInt(rating, 10);
        const { error } = await supabase.from("songs").insert({ title, artist, rating: numericRating });
        if (error) {
            console.error("Error adding song:", error);
        } else {
            // Clear the inputs and reload the list
            setTitle("");
            setArtist("");
            setRating("");
            loadSongs();
        }
    };

    return (
        <main>
            <h1>Add a song</h1>
            <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
            <input placeholder="Artist" value={artist} onChange={(e) => setArtist(e.target.value)} />
            <input placeholder="Rating" value={rating} onChange={(e) => setRating(e.target.value)} />
            <button onClick={addSong}>Add song</button>
            <ul>
                {songs.map((song) => (
                    <li key={song.id}>
                        {song.title} by {song.artist} ({song.rating} stars)
                    </li>
                ))}
            </ul>
        </main>
    );
};

export default Task6;
