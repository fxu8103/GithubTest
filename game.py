import random

class ResourceManager:
    def __init__(self, food, wood, water):
        self.food = food
        self.wood = wood
        self.water = water
        self.settlement_size = 1  # Determines monthly upkeep
        self.current_month = 1  # Tracks the current month

    def apply_disaster_damage(self):
        damage_percentage = random.uniform(0.01, 0.30)  # Random damage between 1% and 30%
        self.food -= int(self.food * damage_percentage)
        self.wood -= int(self.wood * damage_percentage)
        self.water -= int(self.water * damage_percentage)
        print(f"\n⚠️ Natural Disaster! Resources reduced by {damage_percentage * 100:.2f}%:")
        print(f"Food left: {self.food}, Wood left: {self.wood}, Water left: {self.water}")

    def collect_resources(self):
        # Randomly gather resources
        food_collected = random.randint(10, 50)
        wood_collected = random.randint(5, 30)
        water_collected = random.randint(10, 40)
        self.food += food_collected
        self.wood += wood_collected
        self.water += water_collected
        print(f"\n🛠️ Resources collected!")
        print(f"Food: +{food_collected}, Wood: +{wood_collected}, Water: +{water_collected}")

    def monthly_upkeep(self):
        # Consume resources based on settlement size
        food_required = self.settlement_size * 30  # Monthly upkeep scales with size
        wood_required = self.settlement_size * 20
        water_required = self.settlement_size * 25

        print(f"\n📆 Month {self.current_month}: Monthly upkeep due.")
        if self.food < food_required or self.wood < wood_required or self.water < water_required:
            print("❌ Not enough resources for monthly upkeep. Game Over!")
            print(f"Food needed: {food_required}, Wood needed: {wood_required}, Water needed: {water_required}")
            return False  # Game over

        self.food -= food_required
        self.wood -= wood_required
        self.water -= water_required
        print(f"✅ Monthly upkeep met. Resources used:")
        print(f"Food: -{food_required}, Wood: -{wood_required}, Water: -{water_required}")
        return True  # Game continues

    def expand_settlement(self):
        # Cost to expand settlement
        expansion_cost = 100  # Same cost for all resources for simplicity
        if self.food >= expansion_cost and self.wood >= expansion_cost and self.water >= expansion_cost:
            self.food -= expansion_cost
            self.wood -= expansion_cost
            self.water -= expansion_cost
            self.settlement_size += 1
            print(f"\n🏗️ Settlement expanded! New size: {self.settlement_size}")
            print(f"Resources used: Food: -{expansion_cost}, Wood: -{expansion_cost}, Water: -{expansion_cost}")
        else:
            print("\n⚠️ Not enough resources to expand the settlement!")

    def advance_month(self):
        # Advance to the next month
        self.current_month += 1
        print(f"\n📅 Advancing to Month {self.current_month}.")

    def check_random_disaster(self):
        # 20% chance of a disaster occurring
        if random.random() <= 0.2:
            print("\n🔥 A random natural disaster has occurred!")
            self.apply_disaster_damage()


def main():
    # Initialize resources
    initial_food = 300
    initial_wood = 200
    initial_water = 250
    resource_manager = ResourceManager(initial_food, initial_wood, initial_water)

    # Main game loop
    while True:
        print("\n🌟 Resources Management Game 🌟")
        print(f"Settlement Size: {resource_manager.settlement_size}, Month: {resource_manager.current_month}")
        print(f"Food: {resource_manager.food}, Wood: {resource_manager.wood}, Water: {resource_manager.water}")
        print("\nOptions:")
        print("1. Collect resources")
        print("2. Expand settlement")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            resource_manager.collect_resources()
        elif choice == "2":
            resource_manager.expand_settlement()
        elif choice == "3":
            print("\nExiting game. Thanks for playing!")
            break
        else:
            print("\n⚠️ Invalid choice. Please try again.")

        # Perform monthly upkeep automatically
        if not resource_manager.monthly_upkeep():
            break  # End the game if upkeep fails

        # Check for random natural disaster
        resource_manager.check_random_disaster()

        # Advance to the next month
        resource_manager.advance_month()


if __name__ == "__main__":
    main()
