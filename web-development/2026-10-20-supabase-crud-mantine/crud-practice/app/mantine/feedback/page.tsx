"use client";

import { Flex, Stack, Text, Title, TextInput, Button, Card, Checkbox } from '@mantine/core';
import { useEditor } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { RichTextEditor } from '@mantine/tiptap';

const content = '<p>Type your feedback here...</p>';

export default function FeedbackPage() {
    const editor = useEditor({
        shouldRerenderOnTransaction: true,
        extensions: [StarterKit],
        content,
    });

    return (
        <Stack gap="md" p="md" justify="center" align="center">
            <Card shadow="sm" p="lg" radius="md" withBorder>
                <Title order={2}>Feedback</Title>
                <p>Welcome! Please fill out the form below to submit your feedback.</p>

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

                    <RichTextEditor editor={editor} variant="subtle">
                        <RichTextEditor.Toolbar sticky stickyOffset="var(--docs-header-height)">
                            <RichTextEditor.ControlsGroup>
                                <RichTextEditor.Bold />
                                <RichTextEditor.Italic />
                                <RichTextEditor.Underline />
                                <RichTextEditor.Strikethrough />
                                <RichTextEditor.ClearFormatting />
                                <RichTextEditor.Highlight />
                                <RichTextEditor.Code />
                            </RichTextEditor.ControlsGroup>
                        </RichTextEditor.Toolbar>

                        <RichTextEditor.Content />
                    </RichTextEditor>

                    <Checkbox
                        label="I agree to the terms and conditions"
                    />
                    <Flex justify="center" mt="md">
                        <Button variant="filled" type="submit">Submit Feedback</Button>
                    </Flex>
                </Stack>
            </Card>
        </Stack>
    );
}
