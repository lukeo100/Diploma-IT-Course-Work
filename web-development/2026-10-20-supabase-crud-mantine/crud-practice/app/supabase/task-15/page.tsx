"use client";

// Task 15 (Your own table)
// 1. Create your own table in Supabase with RLS off and at least three
//    columns besides id: one text, one int4 and one bool.
// 2. Add a type for it to app/lib/supabase.ts.
// 3. Build all four operations here: list, add, change, delete.
// Expected: every operation still shows its change after a refresh.
import { useEffect, useState } from "react";
import { supabase, Shelter } from "@/app/lib/supabase";
import { Flex, Card, Text, Button, Input, Checkbox } from "@mantine/core";

const Task15 = () => {
    const [shelters, setShelters] = useState<Shelter[]>([]);
    const loadShelters = async () => {
        const { data, error } = await supabase.from("shelters").select("*").order("shelter_name");

        if (error) {
            alert(error.message);
            return;
        } else {
            setShelters(data);
        }
    };

    const addShelter = async (shelterName: string, capacity: number, currentAnimals: number, address: string, animalTypes: string[]) => {
        if (!shelterName || !capacity || !currentAnimals || !address || animalTypes.length === 0) {
            alert("Please provide all fields.");
            return;
        }

        const { data, error } = await supabase.from("shelters").insert({ shelter_name: shelterName, capacity, current_animals: currentAnimals, address, animal_types: animalTypes });
        if (error) {
            alert(error.message);
            return;
        } else {
            loadShelters();
        }
    };

    const updateShelter = async (shelterId: number, updatedFields: Partial<Shelter>) => {
        const { data, error } = await supabase.from("shelters").update(updatedFields).eq("id", shelterId);
        if (error) {
            alert(error.message);
            return;
        } else {
            loadShelters();
        }
    };

    const deleteShelter = async (shelterId: number) => {
        const { data, error } = await supabase.from("shelters").delete().eq("id", shelterId);
        if (error) {
            alert(error.message);
            return;
        } else {
            loadShelters();
        }
    };

    useEffect(() => {
        // TODO: load the shelters
        loadShelters();
    }, []);

    return (
        <main>
            <h1>Animal Shelters</h1>
            {/* TODO */}
            <Flex direction="column" gap="md">
                {shelters.map((shelter) => (
                    <Card key={shelter.id} shadow="sm" padding="lg" radius="md" withBorder>
                        <Text fw={500} size="lg" mt="md">
                            {shelter.shelter_name}
                        </Text>
                        <Text size="sm" color="dimmed">
                            Capacity: {shelter.capacity}, Current Animals: {shelter.current_animals}
                        </Text>
                        <Text size="sm" color="dimmed">
                            Address: {shelter.address}
                        </Text>
                        <Text size="sm" color="dimmed">
                            Animal Types: {shelter.animal_types}
                        </Text>
                        <Button color="blue" mt="md" onClick={async () => {
                            const newCapacity = prompt("Enter new capacity:", shelter.capacity.toString());
                            if (newCapacity) {
                                updateShelter(shelter.id, { capacity: parseInt(newCapacity) });
                            }
                        }}>
                            Update Capacity
                        </Button>
                        <Button color="red" mt="md" onClick={async () => {
                            deleteShelter(shelter.id);
                        }}>
                            Delete
                        </Button>
                    </Card>
                ))}

                <Card shadow="sm" padding="lg" radius="md" withBorder>
                    <Input id="shelterName" placeholder="Shelter Name" />
                    <Input id="capacity" placeholder="Capacity" type="number" mt="sm" />
                    <Input id="currentAnimals" placeholder="Current Animals" type="number" mt="sm" />
                    <Input id="address" placeholder="Address" type="text" mt="sm" />
                    <ul>
                        <Text fw={500} size="md" mt="md">
                            Animal Types (check all that apply):
                        </Text>
                        <Checkbox id="rabbitAnimalType" label="Rabbit" />
                        <Checkbox id="catAnimalType" label="Cat" />
                        <Checkbox id="dogAnimalType" label="Dog" />
                    </ul>
                    <Button color="green" mt="md" onClick={() => {
                        const getValue = (id: string) => (document.getElementById(id) as HTMLInputElement | null)?.value ?? "";
                        const isChecked = (id: string) => (document.getElementById(id) as HTMLInputElement | null)?.checked ?? false;
                        const animalTypes: string[] = [];
                        if (isChecked("rabbitAnimalType")) animalTypes.push("Rabbit");
                        if (isChecked("catAnimalType")) animalTypes.push("Cat");
                        if (isChecked("dogAnimalType")) animalTypes.push("Dog");
                        addShelter(
                            getValue("shelterName"),
                            Number(getValue("capacity")),
                            Number(getValue("currentAnimals")),
                            getValue("address"),
                            animalTypes
                        );
                    }}>
                        Add Shelter
                    </Button>
                </Card>

            </Flex>
        </main>
    );
};

export default Task15;
