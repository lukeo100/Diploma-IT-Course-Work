# Part 1 — Create the Next.js app (step by step)

> This is a reminder in case you have forgotten the exact steps.

1. Open a terminal and go to the folder where you want to keep your projects:

   ```bash
   cd ~/projects
   ```

2. Create a new Next.js app called `countries-app`:

   ```bash
   npx create-next-app@latest countries-app
   ```

   - If it asks to install the `create-next-app` package, type `y` and press Enter.

3. Answer the prompts like this (use **TypeScript**):

   ```text
   Would you like to use TypeScript? → Yes
   Would you like to use ESLint? → Yes
   Would you like to use Tailwind CSS? → No
   Would you like to use `src/` directory? → No
   Would you like to use App Router? → Yes
   Would you like to use Turbopack? → Yes
   Would you like to customize the import alias? → No
   ```

4. Move into the project and start the dev server:

   ```bash
   cd countries-app
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000). You should see the default Next.js welcome page.

6. Stop the server with `Ctrl+C`. You are ready to build.

> We do **not** need to install `@supabase/supabase-js`. We will use the browser/server built-in `fetch`.
>
> Because we chose TypeScript, our files will end in `.ts` (plain code) and `.tsx` (code that contains JSX/components).

---

[← Part 0](./01-part-0-supabase-setup.md) | [Back to index](./README.md) | [Next: Part 2 — Typed fetch functions →](./03-part-2-api-module.md)
