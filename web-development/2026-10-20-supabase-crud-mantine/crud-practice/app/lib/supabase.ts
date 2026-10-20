// app/lib/supabase.ts
import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL ?? "",
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? "",
);

export type Fruit = { id: number; name: string; colour: string };
export type Song = {
  id: number;
  title: string;
  artist: string;
  rating: number;
};
export type Todo = { id: number; task: string; done: boolean };
export type Movie = {
  id: number;
  title: string;
  year: number;
  watched: boolean;
};
export type Shelter = {
  id: number;
  shelter_name: string;
  address: string;
  capacity: number;
  current_animals: number;
  created_at: string;
  animal_types: string;
};
