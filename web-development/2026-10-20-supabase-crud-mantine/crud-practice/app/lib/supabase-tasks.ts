export type SupabaseTask = {
    n: number;
    section: "Read" | "Create" | "Update" | "Delete" | "From memory";
    title: string;
    description: string;
};

export const supabaseTasks: SupabaseTask[] = [
    { n: 1, section: "Read", title: "Read fruits", description: "Load all fruits in a useEffect and list their names." },
    { n: 2, section: "Read", title: "Read songs", description: "Show each song as Title by Artist (N stars)." },
    { n: 3, section: "Read", title: "Read todos", description: "List each task and mark finished ones with (done)." },
    { n: 4, section: "Read", title: "Sorting and filtering", description: "Fruits A to Z, songs by rating, and only the todos that are not done." },
    { n: 5, section: "Create", title: "Add a fruit", description: "Name and colour inputs that insert a new fruit and reload." },
    { n: 6, section: "Create", title: "Add a song", description: "Title, artist and rating inputs, with the rating converted to a number." },
    { n: 7, section: "Create", title: "Add a todo", description: "A single task input that relies on the database default for done." },
    { n: 8, section: "Update", title: "Rename a fruit", description: "A Rename button that prompts for a new name and updates the matching row." },
    { n: 9, section: "Update", title: "Tick off a todo", description: "A checkbox that saves the opposite value of done." },
    { n: 10, section: "Update", title: "Rate a song", description: "Plus and minus buttons that change the rating, kept between 1 and 5." },
    { n: 11, section: "Delete", title: "Delete a fruit", description: "A Delete button that removes the row matching the id." },
    { n: 12, section: "Delete", title: "Delete a song", description: "Asks for confirmation before deleting." },
    { n: 13, section: "Delete", title: "Clear finished todos", description: "One query that deletes every todo where done is true." },
    { n: 14, section: "From memory", title: "Movie watchlist", description: "List, add, toggle watched and delete movies without looking back." },
    { n: 15, section: "From memory", title: "Your own table", description: "Build all four operations for a table of your own design." },
];

export const supabaseTaskHref = (n: number) => `/supabase/task-${n}`;
