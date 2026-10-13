"use client";
const greet = (name: string) => "Hello, " + name + "!";
const double = (n: number) => n * 2;
const add = (a: number, b: number) => a + b;

const Task2Page = () => {
    return (
        <>
            <p>All implicit returns</p>
            <p>Greet function: {greet("Implicit Luca")}</p>
            <p>Double function: {double(32)}</p>
            <p>Add function: {add(76, 83)}</p>
        </>
    )
};
export default Task2Page;