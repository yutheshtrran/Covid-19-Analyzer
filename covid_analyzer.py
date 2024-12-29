#GROUP MEMBERS
'''21/ENG/009 A.HARISHAN 
   21/ENG/131 S.YUTHESHTRRAN
   21/ENG/132 S.GEERTHIGA'''
   
   
import random
import matplotlib.pyplot as plt

class Person:
    def __init__(self, age_group):
        self.infected = False
        self.days_infected = 0
        self.age_group = age_group
        self.wears_mask = False
        self.travel_restrictions = False

    def infect(self, transmission_rate):
        if not self.infected and random.uniform(0, 100) < transmission_rate:
            self.infected = True

    def progress_infection(self):
        if self.infected:
            self.days_infected += 1

class Family:
    def __init__(self, size):
        self.members = [Person(age_group=random.choice(["child", "adult", "senior"])) for _ in range(size)]

    def get_infected_members(self):
        return [member for member in self.members if member.infected]

class Community:
    def __init__(self, population_size, num_families, essential_workers):
        self.population = [Family(size=random.randint(2, 7)) for _ in range(num_families)]
        self.essential_workers = random.sample(range(population_size), essential_workers)

    def enforce_mask_wearing(self):
        for family in self.population:
            for person in family.members:
                person.wears_mask = True

    def lift_mask_wearing_enforcement(self):
        for family in self.population:
            for person in family.members:
                person.wears_mask = False

    def enforce_travel_restrictions(self):
        for family in self.population:
            for person in family.members:
                person.travel_restrictions = True

    def lift_travel_restrictions_enforcement(self):
        for family in self.population:
            for person in family.members:
                person.travel_restrictions = False

    def simulate_day(self, wear_masks=False, travel_restrictions=False):
        daily_infected = 0
        for family in self.population:
            for person in family.members:
                if person.infected and person.days_infected >= 11:
                    person.infected = False
                elif person.infected:
                    for family_member in family.members:
                        if not family_member.infected and random.uniform(0, 100) < 0.4:  # Family transmission rate
                            family_member.infected = True
                            daily_infected += 1
                transmission_rate = self.get_transmission_rate(person.age_group)
                if wear_masks and person.wears_mask:
                    transmission_rate *= 0.05  # Reducing transmission rate with masks to 5%
                if travel_restrictions and person.travel_restrictions:
                    transmission_rate *= 0.1  # Reducing transmission rate with travel restrictions to 10%
                person.infect(transmission_rate)

        return daily_infected

    def get_transmission_rate(self, age_group):
        if age_group == "child":
            return random.uniform(10, 20)
        elif age_group == "adult":
            return random.uniform(15, 40)
        elif age_group == "senior":
            return random.uniform(35, 60)

# Set a seed for random number generation
random.seed(42)

# Simulation
community = Community(population_size=100000, num_families=100000, essential_workers=40000)
daily_infected_counts = [1]  # Starting with an initial infected count
total_hospitalized = 0
total_fatalities = 0
total_recovered = 0

for day in range(50):
    print(f"\nDay {day + 1} Simulation:")
    print("1. Enforce Face Mask Wearing")
    print("2. Lift Face Mask Wearing Enforcement")
    print("3. Enforce Travel Restrictions")
    print("4. Lift Travel Restrictions Enforcement")

    # Handle invalid user input
    choice = input("Enter your choice (1-4): ")
    while choice not in ['1', '2', '3', '4']:
        print("Invalid choice. Please enter a correct number (1-4).")
        choice = input("Enter your choice (1-4): ")

    if choice == '1':
        community.enforce_mask_wearing()
    elif choice == '2':
        community.lift_mask_wearing_enforcement()
    elif choice == '3':
        community.enforce_travel_restrictions()
    elif choice == '4':
        community.lift_travel_restrictions_enforcement()

    daily_infected = community.simulate_day(wear_masks=day >= 5, travel_restrictions=day >= 5)
    daily_infected_counts.append(daily_infected)

    if day >= 5:
        total_hospitalized += daily_infected * 9
        total_fatalities += daily_infected * 0.1
        total_recovered += daily_infected * 0.8

    if day % 180 == 0:
        community = Community(population_size=100000, num_families=100000, essential_workers=40000)

# Displaying the results
print("Daily Infected Counts:", daily_infected_counts)
print("Total Hospitalized:", int(total_hospitalized))
print("Total Fatalities:", int(total_fatalities))
print("Total Recovered:", int(total_recovered))

# Plotting charts (if needed)
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(range(1, 52), daily_infected_counts, marker='o') 
plt.title('Daily Infected Counts')
plt.xlabel('Days')
plt.ylabel('Infected Count')

plt.subplot(2, 2, 2)
plt.bar(['Hospitalized', 'Fatalities', 'Recovered'], [total_hospitalized, total_fatalities, total_recovered])
plt.title('Total Hospitalized, Fatalities, and Recovered')
plt.ylabel('Count')

plt.subplot(2, 2, 3)
plt.pie([total_hospitalized, total_fatalities, total_recovered], labels=['Hospitalized', 'Fatalities', 'Recovered'], autopct='%1.1f%%')
plt.title('Percentage of Hospitalized, Fatalities, and Recovered')

plt.tight_layout()
plt.show()
