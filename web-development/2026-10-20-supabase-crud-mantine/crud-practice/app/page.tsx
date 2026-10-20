"use client";
import { useState } from "react";
import { Alert, Button, Card, Group, Stack, Text, TextInput, Title, Tour } from "@mantine/core";

export default function MiniInterface() {
  const [active, setActive] = useState(false);
  const [step, setStep] = useState(0);

  return (
    <Stack gap="md" p="md" justify="center" align="center">
      <Title order={2}>Welcome</Title>
      <Button onClick={() => setActive(true)}>Start Tour</Button>

      <Tour active={active} step={step} onStepChange={setStep} onClose={() => setActive(false)}>
        <Tour.Step target="#tour-target-1" title="Step 1">
          This is the navbar where you can navigate to different sections of my task. Use the links to explore various pages and tasks.
        </Tour.Step>
      </Tour>
    </Stack>
  );
}