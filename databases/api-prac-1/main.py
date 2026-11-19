from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

class BookCreate(BaseModel):
    title: str
    price: float

class Book(BookCreate):
    id: int

class Game(BaseModel):
    id: int
    title: str
    price: float

app = FastAPI()

print("starting api")

books: list[Book] = [
    Book(id=1, title="Python Basics", price=39.95),
    Book(id=2, title="Web Development", price=49.95),
    Book(id=3, title="Learning APIs", price=29.95)
]

games: list[Game] = [
    Game(id=1, title="Minecraft", price=39.95),
    Game(id=2, title="Stardew Valley", price=19.95),
    Game(id=3, title="Rocket League", price=29.95)
]

@app.get("/")
def home():
    return {"message": "Welcome to the Books and Games API"}


# Books Endpoints
@app.get("/books")
def get_books():
    return books

@app.get("/books/search")
def search_books(title: str):
    result = [book for book in books if title.lower() in book.title.lower()]
    return result

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}

@app.post("/books")
def add_book(book: BookCreate):
    book_id = len(books) + 1
    new_book = Book(id=book_id, title=book.title, price=book.price)
    books.append(new_book)
    return new_book

# Games Endpoints
@app.get("/games")
def get_games():
    return games

@app.get("/games/search")
def search_games(title: str):
    result = [game for game in games if title.lower() in game.title.lower()]
    return result

@app.get("/games/{game_id}")
def get_game(game_id: int):
    for game in games:
        if game.id == game_id:
            return game
    return {"error": "Game not found"}

@app.post("/games")
def add_game(game: Game):
    game_id = len(games) + 1
    new_game = Game(id=game_id, title=game.title, price=game.price)
    games.append(new_game)
    return new_game