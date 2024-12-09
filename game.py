import random
import json
import os

class ResourceManager:
    def __init__(self, food, wood, water, goal_resources, population, disaster_chance):
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
        self.disaster_chance = disaster_chance
        self.seasons = [
            {"name": "Spring", "months": [3, 4, 5], "food_multiplier": 1.2, "wood_multiplier": 1.1, "water_multiplier": 1.3},
            {"name": "Summer", "months": [6, 7, 8], "food_multiplier": 1.5, "wood_multiplier": 1.0, "water_multiplier": 0.9},
            {"name": "Autumn", "months": [9, 10, 11], "food_multiplier": 1.3, "wood_multiplier": 1.2, "water_multiplier": 1.1},
            {"name": "Winter", "months": [12, 1, 2], "food_multiplier": 0.7, "wood_multiplier": 1.0, "water_multiplier": 0.8},
        ]
    def get_current_season(self):
        for season in self.seasons:
            if self.current_month % 12 in season["months"]:
                return season
        return None


    def display_resources(self):
        print(f"\n📊 Current Status:")
        print(f"Food: {self.food}, Wood: {self.wood}, Water: {self.water}")
        print(f"Population: {self.population}, Morality: {self.morality}, Points: {self.points}")
        print(f"Settlement Size: {self.settlement_size}")

    def allocate_workforce(self):
        print("\nAssign workforce to gather resources:")
        max_workers = self.population  # Total workers available
        while True:
            try:
            # Prompt user for workforce allocation
                food_workers = int(input(f"How many workers for food (max {max_workers})? "))
                if food_workers < 0 or food_workers > max_workers:
                    raise ValueError(f"Invalid number of workers for food (must be between 0 and {max_workers}).")
            
                wood_workers = int(input(f"How many workers for wood (max {max_workers - food_workers})? "))
                if wood_workers < 0 or food_workers + wood_workers > max_workers:
                    raise ValueError(f"Invalid number of workers for wood (must be between 0 and {max_workers - food_workers}).")
            
                water_workers = max_workers - food_workers - wood_workers
                if water_workers < 0:
                    raise ValueError("Workforce allocation exceeds available workers.")

            # Set workforce allocation
                self.workforce = {"food": food_workers, "wood": wood_workers, "water": water_workers}
                print(f"\nWorkforce allocated: Food: {food_workers}, Wood: {wood_workers}, Water: {water_workers}")
                break
            except ValueError as e:
                print(f"❌ Error: {e}. Please try again.")


    def collect_resources(self):
        """Gather resources based on workforce and seasonal effects."""
        season = self.get_current_season()
        food_multiplier = season["food_multiplier"]
        wood_multiplier = season["wood_multiplier"]
        water_multiplier = season["water_multiplier"]

        food_collected = int(self.workforce["food"] * random.randint(5, 15) * food_multiplier)
        wood_collected = int(self.workforce["wood"] * random.randint(5, 15) * wood_multiplier)
        water_collected = int(self.workforce["water"] * random.randint(5, 15) * water_multiplier)

        self.food += food_collected
        self.wood += wood_collected
        self.water += water_collected
        print(f"\n🛠️ Resources collected during {season['name']}! Food: +{food_collected}, Wood: +{wood_collected}, Water: +{water_collected}")

    def expand_settlement(self):
        base_cost = 50  # Base cost for food and wood
        scaling_factor = 1.5  # Increase cost with settlement size

        # Calculate the total cost
        food_cost = int(base_cost * (self.settlement_size ** scaling_factor))
        wood_cost = int(base_cost * (self.settlement_size ** scaling_factor))
        
        if self.food >= food_cost and self.wood >= wood_cost:
            self.food -= food_cost
            self.wood -= wood_cost
            self.settlement_size += 1

            # Population increase upon expansion
            new_population = 5 + self.settlement_size * 2  # Larger settlements yield more population
            self.population += new_population

            print(f"🎉 Settlement expanded to size {self.settlement_size}!")
            print(f"👨‍👩‍👧 Population increased by {new_population}. Total: {self.population}")
            print(f"✨ Bonus Morality: +5")
            self.morality += 25  # Morality bonus for successful expansion
        else:
            print(f"❌ Not enough resources to expand. You need:")
            print(f"   Food: {food_cost}, Wood: {wood_cost}")
    def display_resources(self):
        """Display all resources, population, and status."""
        season = self.get_current_season()
        print(f"\n📊 Current Status - Month {self.current_month} ({season['name']}):")
        print(f"Food: {self.food}, Wood: {self.wood}, Water: {self.water}")
        print(f"Population: {self.population}, Morality: {self.morality}, Points: {self.points}")
        print(f"Settlement Size: {self.settlement_size}")
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
        disaster_roll = random.random()
        if disaster_roll <= self.disaster_chance:
            disaster_type = random.choice(["Heatwave", "Tsunami", "Volcanic Eruption", "Thunderstorm"])
            print(f"\n🔥 A {disaster_type} has occurred!")
            self.apply_disaster_damage(disaster_type)

    def apply_disaster_damage(self, disaster_type):
        """Apply random disaster damage."""
        if disaster_type == "Heatwave":
            damage_percentage = random.uniform(0.25, 0.40)
            self.water -= int(self.water * damage_percentage)
            self.morality -= 5
            print(f"⚠️ Heatwave! Everyone is FEINING for water! Water reduced by {damage_percentage * 100:.2f}%.")
           
        elif disaster_type == "Tsunami":
            damage_percentage = random.uniform(0.20, 0.50)
            self.food -= int(self.food * damage_percentage)
            self.wood -= int(self.wood * damage_percentage)
            self.morality -= 10
            print(f"⚠️ Tsunami! Super Unlucky and Deadly! Food and Wood reduced by {damage_percentage * 100:.2f}%.")
           
        elif disaster_type == "Volcanic Eruption":
            damage_percentage = random.uniform(0.15, 0.25)
            self.food -= int(self.food * damage_percentage)
            self.wood -= int(self.wood * damage_percentage)
            self.water -= int(self.water * damage_percentage)
            self.morality -= 12
            print(f"⚠️ Volcanic Eruption! Everyone is shivering in their boots due to this catastrophic event!! Resources reduced by {damage_percentage * 100:.2f}%.")
           
        elif disaster_type == "Thunderstorm":
            damage_percentage = random.uniform(0.05, 0.15)
            self.wood -= int(self.wood * damage_percentage)
            self.water -= int(self.water * damage_percentage)
            self.morality -= 3
            print(f"⚠️ Thunderstorm! Some Resources may be destroyed and children are scared! Resources reduced by {damage_percentage * 100:.2f}%.")
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
    def apply_morality_penalty(self):
        """Apply penalties when morality drops below 0."""
        print("⚠️ Morality has dropped below 0! Chaos spreads in the settlement.")
    
        # Resource penalty
        food_penalty = int(self.food * 0.25)  # Lose 25% of food
        wood_penalty = int(self.wood * 0.25)  # Lose 25% of wood
        water_penalty = int(self.water * 0.25)  # Lose 25% of water

        self.food = max(0, self.food - food_penalty)
        self.wood = max(0, self.wood - wood_penalty)
        self.water = max(0, self.water - water_penalty)

        print(f"🛑 Penalty: Lost {food_penalty} food, {wood_penalty} wood, and {water_penalty} water.")

        # Population penalty
        if self.population > 1:
            self.population -= 1
            print("👥 A member of the settlement has abandoned you! Population reduced by 1.")

        # Points penalty
        points_penalty = int(100 * self.multiplier)
        self.points = max(0, self.points - points_penalty)
        print(f"📉 Points penalty: Lost {points_penalty} points.")

        # Reset morality to 0
        self.morality = 0
        print("🔄 Morality has been reset to 0.")
  

class EthicalTradeManager:
    def __init__(self):
        self.ethical_dilemmas = [
            {
                "question": "A neighboring settlement is starving. Do you donate 20 food to help them, or prioritize your own people?",
                "choices": {
                    "Donate food": {"morality": 20, "points": 50, "resources": {"food": -20}},
                    "Keep food": {"morality": -10, "points": 75}
                }
            },
            {
                "question": "A wealthy merchant offers to pay you 50 points for 25 water. Do you accept the trade or refuse?",
                "choices": {
                    "Accept trade": {"morality": 10, "points": 50, "resources": {"water": -25}},
                    "Refuse trade": {"morality": 5, "points": 0}
                }
            },
            {
                "question": "You discover illegal logging in your forests. Do you crack down on it or let it continue for extra wood?",
                "choices": {
                    "Stop the logging": {"morality": 30, "points": 75},
                    "Allow logging": {"morality": -30, "points": 50, "resources": {"wood": 50}}
                }
            },
            {
                "question": "A trader offers to exchange 25 wood for 15 food. Do you take the trade or decline?",
                "choices": {
                    "Take trade": {"morality": 10, "resources": {"wood": 25, "food": -15}},
                    "Decline trade": {"morality": 5, "points": 0}
                }
            },
            {
                "question": "A group of rebels demands 15 wood and 20 food in exchange for peace. Do you comply or risk fighting?",
                "choices": {
                    "Comply": {"morality": -10, "resources": {"wood": -15, "food": -20}},
                    "Fight": {"morality": 20, "points": -25, "population": -1}
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
            {"offer": {"food": 30}, "request": {"wood": 15}},
            {"offer": {"water": 30}, "request": {"food": 15}},
            {"offer": {"points": 30}, "request": {"water": 15}},
            {"offer": {"wood": 30}, "request": {"points": 15}}
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
    

class LoopGame:
    def __init__(self):
        self.player_name = input("\n🌟 Enter your name: ").strip() or "Anonymous"
        self.difficulty = self.choose_difficulty()
        self.manager = ResourceManager(
            food=self.difficulty["food"],
            wood=self.difficulty["wood"],
            water=self.difficulty["water"],
            goal_resources=self.difficulty["goal_resources"],
            population=self.difficulty["population"],
            disaster_chance=self.difficulty["disaster_chance"]
        )
       
        self.ethical_manager = EthicalTradeManager()
        self.dilemma_probability = 0.45  # 30% chance of encountering a dilemma each month

    def choose_difficulty(self):
        print("\nChoose your game mode:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Nightmare")

        while True:
            try:
                choice = int(input("\nSelect a difficulty (1-4): "))
                if choice == 1:
                    self.display_land_description("Easy")
                    return {
                        "food": 150,
                        "wood": 150,
                        "water": 150,
                        "goal_resources": 350,
                        "population": 15,
                        "disaster_chance": 0.10,
                        "multiplier": 1.0
                    }
                elif choice == 2:
                    self.display_land_description("Medium")
                    return {
                        "food": 125,
                        "wood": 125,
                        "water": 125,
                        "goal_resources": 500,
                        "population": 12,
                        "disaster_chance": 0.15,
                        "multiplier": 1.5
                    }
                elif choice == 3:
                    self.display_land_description("Hard")
                    return {
                        "food": 100,
                        "wood": 100,
                        "water": 100,
                        "goal_resources": 700,
                        "population": 10,
                        "disaster_chance": 0.22,
                        "multiplier": 2.0
                    }
                elif choice == 4:
                    self.display_land_description("Nightmare")
                    return {
                        "food": 75,
                        "wood": 75,
                        "water": 75,
                        "goal_resources": 850,
                        "population": 9,
                        "disaster_chance": 0.30,
                        "multiplier": 3.0
                    }
                else:
                    raise ValueError("Invalid choice. Please select a number between 1 and 4.")
            except ValueError as e:
                print(f"❌ Error: {e}. Please try again.")

    def display_land_description(self, difficulty):
        """Display a description of the player's land based on the difficulty level."""
        descriptions = {
            "Easy": (
                "You have settled on a fertile piece of land with abundant natural resources. "
                "The soil is rich, forests are plentiful, and nearby water sources are easily accessible. "
                "Your settlement will thrive with ease, and you have room to expand rapidly."
            ),
            "Medium": (
                "Your settlement is on moderately fertile land. Resources are balanced, but you will need to manage them wisely. "
                "The terrain has some challenges, with fewer forests and a distant water source, but your settlement can grow with effort."
            ),
            "Hard": (
                "The land you occupy is harsh and unforgiving. Resources are scarce, and you will struggle to gather enough food, wood, and water. "
                "The terrain is rugged, with little fertile land, and the weather is unpredictable. Expansion will be slow."
            ),
            "Nightmare": (
                "You have chosen to settle in an unknown island. The resources are barely sufficient to sustain a small settlement. "
                "The environment is treacherous, with frequent natural disasters, droughts, and harsh conditions. "
                "Survival is a constant struggle, and every decision could be the difference between life and death."
            )
        }
        print(f"\n🌍 Land Description: {descriptions[difficulty]}")

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
    game = LoopGame()
    game.start()
