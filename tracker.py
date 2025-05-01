import difflib
import json
from food import Food


daily_macros = {
    'protein': 150,
    'carbs': 200,
    'fats': 150
}


eaten_foods = []

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

available_foods = [
    Food("Chicken breast", 30, 0, 3, 100),
    Food("Rice (100g)", 2, 28, 0, 100),
    Food("Almonds (30g)", 6, 6, 15, 30),
    Food("Egg", 6, 0, 5, 1),
    Food("Banana", 1, 23, 0, 1),
]


def add_food():
    name = input("Enter food name (or 'exit' to quit): ")
    if name.lower() == 'exit':
        exit()
    quantity = input("Enter quantity (in servings, e.g. 1 egg, 1 chicken breast(100 grams)): ")
    available_names = [food.name for food in available_foods]
    matches = difflib.get_close_matches(name, available_names, n=1, cutoff=0.6)
    if matches:
        for foods in available_foods:
            if foods.name.lower() == matches[0].lower():
                print("Matched: %s\n" % foods.name)
                multiplier = float(quantity) / foods.quantity
                real_ammount_protein = foods.protein * multiplier
                real_ammount_carbs = foods.carbs * multiplier
                real_ammount_fats = foods.fats * multiplier
                print(f"-> Added: {foods.name} ({real_ammount_protein:.1f}P / {real_ammount_carbs:.1f}C / {real_ammount_fats:.1f}F)")
                eaten_foods.append(
                    Food(foods.name, real_ammount_protein, real_ammount_carbs, real_ammount_fats, quantity)
                )


def print_remaining_macros():
    consumed = {'protein': 0, 'carbs': 0, 'fats': 0}
    for food in eaten_foods:
        consumed['protein'] += food.protein
        consumed['carbs'] += food.carbs
        consumed['fats'] += food.fats
    print("\nRemaining macros:")
    for macro in daily_macros:
        remaining = daily_macros[macro] - consumed[macro]
        print(f"{macro.capitalize()}: {remaining}g")
        if remaining < 0:
            print(f"Warning: You have exceeded your daily {macro} goal!")

    print("\nEaten foods:")
    for food in eaten_foods:
        print(f"{food.name}: {food.protein}g protein, {food.carbs}g carbs, {food.fats}g fats")

def suggest_foods():
    print("\nSuggested foods to complete your macros:")
    consumed = {'protein': 0, 'carbs': 0, 'fats': 0}
    for food in eaten_foods:
        consumed['protein'] += food.protein
        consumed['carbs'] += food.carbs
        consumed['fats'] += food.fats

    remaining = {
        'protein': daily_macros['protein'] - consumed['protein'],
        'carbs': daily_macros['carbs'] - consumed['carbs'],
        'fats': daily_macros['fats'] - consumed['fats'],
    }

    for food in available_foods:
        max_multiplier = min(
            remaining['protein'] / food.protein if food.protein > 0 else float('inf'),
            remaining['carbs'] / food.carbs if food.carbs > 0 else float('inf'),
            remaining['fats'] / food.fats if food.fats > 0 else float('inf'),
        )

        if max_multiplier <= 0:
            continue  # skip foods that would exceed macros

        suggested_amount = max_multiplier * food.quantity
        unit = "unit" if food.quantity == 1 else "g"

        print(f"- {food.name}: up to {suggested_amount:.0f}{unit} ({food.protein:.1f}P / {food.carbs:.1f}C / {food.fats:.1f}F per {unit})")



def load_eaten_foods():
    try:
        with open('eaten_foods.json', 'r') as file:
            try:
                data = json.load(file)
                for item in data:
                    food = Food(item['name'], item['protein'], item['carbs'], item['fats'], item['quantity'])
                    eaten_foods.append(food)
            except json.JSONDecodeError:
                print("Error decoding JSON. Starting with an empty list of eaten foods.")
    except FileNotFoundError:
        print("No previous food data found.")

def save_eaten_foods():
    with open('eaten_foods.json', 'w') as file:
        data = [
            {'name': food.name, 'protein': food.protein, 'carbs': food.carbs, 'fats': food.fats, 'quantity': food.quantity}
            for food in eaten_foods
        ]
        json.dump(data, file)

def empty_eaten_foods():
    question = input("Do you want to clear the eaten foods? (yes/no): ")
    if question.lower() == 'yes':
        with open('eaten_foods.json', 'w') as file:
            json.dump([], file)
            global eaten_foods
            eaten_foods = []
        print("Eaten foods cleared.")
