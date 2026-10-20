"use client";

import { Flex, Stack, Text, Title, TextInput, Button, Card, Checkbox } from '@mantine/core';

export default function SignUpPage() {
    return (
        <Stack gap="md" p="md" justify="center" align="center">
            <Card shadow="sm" p="lg" radius="md" withBorder>
                <Title order={2}>Sign Up</Title>
                <p>Welcome! Please fill out the form below to create an account.</p>

                <Stack gap="sm" mt="md">
                    <Stack gap="xs">
                        <Text size="sm" mb="xs">
                            Full Name
                        </Text>
                        <TextInput
                            placeholder="Enter your full name"
                        />
                    </Stack>
                    <Stack gap="xs">
                        <Text size="sm" mb="xs">
                            Email Address
                        </Text>
                        <TextInput
                            placeholder="Enter your email"
                        />
                    </Stack>
                    <Stack gap="xs">
                        <Text size="sm" mb="xs">
                            Password
                        </Text>
                        <TextInput
                            placeholder="Enter your password"
                            type="password"
                        />
                    </Stack>
                    <Stack gap="xs">
                        <Text size="sm" mb="xs">
                            Confirm Password
                        </Text>
                        <TextInput
                            placeholder="Confirm your password"
                            type="password"
                        />
                    </Stack>

                    <Checkbox
                        label="I agree to the terms and conditions"
                    />
                    <Flex justify="center" mt="md">
                        <Button variant="filled" type="submit">Sign Up</Button>
                    </Flex>
                </Stack>
            </Card>
        </Stack>
    );
}
