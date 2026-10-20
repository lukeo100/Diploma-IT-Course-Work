# 2026-10-20 Web Development: Mantine and Supabase Client CRUD

Remote class (Lewis). One Next.js app, `crud-practice/`, holds both tasks.

Task pages:
- Task 22: Mantine Component Library (https://bki-di.pages.dev/nextjs/pages/tasks/mantine-components/)
- Task 30: Supabase Client CRUD (https://bki-di.pages.dev/nextjs/pages/tasks/supabase-client-crud/)

## Status

- [x] Task 22 Mantine (committed and pushed: "Finished Mantine Task")
- [ ] Task 30 Supabase setup (project, tables, keys, `lib/supabase.ts`)
- [ ] Task 30 Read (Tasks 1 to 4)
- [ ] Task 30 Create (Tasks 5 to 7)
- [ ] Task 30 Update (Tasks 8 to 10)
- [ ] Task 30 Delete (Tasks 11 to 13)
- [ ] Task 30 from memory (Tasks 14 and 15)

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
- Shared components live in `lib/components/` (`navbar.tsx`, `product-card.tsx`)

Components used: Button, Card, Stack, Flex, Group, Text, Title, TextInput, Checkbox, Menu, Anchor, Container, Tour, RichTextEditor.

## Possible clean-up before moving on

- Navbar links use plain `<a href>`, which reloads the page. Next.js `Link` avoids that
- The `/supabase` navbar link 404s until that route exists
- Sign-up and feedback use a `Text` above each input. Mantine inputs have a `label` prop, and passwords have a dedicated `PasswordInput`
- Mix of plain `<h1>` and `<p>` with Mantine `Title` and `Text` on some pages
- Unused imports on `app/page.tsx` and the form pages
- `ProductCard` secondary button uses `light`; the task suggests `outline` for secondary actions
- Check the feedback editor: Highlight control may need its own Tiptap extension, and `--docs-header-height` is a Mantine docs variable that is not defined in this app
- Mantine's docs recommend `ColorSchemeScript` and `mantineHtmlProps` on `<html>` in the root layout
- Task 30 step 5 adds a global CSS rule for buttons, inputs and selects. Decide whether to scope it to the Supabase routes so it does not fight Mantine

## Task 30: plan

- Tables: fruits, songs, todos, movies (RLS off), then one of my own
- Env vars: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` in `.env.local` (not committed)
- Client file and types in `lib/supabase.ts` (same `lib/` folder as the components)
- One page per exercise: `app/taskN/page.tsx` with `"use client";`

## Notes

- `.select()` reads columns (`"*"` for all) and returns a result object, not the rows directly
- `.insert()` takes its own argument; it is not connected to `.select()`
