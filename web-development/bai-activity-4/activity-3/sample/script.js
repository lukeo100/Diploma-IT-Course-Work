const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const recipeList = document.getElementById('recipeList');
const status = document.getElementById('status');

function onSearchDataReady(data) {
    const recipes = data.recipes;

    if (recipes.length === 0) {
        status.innerText = 'No recipes found for "' + searchInput.value + '"';
        recipeList.innerHTML = '<p class="empty">Try searching for "pizza", "chicken", or "pasta".</p>';
        return;
    }

    status.innerText = 'Found ' + recipes.length + ' recipes for "' + searchInput.value + '"';

    let html = '';
    for (let i = 0; i < recipes.length; i++) {
        const recipe = recipes[i];
        html = html + '<div class="card">';
        html = html + '<img src="' + recipe.image + '" alt="' + recipe.name + '">';
        html = html + '<div class="card-body">';
        html = html + '<h3>' + recipe.name + '</h3>';
        html = html + '<p class="meta">' + recipe.cuisine + ' · ' + recipe.difficulty + ' · ' + recipe.prepTimeMinutes + ' mins</p>';
        html = html + '<p class="rating">★ ' + recipe.rating + ' (' + recipe.reviewCount + ' reviews)</p>';
        html = html + '</div>';
        html = html + '</div>';
    }

    recipeList.innerHTML = html;
}

function onSearchResponseReady(response) {
    response.json().then(onSearchDataReady);
}

function onSearchClick() {
    const query = searchInput.value.trim();

    if (query === '') {
        status.innerText = 'Please type something to search';
        return;
    }

    status.innerText = 'Searching for "' + query + '"...';
    recipeList.innerHTML = '';

    fetch('https://dummyjson.com/recipes/search?q=' + query).then(onSearchResponseReady);
}

searchButton.addEventListener('click', onSearchClick);
