"use client";
const areaOfRectangle = (length: number, width: number) => length * width;
const addGST = (price: number) => price * 1.1;
const initials = (first: string, last: string) => `${first.charAt(0)}.${last.charAt(0)}.`; // I worked out on my own that charAt(0) also works, just like first[0]
const PriceTag = ({ price }: { price: number }) => <p>Price: ${price}</p>;

const Task6Page = () => (
    <>
        <p>Area of rectangle: {areaOfRectangle(10, 5)}</p>
        <p>Price with GST: ${addGST(100).toFixed(2)}</p>
        <p>Initials for Luca Doe: {initials("Luca", "Doe")}</p>
        <PriceTag price={2} />
        <PriceTag price={92} />
        <PriceTag price={521} />

    </>
);

export default Task6Page;


