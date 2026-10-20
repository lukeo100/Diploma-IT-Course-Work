"use client";
import { Button, Card, Group, Text, Title } from '@mantine/core';

interface ProductCardProps {
    name: string;
    description: string;
    price: number;
}

export default function ProductCard({ name, description, price }: ProductCardProps) {
    return (
        <Card shadow="sm" padding="lg" radius="md" withBorder w={300} h={250} style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <Title order={3} mb="xs">{name}</Title>
            <Text size="sm" c="dimmed">
                {description}
            </Text>
            <Text fw={700} size="lg" mt="md">${price.toFixed(2)}</Text>
            <Group mt="md" grow>
                <Button variant="light">Add to Cart</Button>
                <Button>Buy Now</Button>
            </Group>
        </Card>
    )
}