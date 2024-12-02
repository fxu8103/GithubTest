import random
import json
import os

class ResourceManager:
    def __init__(self, food, wood, water, goal_resources, population):
        self.food = food
        self.wood = wood
        self.water = water
        self.settlement_size = 1  # Determines monthly upkeep
        self.current_month = 1  # Tracks the current month
        self.goal_resources = goal_resources  # Goal to reach to win the game
        self.max_months = 120  # 10 years (120 months)
        self.population = population  # Total population available for work
        self.workforce = {"food": 0, "wood": 0, "water": 0}  # Workforce allocation

    def allocate_workforce(self):
        print("\n👷 Workforce Allocation:")
        print(f"Total Population: {self.population}")
        while True:
            try:
                food_workers = int(input("Enter number of workers for food collection: "))
                wood_workers = int(input("Enter number of workers for wood collection: "))
                water_workers = int(input("Enter number of workers for water collection: "))
                if food_workers + wood_workers + water_workers > self.population:
                    print("❌ Total workers assigned exceeds population. Try again.")
                else:
                    self.workforce["food"] = food_workers
                    self.workforce["wood"] = wood_workers
                    self.workforce["water"] = water_workers
                    print(f"\n👷 Workforce allocated: Food: {food_workers}, Wood: {wood_workers}, Water: {water_workers}")
                    break
            except ValueError:
                print("❌ Invalid input. Please enter numbers only.")

    def collect_resources_automatically(self):
        # Collect resources based on workforce allocation
        food_collected = self.workforce["food"] * random.randint(5, 15)
        wood_collected = self.workforce["wood"] * random.randint(3, 10)
        water_collected = self.workforce["water"] * random.randint(4, 12)
        self.food += food_collected
        self.wood += wood_collected
        self.water += water_collected
        print(f"\n🛠️ Resources automatically collected!")
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
            self.population += 10  # Population increases with settlement size
            print(f"\n🏗️ Settlement expanded! New size: {self.settlement_size}")
            print(f"Resources used: Food: -{expansion_cost}, Wood: -{expansion_cost}, Water: -{expansion_cost}")
            print(f"Population increased to: {self.population}")
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

    def apply_disaster_damage(self):
        damage_percentage = random.uniform(0.01, 0.30)  # Random damage between 1% and 30%
        self.food -= int(self.food * damage_percentage)
        self.wood -= int(self.wood * damage_percentage)
        self.water -= int(self.water * damage_percentage)
        print(f"\n⚠️ Natural Disaster! Resources reduced by {damage_percentage * 100:.2f}%:")
        print(f"Food left: {self.food}, Wood left: {self.wood}, Water left: {self.water}")

    def check_goal(self):
        # Check if the player has met the goal
        if self.food >= self.goal_resources and self.wood >= self.goal_resources and self.water >= self.goal_resources:
            print(f"\n🎉 Congratulations! You reached your goal of {self.goal_resources} resources and won the game!")
            return True
        return False


class Leaderboard:
    def __init__(self, file_path="leaderboard.json"):
        self.file_path = file_path
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []

    def save_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10
        with open(self.file_path, "w") as file:
            json.dump(self.scores, file)

    def display(self):
        print("\n🏆 Leaderboard:")
        for rank, entry in enumerate(self.scores, start=1):
            print(f"{rank}. {entry['name']} - {entry['score']}")

def main():
    # Initialize resources and goal
    initial_food = 300
    initial_wood = 200
    initial_water = 250
    goal_resources = 1000  # Goal to reach
    initial_population = 10  # Starting population
    resource_manager = ResourceManager(initial_food, initial_wood, initial_water, goal_resources, initial_population)
    leaderboard = Leaderboard()

    # Main game loop
    while True:
        print("\n🌟 Resources Management Game 🌟")
        print(f"Settlement Size: {resource_manager.settlement_size}, Month: {resource_manager.current_month}")
        print(f"Population: {resource_manager.population}")
        print(f"Food: {resource_manager.food}, Wood: {resource_manager.wood}, Water: {resource_manager.water}")
        print(f"Goal: {goal_resources} of each resource")
        
        # Allocate workforce at the start of each month
        resource_manager.allocate_workforce()
        
        # Collect resources automatically
        resource_manager.collect_resources_automatically()
        
        # Perform monthly upkeep automatically
        if not resource_manager.monthly_upkeep():
            break  # End the game if upkeep fails

        # Check for random disaster
        resource_manager.check_random_disaster()

        # Check if goal is achieved
        if resource_manager.check_goal():
            break

        # Advance to the next month
        resource_manager.advance_month()

        # Check if max months reached
        if resource_manager.current_month > resource_manager.max_months:
            print("\n⏳ Time's up! You did not reach the goal. Game Over!")
            break

    # End game and save score
    total_resources = resource_manager.food + resource_manager.wood + resource_manager.water
    print(f"\nGame Over! Total Resources Collected: {total_resources}")
    player_name = input("Enter your name for the leaderboard: ")
    leaderboard.save_score(player_name, total_resources)
    leaderboard.display()

if __name__ == "__main__":
    main()
