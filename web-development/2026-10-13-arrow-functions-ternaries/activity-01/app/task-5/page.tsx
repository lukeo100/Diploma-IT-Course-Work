"use client";
const Header = () => {
    return <h1>My Arrow Function Site</h1>;
};

const Footer = () => {
    return <p>© 2026 Me</p>;
};

const Greeting = (props: { name: string }) => {
    return <p>Welcome back, {props.name}!</p>;
};

const Header2 = () => <h1>My Arrow Function Site</h1>;

const Footer2 = () => <p>© 2026 Me</p>;

const Greeting2 = (props: { name: string }) => <p>Welcome back, {props.name}!</p>;

const Greeting3 = ({ name }: { name: string }) => <p>Welcome back, {name}!</p>;


const Task5Page = () => {
    return (
        <>
            <div style={{ marginBottom: "2rem" }}>
                <h1>Block body returns:</h1>
                <Header />
                <Greeting name="Alex" />
                <Footer />
            </div>

            <div style={{ marginBottom: "2rem" }}>
                <h1>Implicit returns:</h1>
                <Header2 />

                <div style={{ margin: "0.75rem 0" }}>
                    <label>Non destructured props: </label>
                    <Greeting2 name="Jo" />
                </div>

                <div style={{ margin: "0.75rem 0" }}>
                    <label>Destructured props: </label>
                    <Greeting3 name="Sam" />
                </div>

                <Footer2 />
            </div>
        </>
    );
};

export default Task5Page;