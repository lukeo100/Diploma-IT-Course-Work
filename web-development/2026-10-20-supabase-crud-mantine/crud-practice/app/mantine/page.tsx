"use client";

import ProductCard from '@/app/lib/components/product-card';
import { Flex, Stack } from '@mantine/core';

export default function Demo() {
    return (
        <Stack gap="md" p="md" justify="center" align="center">
            <h1>Product Showcase</h1>
            <p>Explore our range of products below. Luca will not accept any orders.</p>
            <Flex
                mih={50}
                gap="md"
                justify="center"
                align="flex-start"
                direction="row"
                wrap="wrap"
            >
                {/* Product Card */}
                <ProductCard name="Everyday Backpack" description="A versatile backpack for everyday use." price={79.99} />
                <ProductCard name="Wireless Headphones" description="High-quality sound with noise cancellation." price={199.99} />
                <ProductCard name="Smartwatch" description="Stay connected and track your fitness." price={149.99} />
                <ProductCard name="Portable Charger" description="Keep your devices charged on the go." price={29.99} />
                <ProductCard name="Bluetooth Speaker" description="Enjoy music anywhere with this portable speaker." price={49.99} />
                <ProductCard name="Gaming Mouse" description="Precision and comfort for gamers." price={59.99} />
                <ProductCard name="4K Monitor" description="Experience stunning visuals with this 4K monitor." price={399.99} />
                <ProductCard name="Mechanical Keyboard" description="A tactile typing experience for enthusiasts." price={89.99} />
                <ProductCard name="Fitness Tracker" description="Monitor your health and activity levels." price={99.99} />
                <ProductCard name="Noise-Canceling Earbuds" description="Immerse yourself in music without distractions." price={129.99} />
                <ProductCard name="Smart Home Hub" description="Control your smart devices from one central hub." price={149.99} />
                <ProductCard name="Action Camera" description="Capture your adventures in high definition." price={249.99} />
                <ProductCard name="E-Reader" description="Read your favorite books on the go." price={119.99} />
                <ProductCard name="VR Headset" description="Step into virtual reality experiences." price={299.99} />
                <ProductCard name="Segway Ninebot" description="A fun and efficient way to get around." price={499.99} />



            </Flex>
        </Stack>
    );
}