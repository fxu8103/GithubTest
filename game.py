import random
import json
import os

class ResourceManager:
    def __init__(self, food, wood, water, goal_resources, population):
        self.food = food
        self.wood = wood
        self.water = water
        self.settlement_size = 1
        self.current_month = 1
        self.goal_resources = goal_resources
        self.max_months = 120
        self.population = population
        self.workforce = {"food": 0, "wood": 0, "water": 0}
        self.points = 0
        self.morality = 50

    def display_resources(self):
        print(f"\n📊 Current Resources:")
        print(f"Food: {self.food}, Wood: {self.wood}, Water: {self.water}")
        print(f"Population: {self.population}, Morality: {self.morality}, Points: {self.points}")

    def allocate_workforce(self):
        """Allow the user to assign workforce."""
        print("\nAssign workforce to gather resources:")
        max_workers = self.population
        while True:
            try:
                food_workers = int(input(f"How many workers for food (max {max_workers})? "))
                wood_workers = int(input(f"How many workers for wood (max {max_workers - food_workers})? "))
                water_workers = max_workers - food_workers - wood_workers

                if food_workers + wood_workers > max_workers or food_workers < 0 or wood_workers < 0:
                    raise ValueError("Invalid workforce allocation.")
                self.workforce = {"food": food_workers, "wood": wood_workers, "water": water_workers}
                print(f"\nWorkforce allocated: Food: {food_workers}, Wood: {wood_workers}, Water: {water_workers}")
                break
            except ValueError as e:
                print(f"❌ Error: {e}. Please try again.")

    def collect_resources(self):
        """Gather resources based on workforce."""
        food_collected = self.workforce["food"] * random.randint(5, 15)
        wood_collected = self.workforce["wood"] * random.randint(3, 10)
        water_collected = self.workforce["water"] * random.randint(4, 12)

        self.food += food_collected
        self.wood += wood_collected
        self.water += water_collected
        print(f"\n🛠️ Resources collected! Food: +{food_collected}, Wood: +{wood_collected}, Water: +{water_collected}")

    def expand_settlement(self):
        """Expand the settlement if resources allow."""
        cost = 200 * self.settlement_size
        if self.food >= cost and self.wood >= cost:
            self.food -= cost
            self.wood -= cost
            self.settlement_size += 1
            new_population = self.settlement_size * 5  # Example rule: 5 new people per settlement size increase
            self.population += new_population
            print(f"🎉 Settlement expanded! New size: {self.settlement_size}, Population increased by {new_population}!")
        else:
            print(f"❌ Not enough resources to expand. Cost: {cost} Food & Wood.")

    def monthly_upkeep(self):
        """Calculate monthly resource consumption."""
        food_required = self.settlement_size * 30
        wood_required = self.settlement_size * 20
        water_required = self.settlement_size * 25

        print(f"\n📆 Month {self.current_month}: Monthly upkeep due.")
        if self.food < food_required or self.wood < wood_required or self.water < water_required:
            print("❌ Not enough resources for monthly upkeep. Game Over!")
            print(f"Food needed: {food_required}, Wood needed: {wood_required}, Water needed: {water_required}")
            return False

        self.food -= food_required
        self.wood -= wood_required
        self.water -= water_required
        print(f"✅ Monthly upkeep met. Resources used:")
        print(f"Food: -{food_required}, Wood: -{wood_required}, Water: -{water_required}")
        return True

    def check_random_disaster(self):
        """Random chance of a natural disaster."""
        if random.random() <= 0.2:  # 20% chance
            print("\n🔥 A random natural disaster has occurred!")
            self.apply_disaster_damage()

    def apply_disaster_damage(self):
        """Apply random disaster damage."""
        damage_percentage = random.uniform(0.01, 0.30)
        self.food -= int(self.food * damage_percentage)
        self.wood -= int(self.wood * damage_percentage)
        self.water -= int(self.water * damage_percentage)
        self.morality -= 5
        print(f"⚠️ Disaster! Resources reduced by {damage_percentage * 100:.2f}%.")
        print(f"Remaining: Food: {self.food}, Wood: {self.wood}, Water: {self.water}")
        print(f"Morality reduced to {self.morality}")

    def check_and_award_points(self):
        """Award points for reaching resource and moral goals."""
        if self.food >= self.goal_resources:
            self.points += 100
            self.food -= self.goal_resources
            print("🎉 Food goal met! Earned 100 points.")
        if self.wood >= self.goal_resources:
            self.points += 100
            self.wood -= self.goal_resources
            print("🎉 Wood goal met! Earned 100 points.")
        if self.water >= self.goal_resources:
            self.points += 100
            self.water -= self.goal_resources
            print("🎉 Water goal met! Earned 100 points.")
        if self.morality >= 80:
            self.points += 200
            print("🌟 High morality! Earned 200 points.")
        elif self.morality < 20:
            print("⚠️ Low morality is affecting the settlement.")
    def advance_month(self):
        """Advance to the next month."""
        self.current_month += 1
        print(f"\n📅 Advancing to Month {self.current_month}.")
class EthicalTradeManager:
    def __init__(self):
        self.ethical_dilemmas = [
            {
                "question": "A neighboring settlement is starving. Do you donate 100 food to help them, or prioritize your own people?",
                "choices": {
                    "Donate food": {"morality": 20, "points": 50, "resources": {"food": -100}},
                    "Keep food": {"morality": -10, "points": 100}
                }
            },
            {
                "question": "A wealthy merchant offers to pay you 200 points for 150 water. Do you accept the trade or refuse?",
                "choices": {
                    "Accept trade": {"morality": 10, "points": 200, "resources": {"water": -150}},
                    "Refuse trade": {"morality": 5, "points": 0}
                }
            },
            {
                "question": "You discover illegal logging in your forests. Do you crack down on it or let it continue for extra wood?",
                "choices": {
                    "Stop the logging": {"morality": 30, "points": 0},
                    "Allow logging": {"morality": -30, "points": 150, "resources": {"wood": 100}}
                }
            },
            {
                "question": "A trader offers to exchange 200 wood for 100 food. Do you take the trade or decline?",
                "choices": {
                    "Take trade": {"morality": 10, "resources": {"wood": 200, "food": -100}},
                    "Decline trade": {"morality": 5, "points": 0}
                }
            },
            {
                "question": "A group of rebels demands 300 wood and 200 food in exchange for peace. Do you comply or risk fighting?",
                "choices": {
                    "Comply": {"morality": -10, "resources": {"wood": -300, "food": -200}},
                    "Fight": {"morality": 20, "points": 100}
                }
            }
        ]

    def present_ethics_dilemma(self, resource_manager):
        """Randomly present an ethical dilemma to the player."""
        dilemma = random.choice(self.ethical_dilemmas)
        print(f"\n🤔 Ethical Dilemma: {dilemma['question']}")
        
        options = list(dilemma["choices"].keys())
        print("Choices:")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        while True:
            try:
                choice_idx = int(input("Choose your option (1/2): ")) - 1
                if choice_idx < 0 or choice_idx >= len(options):
                    raise ValueError("Invalid choice. Please select a valid option.")
                
                choice_key = options[choice_idx]
                effects = dilemma["choices"][choice_key]

                # Apply effects
                resource_manager.morality += effects.get("morality", 0)
                resource_manager.points += effects.get("points", 0)
                for resource, change in effects.get("resources", {}).items():
                    setattr(resource_manager, resource, max(0, getattr(resource_manager, resource) + change))
                
                print(f"\n✅ You chose: {choice_key}")
                for key, value in effects.items():
                    if key == "resources":
                        for res, amount in value.items():
                            print(f"  {res.capitalize()}: {amount:+}")
                    else:
                        print(f"  {key.capitalize()}: {value:+}")
                break
            except (ValueError, IndexError):
                print("❌ Invalid input. Please try again.")



class TradeManager:
    def __init__(self):
        self.trade_offers = [
            {"offer": {"food": 200}, "request": {"wood": 150}},
            {"offer": {"water": 300}, "request": {"food": 250}},
            {"offer": {"points": 100}, "request": {"water": 100}},
            {"offer": {"wood": 400}, "request": {"points": 200}}
        ]

    def present_trade_offer(self, resource_manager):
        """Randomly present a trade opportunity to the player."""
        trade = random.choice(self.trade_offers)
        print("\n💱 Trade Opportunity!")
        print(f"A trader offers: {trade['offer']}")
        print(f"In exchange for: {trade['request']}")
        choice = input("Do you accept this trade? (yes/no): ").strip().lower()

        if choice == "yes":
            if all(getattr(resource_manager, key, 0) >= val for key, val in trade["request"].items()):
                for key, val in trade["request"].items():
                    setattr(resource_manager, key, getattr(resource_manager, key) - val)
                for key, val in trade["offer"].items():
                    setattr(resource_manager, key, getattr(resource_manager, key) + val)
                print("✅ Trade successful!")
            else:
                print("❌ You don't have enough resources to complete the trade.")
        elif choice == "no":
            print("Trade declined.")
        else:
            print("❌ Invalid choice. No trade made.")

class SettlementGame:
    def __init__(self):
        self.player_name = input("\n🌟 Enter your name: ").strip() or "Anonymous"
        self.manager = ResourceManager(food=100, wood=100, water=100, goal_resources=500, population=10)
        self.ethical_manager = EthicalTradeManager()
        self.dilemma_probability = 0.3  # 30% chance of encountering a dilemma each month

    def game_loop(self):
        """Main game loop."""
        while self.manager.current_month <= self.manager.max_months:
            self.manager.display_resources()
            self.manager.allocate_workforce()
            self.manager.collect_resources()

            if not self.manager.monthly_upkeep():
                print("\nGame Over! Settlement failed.")
                break

            self.manager.check_random_disaster()
            self.manager.check_and_award_points()

            # Check for ethical dilemmas (random encounter)
            if random.random() < self.dilemma_probability:
                self.ethical_manager.present_ethics_dilemma(self.manager)

            # Choose next action
            action = input("\nWould you like to (1) Expand settlement, or (2) Skip to next month? ")
            if action == "1":
                self.manager.expand_settlement()

            # Advance to the next month
            self.manager.advance_month()

        print("\n🎉 Game Complete! Total Points:", self.manager.points)
        self.save_leaderboard()

    def save_leaderboard(self):
        """Save the high scores to a file."""
        filename = "leaderboard.json"
        # Load existing leaderboard or create a new one
        if os.path.exists(filename):
            with open(filename, "r") as file:
                leaderboard = json.load(file)
        else:
            leaderboard = []

        # Append the current game score to the leaderboard
        leaderboard.append({
            "name": self.player_name,
            "points": self.manager.points,
            "month": self.manager.current_month - 1
        })
        leaderboard = sorted(leaderboard, key=lambda x: x["points"], reverse=True)[:10]

        # Save the leaderboard back to the file
        with open(filename, "w") as file:
            json.dump(leaderboard, file)

        # Print the leaderboard
        print("\n🏆 High Scores:")
        for idx, entry in enumerate(leaderboard, 1):
            print(f"{idx}. {entry['name']} - Points: {entry['points']} - Month: {entry['month']}")

    def start(self):
        """Start the game."""
        print("\n🌟 Welcome to Settlement Game!")
        self.game_loop()

if __name__ == "__main__":
    game = SettlementGame()
    game.start()
