"use client";

// Task 14 (All four from memory): movie watchlist
// Try this without looking back at the earlier pages.
//   - list movies newest first
//   - add a movie (title and year)
//   - toggle "watched"
//   - delete a movie
// Expected: an added movie can be ticked, the tick persists after refresh,
// and the movie can then be deleted.

import { useEffect, useState } from "react";
import { supabase, Movie } from "@/app/lib/supabase";

const Task14 = () => {
    const [movies, setMovies] = useState<Movie[]>([]);
    const [title, setTitle] = useState("");
    const [year, setYear] = useState("");

    const loadMovies = async () => {
        const { data, error } = await supabase.from("movies").select("*").order("title", { ascending: true });
        if (error) {
            alert(error.message);
            return;
        } else {
            setMovies(data);
        }
    }

    const addMovie = async (newMovieTitle: string, newMovieYear: number, newMovieWatched: boolean = false) => {
        if (!newMovieTitle || !newMovieYear) {
            alert("Please provide both title and year.");
            return;
        }

        const { data, error } = await supabase.from("movies").insert({ title: newMovieTitle, year: newMovieYear, watched: newMovieWatched });
        if (error) {
            alert(error.message);
            return;
        } else {
            loadMovies();
        }
    }

    const markAsWatched = async (movieId: number, watched: boolean) => {
        const { data, error } = await supabase.from("movies").update({ watched }).eq("id", movieId);
        if (error) {
            alert(error.message);
            return;
        } else {
            loadMovies();
        }
    }

    const deleteMovie = async (movieId: number) => {
        const { data, error } = await supabase.from("movies").delete().eq("id", movieId);
        if (error) {
            alert(error.message);
            return;
        } else {
            loadMovies();
        }
    }

    useEffect(() => {
        // TODO: load the movies
        loadMovies();
    }, []);

    return (
        <main>
            <h1>Movie watchlist</h1>
            {/* TODO: inputs, add button, list with watched checkbox and delete button */}
            <ol>
                {movies.map((movie) => {
                    return (
                        <li key={movie.id}>{movie.title} ({movie.year}) <input type="checkbox" checked={movie.watched} onChange={() => { markAsWatched(movie.id, !movie.watched); }} /> <button onClick={() => { deleteMovie(movie.id); }}>Delete</button></li>
                    )
                })}
            </ol>
            <input id="add-movie-input" type="text" placeholder="Add a new movie.." onChange={(event) => setTitle(event.currentTarget.value)} />
            <input id="add-movie-year-input" type="number" placeholder="Year" onChange={(event) => setYear(event.currentTarget.value)} />
            <button id="add-movie-button" onClick={() => addMovie(title, parseInt(year))}>Add movie</button>
        </main>
    );
}

export default Task14;
