"use client";
const greet = (name: string) => {
    return "Hello, " + name + "!";
};

const double = (n: number) => {
    return n * 2;
};

const add = (a: number, b: number) => {
    return a + b;
};

const Task1Page = () => {
    return (
        <>
            <p>All block bodies</p>
            <p>Greet function: {greet("Luca")}</p>
            <p>Double function: {double(19)}</p>
            <p>Add function: {add(25, 90)}</p>
        </>
    )
};
export default Task1Page;