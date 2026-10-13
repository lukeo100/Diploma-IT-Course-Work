"use client";
const currentShelterRabbits: number = 32;
const vaccinatedShelterRabbits: number = 26;
const money: number = 3984;
const expenses: number = 2473;

const shelterCapacity = (capacity: number, currentRabbits: number) => ({
    percentage: (currentRabbits / capacity),
    count: `${currentRabbits}/${capacity}`
});
const fundraisingRevenue = (money: number, expenses: number) => money - expenses;
const unvaccinatedRabbits = (currentRabbits: number, vaccinatedRabbits: number) => currentRabbits - vaccinatedRabbits;
const avgExpensesPerRabbit = (currentRabbits: number, expenses: number) => expenses / currentRabbits;
const vaccinationRate = (currentRabbits: number, vaccinatedRabbits: number) => vaccinatedRabbits / currentRabbits;

const Task7Page = () => {
    const shelterStats = shelterCapacity(50, currentShelterRabbits);
    const revenue = fundraisingRevenue(money, expenses);
    const unvaccinated = unvaccinatedRabbits(currentShelterRabbits, vaccinatedShelterRabbits);
    const avgExpense = avgExpensesPerRabbit(currentShelterRabbits, expenses);
    const vaccination = vaccinationRate(currentShelterRabbits, vaccinatedShelterRabbits);

    return (
        <div>
            <h1>Rabbit Shelter Overview</h1>
            <p>Shelter capacity: {shelterStats.count}</p>
            <p>Capacity percentage: {(shelterStats.percentage * 100).toFixed(1)}%</p>
            <p>Fundraising revenue: ${revenue}</p>
            <p>Unvaccinated rabbits: {unvaccinated}</p>
            <p>Average expenses per rabbit: ${avgExpense.toFixed(2)}</p>
            <p>Vaccination rate: {(vaccination * 100).toFixed(1)}%</p>
            <p>
                {vaccination >= 0.75
                    ? "Excellent vaccination coverage."
                    : "Vaccination coverage needs attention."}
            </p>
        </div>
    );
};

export default Task7Page;