# 2026-10-20 Web Development: Mantine and Supabase Client CRUD

Remote class (Lewis). One Next.js app, `crud-practice/`, holds both tasks.

Task pages:
- Task 22: Mantine Component Library (https://bki-di.pages.dev/nextjs/pages/tasks/mantine-components/)
- Task 30: Supabase Client CRUD (https://bki-di.pages.dev/nextjs/pages/tasks/supabase-client-crud/)

## Status

- [x] Task 22 Mantine (committed and pushed: "Finished Mantine Task")
- [x] Task 30 setup (Supabase "Learning" project, tables, keys, `app/lib/supabase.ts`)
- [x] Task 30 Read (Tasks 1 to 4)
- [x] Task 30 Create (Tasks 5 to 7)
- [x] Task 30 Update (Tasks 8 to 10)
- [x] Task 30 Delete (Tasks 11 to 13)
- [x] Task 30 from memory (Task 14 movies, Task 15 own table: animal shelters)
- [x] Committed and pushed: "Finished Supabase Client Tasks"

## Project layout

- `app/layout.tsx`: Mantine stylesheet, `MantineProvider`, shared `Navbar`
- `app/page.tsx`: home page with a Mantine `Tour` of the navbar
- `app/mantine/`: product showcase, `sign-up`, `feedback` (Tiptap editor)
- `app/supabase/page.tsx`: overview with a card and short description for each task
- `app/supabase/task-1` to `task-15`: one page per exercise, each starting with `"use client";`
- `app/lib/supabase.ts`: Supabase client and the `Fruit`, `Song`, `Todo`, `Movie` and `Shelter` types
- `app/lib/supabase-tasks.ts`: list of the 15 tasks used by both the overview page and the navbar menu
- `app/lib/components/`: `navbar.tsx`, `product-card.tsx`, `logo.tsx`
- `.env.local` (not committed): `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`

## Task 22: what was built

Routes:
- `/` home page with a Mantine `Tour` of the navbar
- `/mantine` product showcase (reusable `ProductCard` component)
- `/mantine/sign-up` sign-up form
- `/mantine/feedback` feedback form with a Tiptap rich text editor (`@mantine/tiptap`)

Setup notes:
- Packages: `@mantine/core`, `@mantine/hooks`, plus `@mantine/tiptap` and the Tiptap packages for the editor
- `app/layout.tsx` imports `@mantine/core/styles.css` and wraps everything in `MantineProvider`. Without the stylesheet, components render unstyled
- Mantine components use state and events, so pages and components using them start with `"use client";`
- `Stack` for vertical spacing, `Group` and `Flex` for rows

Components used: Button, Card, Stack, Flex, Group, Text, Title, TextInput, Checkbox, Menu, Anchor, Container, Tour, RichTextEditor, Badge, SimpleGrid.

## Task 30: what was built

Database (Supabase project "Learning", RLS off for practice data):
- `fruits` (name, colour), `songs` (title, artist, rating default 3), `todos` (task, done default false), `movies` (title, year, watched default false), each with an auto-generated `id`
- Own table for Task 15: `shelters` (shelter_name, address, capacity, current_animals, animal_types, created_at)

Pages by section:
- Read (1 to 4): `.select()` with sorting and filtering on the last page
- Create (5 to 7): `.insert()`, with the rating converted to a number and `done` left to the database default
- Update (8 to 10): `.update()` matched on `id`
- Delete (11 to 13): `.delete()` by `id`, then one query for all finished todos
- From memory (14 and 15): movie watchlist and the shelters table with list, add, update and delete

Notes:
- `.select()` reads columns (`"*"` for all) and returns a result object, not the rows directly
- `.insert()` takes its own argument; it is not connected to `.select()`
- `.update()` and `.delete()` need a filter such as `.eq("id", id)` so they only touch the intended row

## Open items

- A few leftover `// TODO` comments remain in the task files (for example Tasks 3, 13, 14 and 15) even where the code is written
- Check each task's expected result after a page refresh, as listed in the comment at the top of each file
- Task 15: `Shelter.animal_types` is typed as a `string` but the add function sends an array of strings; check the column type matches
- Navbar links use plain `<a href>`, which reloads the page. Next.js `Link` avoids that
- Sign-up and feedback use a `Text` above each input. Mantine inputs have a `label` prop, and passwords have a dedicated `PasswordInput`
- Mix of plain `<h1>` and `<p>` with Mantine `Title` and `Text` on some pages, and some unused imports
- `ProductCard` secondary button uses `light`; the task suggests `outline` for secondary actions
- Feedback editor: the Highlight control may need its own Tiptap extension, and `--docs-header-height` is a Mantine docs variable that is not defined in this app
- Mantine's docs recommend `ColorSchemeScript` and `mantineHtmlProps` on `<html>` in the root layout
- Task 30 step 5 suggests a global CSS rule for buttons, inputs and selects; none is in `globals.css` yet, so decide whether to scope one to the Supabase routes so it does not fight Mantine
