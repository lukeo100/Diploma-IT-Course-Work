const recipeList = document.getElementById('recipeList');
const status = document.getElementById('status');

function onDataReady(data) {
    const recipes = data.recipes;

    status.innerText = 'Found ' + recipes.length + ' recipes';

    let html = '';
    for (let i = 0; i < recipes.length; i++) {
        const recipe = recipes[i];
        html = html + '<div class="card">';
        html = html + '<img src="' + recipe.image + '" alt="' + recipe.name + '">';
        html = html + '<div class="card-body">';
        html = html + '<h3>' + recipe.name + '</h3>';
        html = html + '<p class="meta">' + recipe.cuisine + ' · ' + recipe.difficulty + '</p>';
        html = html + '<p class="rating">★ ' + recipe.rating + '</p>';
        html = html + '<p class="time">Prep: ' + recipe.prepTimeMinutes + ' mins | Cook: ' + recipe.cookTimeMinutes + ' mins</p>';
        html = html + '</div>';
        html = html + '</div>';
    }

    recipeList.innerHTML = html;
}

function onResponseReady(response) {
    response.json().then(onDataReady);
}

fetch('https://dummyjson.com/recipes').then(onResponseReady);
