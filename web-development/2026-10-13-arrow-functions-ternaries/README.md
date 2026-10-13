# Tuesday 13 Oct 2026: Arrow Functions and Ternaries

Web Development with Lewis, Semester 2, Week 2. Studying from home.

Course site: https://bki-di.pages.dev/nextjs/

## End of day summary

**Completed**

- Read Arrow Functions and Conditional Rendering, and checked my understanding of both
- Skimmed the useEffect and fetch arrows task page
- Arrow Function Basics (`activity-01`), all exercises 4.2 to 4.8, saved as `app/task-1` to `app/task-7`

**Still to do**

- Ternary Basics (`activity-03`): homework, to finish before the next class
- Knowledge assessment (open book): to complete later this week
- Stretch exercises (useEffect and fetch arrows) and the optional Pet Adoption Board: not attempted

## Focus today

- Arrow functions (block body, implicit return, returning objects, components, event handlers, array callbacks)
- The ternary operator and conditional rendering (text, attributes, components, `&&`, nested ternaries)

## Plan

Rough timings, adjust as needed.

| Order | Block | Link | Time |
|-------|-------|------|------|
| 1 | Read: Arrow Functions | https://bki-di.pages.dev/nextjs/pages/resources/nextjs/arrow-functions/ | 15 min |
| 2 | Read: Conditional Rendering | https://bki-di.pages.dev/nextjs/pages/resources/nextjs/conditional-rendering/ | 15 min |
| 3 | Skim: Arrow Functions in useEffect and fetch (task page, read through before attempting) | https://bki-di.pages.dev/nextjs/pages/tasks/useeffect-fetch-arrows/ | 10 min |
| 4 | Task: Arrow Function Basics (`activity-01`) | https://bki-di.pages.dev/nextjs/pages/tasks/arrow-function-basics/ | 45 min |
| 5 | Task: Ternary Basics (`activity-03`) | https://bki-di.pages.dev/nextjs/pages/tasks/ternary-basics/ | homework |
| 6 | Knowledge assessment (open book) | link to be added | later this week |
| 7 | Stretch: useEffect and fetch arrows (`activity-07`), tasks 1 to 3 first | see block 3 | not attempted |
| 8 | Optional project: Pet Adoption Board | https://bki-di.pages.dev/nextjs/pages/tasks/pet-adoption-board/ | not attempted |

## Checklist

- [x] Read Arrow Functions
- [x] Read Conditional Rendering
- [x] Skim useEffect and fetch arrows
- [x] Arrow Function Basics (activity-01), tasks 1 to 7
- [ ] Ternary Basics (activity-03), tasks 1 to 7
- [ ] Knowledge assessment
- [ ] Stretch: activity-07
- [ ] Optional: Pet Adoption Board

## Folder layout

Create each Next.js app inside this folder, for example:

```
npx create-next-app@latest activity-01
```

Press Enter to accept all defaults. Keep `"use client";` on line 1 of every task page.

## Notes

### Arrow functions

- Block body: braces hold statements and need an explicit `return`, otherwise the result is `undefined`
- Implicit return: no braces and no `return`, a single expression is returned automatically
- Returning an object from an implicit return needs brackets: `() => ({ x: 1 })`
- Event handlers with arguments need a wrapper: `onClick={() => handleDelete(item.id)}`
- Arrow functions are stored in a `const` so the name cannot be reassigned or redeclared by accident
- Put a semicolon after the closing `}` of a block-body arrow
- Page files should only have a default export
- Use `const` instead of `let` for values that are never reassigned
- Avoid parameter names that match outer variables, the parameter hides the outer one

### Arrow Function Basics (activity-01)

Completed all exercises 4.2 to 4.8, saved as `activity-01/app/task-1` to `task-7`.

| Task | Exercise | What it covers |
|------|----------|----------------|
| task-1 | 4.2 Block bodies | `greet`, `double`, `add` with `return` |
| task-2 | 4.3 Implicit returns | same functions, no braces |
| task-3 | 4.4 Three ways | declaration, block body and implicit return for four functions |
| task-4 | 4.5 Returning objects | `makeUser` and `makeProduct`, both styles, brackets around the object |
| task-5 | 4.6 Components | `Header`, `Footer`, `Greeting` as arrows, plus destructured props |
| task-6 | 4.7 Create your own | `areaOfRectangle`, `addGST`, `initials`, `PriceTag` |
| task-7 | 4.8 From memory | rabbit shelter overview with five arrow functions |

### Ternaries and conditional rendering

- `if` is a statement and cannot go inside JSX braces, a ternary produces a value so it can
- `count && <p>...</p>` with `count` as `0` shows a `0` on the page, use `count > 0 && ...`
- Nested ternaries stop at the first true condition, so check the most specific condition first

### Things that tripped me up

- Removing the brackets around a returned object gives "Left side of comma operator is unused and has no side effects", because the braces are read as a function body and `name:` as a label
- In task-4 the second section displayed the block-body results, so the implicit functions were never called. Check which function produced each value on the page

### Questions for Lewis

None recorded today.

## Knowledge assessment

Not yet completed. Open book, to be done later this week.
