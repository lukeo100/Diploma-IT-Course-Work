const recipeName = document.getElementById('recipeName');
const recipeImage = document.getElementById('recipeImage');
const recipeCuisine = document.getElementById('recipeCuisine');
const recipeDifficulty = document.getElementById('recipeDifficulty');
const recipePrepTime = document.getElementById('recipePrepTime');
const recipeIngredients = document.getElementById('recipeIngredients');
const recipeInstructions = document.getElementById('recipeInstructions');
const recipeRating = document.getElementById('recipeRating');

function onRecipeReady(recipe) {
    recipeName.innerText = recipe.name;
    recipeImage.src = recipe.image;
    recipeImage.alt = recipe.name;
    recipeCuisine.innerText = 'Cuisine: ' + recipe.cuisine;
    recipeDifficulty.innerText = 'Difficulty: ' + recipe.difficulty;
    recipePrepTime.innerText = 'Prep: ' + recipe.prepTimeMinutes + ' mins | Cook: ' + recipe.cookTimeMinutes + ' mins';
    recipeRating.innerText = '★ ' + recipe.rating + ' (' + recipe.reviewCount + ' reviews)';

    let ingredientsHTML = '';
    for (let i = 0; i < recipe.ingredients.length; i++) {
        ingredientsHTML = ingredientsHTML + '<li>' + recipe.ingredients[i] + '</li>';
    }
    recipeIngredients.innerHTML = ingredientsHTML;

    let instructionsHTML = '';
    for (let i = 0; i < recipe.instructions.length; i++) {
        instructionsHTML = instructionsHTML + '<li>' + recipe.instructions[i] + '</li>';
    }
    recipeInstructions.innerHTML = instructionsHTML;
}

function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
