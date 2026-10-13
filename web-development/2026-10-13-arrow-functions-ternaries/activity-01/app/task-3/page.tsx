"use client";
// Function declarations
function square1(n: number) {
    return n * n;
}

function fullName1(first: string, last: string) {
    return `${first} ${last}`;
}

function toCelsius1(fahrenheitNumber: number) {
    return (fahrenheitNumber - 32) * 5 / 9;
}

function shout1(s: string) {
    return s.toUpperCase();
}

// Block body arrow functions
const square2 = (n: number) => {
    return n * n;
}

const fullName2 = (first: string, last: string) => {
    return `${first} ${last}`;
}

const toCelsius2 = (fahrenheitNumber: number) => {
    return (fahrenheitNumber - 32) * 5 / 9;
}

const shout2 = (s: string) => {
    return s.toUpperCase();
}

// Implicit returns arrow functions
const square3 = (n: number) => n * n;

const fullName3 = (first: string, last: string) => `${first} ${last}`;

const toCelsius3 = (fahrenheitNumber: number) => (fahrenheitNumber - 32) * 5 / 9;

const shout3 = (s: string) => s.toUpperCase();

const Task3Page = () => {
    // Display all the different variations
    return (
        <>
            <h1 className="text-2xl mb-4">Task 3 - Three different function declarations</h1>

            <div className="mb-5">
                <h3 className="text-xl">Function declarations</h3>
                <p>square1(4) = {square1(4)}</p>
                <p>fullName1("Luca", "T") = {fullName1("Luca", "T")}</p>
                <p>toCelsius1(68) = {toCelsius1(68).toFixed(2)}</p>
                <p>shout1("hello") = {shout1("hello")}</p>
            </div>

            <div className="mb-5">
                <h3 className="text-xl">Block body arrow functions</h3>
                <p>square2(4) = {square2(4)}</p>
                <p>fullName2("Luca", "T") = {fullName2("Luca", "T")}</p>
                <p>toCelsius2(68) = {toCelsius2(68).toFixed(2)}</p>
                <p>shout2("hello") = {shout2("hello")}</p>
            </div>

            <div>
                <h3 className="text-xl">Implicit return arrow functions</h3>
                <p>square3(4) = {square3(4)}</p>
                <p>fullName3("Luca", "T") = {fullName3("Luca", "T")}</p>
                <p>toCelsius3(68) = {toCelsius3(68).toFixed(2)}</p>
                <p>shout3("hello") = {shout3("hello")}</p>
            </div>

        </>
    );

};
export default Task3Page;