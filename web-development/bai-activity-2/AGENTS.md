# Agent Instructions

## Image Search

When you need to find an image, use the Unsplash API to search and verify images before using them.

### Searching for Images

Use this endpoint to search Unsplash for photos:

```
GET https://unsplash.com/napi/search/photos?page=1&per_page=20&query={search_term}
```

Example with curl:
```bash
curl -s "https://unsplash.com/napi/search/photos?page=1&per_page=20&query=capybara" | head -c 5000
```

### Parsing the Response

The response is JSON. Each result has a `urls` object with different sizes:

```json
{
  "results": [
    {
      "id": "...",
      "description": "...",
      "urls": {
        "raw": "https://images.unsplash.com/photo-xxx",
        "full": "https://images.unsplash.com/photo-xxx",
        "regular": "https://images.unsplash.com/photo-xxx",
        "small": "https://images.unsplash.com/photo-xxx",
        "thumb": "https://images.unsplash.com/photo-xxx"
      }
    }
  ]
}
```

### Using Images

To use an image in CSS, append query parameters for sizing:

```css
background-image: url('https://images.unsplash.com/photo-xxx?w=800&q=80');
```

Parameters:
- `w=800` - width in pixels
- `q=80` - quality (1-100)

### Workflow

1. Search using the API endpoint with your query
2. Parse the JSON response to get image URLs
3. Pick a suitable image from the results
4. Use the `regular` or `full` URL with sizing parameters

### Example: Finding a Capybara Image

```bash
# Search
curl -s "https://unsplash.com/napi/search/photos?page=1&per_page=20&query=capybara"

# Extract first image URL
curl -s "https://unsplash.com/napi/search/photos?page=1&per_page=20&query=capybara" | grep -o '"regular":"[^"]*"' | head -1
```

Then use that URL in your CSS.

---

## JavaScript Guidelines

This project targets beginners. Write code that is easy to read and understand.

### Keep It Simple

- Use `const` for variables that don't change, `let` for variables that do
- Never use `var`
- No arrow functions (`() => {}`)
- No anonymous functions (`function() {}`)
- Always create a named function and reference it
- Register event listeners individually, don't loop through elements
- Avoid advanced patterns (closures, IIFE, chaining, etc.)

### Example: Do This

```js
function onNameBlur() {
    validateName(nameInput, nameError);
}

nameInput.addEventListener('blur', onNameBlur);
```

### Not This

```js
nameInput.addEventListener('blur', () => validateName(nameInput, nameError));
```

### Comments

Don't over-comment. Only add comments where code is not obvious or where context is needed. Well-named functions and variables should be self-documenting.

```js
// Good - no comment needed
function validateEmail(input, error) { ... }

// Good - comment explains why
// Defer validation until user leaves field
input.addEventListener('blur', validateEmail);
```

### File Structure

- Keep HTML, CSS, and JS in separate files
- Use ES6 modules (`type="module"`) for imports/exports
- Validation or reusable logic goes in its own file
- Main script handles DOM setup and event binding
