"use client";
const makeUser = (name: string, age: number) => {
    return (
        { name: name, age: age }
    );
};

const makeProduct = (title: string, price: number) => {
    return (
        { title: title, price: price, onSale: false }
    );
};

const makeUser2 = (name: string, age: number) => (
    { name: name, age: age }
);

const makeProduct2 = (title: string, price: number) => (
    { title: title, price: price, onSale: false }
);

const user = makeUser("Luca", 19);
const product = makeProduct("Lunch", 22);


const user2 = makeUser2("John Smith", 25);
const product2 = makeProduct2("Dinner", 50);

const Task4Page = () => {
    return (
        <div className="space-y-4">
            <h1>Task 4 - Arrow functions returning objects</h1>
            <p>Block body version:</p>
            <p>{user.name} is {user.age}</p>
            <p>Product of the day: {product.title} ................ ${product.price} ({product.onSale ? "ON SALE" : "RRP"})</p>

            <p>Implicit returns version:</p>
            <p>{user2.name} is {user2.age}</p>
            <p>Product of the day: {product2.title} ................ ${product2.price} ({product2.onSale ? "ON SALE" : "RRP"})</p>
        </div>
    );
};

export default Task4Page;