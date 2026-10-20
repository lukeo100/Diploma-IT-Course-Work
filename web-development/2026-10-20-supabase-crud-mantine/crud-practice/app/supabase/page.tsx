"use client";

import { Badge, Button, Card, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { supabaseTasks, supabaseTaskHref } from "@/app/lib/supabase-tasks";

export default function SupabasePractice() {
    return (
        <Stack gap="md" p="md" align="center">
            <Title order={2}>Supabase Practice</Title>
            <Text c="dimmed" maw={600} ta="center">
                Fifteen exercises covering Create, Read, Update and Delete with the Supabase JavaScript client.
            </Text>
            <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }} spacing="md" maw={1000}>
                {supabaseTasks.map((task) => (
                    <Card key={task.n} shadow="sm" padding="lg" radius="md" withBorder>
                        <Badge mb="xs" variant="light">
                            {task.section}
                        </Badge>
                        <Title order={4} mb="xs">
                            Task {task.n}: {task.title}
                        </Title>
                        <Text size="sm" c="dimmed" mb="md">
                            {task.description}
                        </Text>
                        <Button component="a" href={supabaseTaskHref(task.n)} variant="outline" mt="auto">
                            Open
                        </Button>
                    </Card>
                ))}
            </SimpleGrid>
        </Stack>
    );
}
