import difflib
import json
import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from food import Food
from openai import OpenAI
import os
from google import genai


daily_macros = {
    'protein': 150,
    'carbs': 200,
    'fats': 150,
    'calories': 2500
}


eaten_foods = []

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

available_foods = [
    Food("Chicken breast", 30, 0, 3, 165, 100),
    Food("Rice (100g)", 2, 28, 0, 130, 100),
    Food("Almonds (30g)", 6, 6, 15, 173, 30),
    Food("Egg", 6, 0, 5, 70, 1),
    Food("Banana", 1, 23, 0, 105, 1),
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
                real_amount_calories = foods.calories * multiplier  
                print(f"-> Added: {foods.name} ({real_ammount_protein:.1f}P / {real_ammount_carbs:.1f}C / {real_ammount_fats:.1f}F, {real_amount_calories:.1f} Cal)\n")
                eaten_foods.append(
                    Food(foods.name, real_ammount_protein, real_ammount_carbs, real_ammount_fats, real_amount_calories, quantity)
                )


def print_remaining_macros():
    consumed = {'protein': 0, 'carbs': 0, 'fats': 0}
    for food in eaten_foods:
        consumed['protein'] += food.protein
        consumed['carbs'] += food.carbs
        consumed['fats'] += food.fats
        consumed['calories'] = food.calories
    print("\nRemaining macros:")
    for macro in daily_macros:
        remaining = daily_macros[macro] - consumed[macro]
        print(f"{macro.capitalize()}: {remaining}g")
        if remaining < 0:
            print(f"Warning: You have exceeded your daily {macro} goal!")

    print("\nEaten foods:")
    for food in eaten_foods:
        print(f"{food.name}: {food.protein}g protein, {food.carbs}g carbs, {food.fats}g fats, {food.calories} calories, Quantity: {food.quantity}")

def suggest_foods():
    consumed = {'protein': 0, 'carbs': 0, 'fats': 0, 'calories': 0}
    for food in eaten_foods:
        consumed['protein'] += food.protein
        consumed['carbs'] += food.carbs
        consumed['fats'] += food.fats
        consumed['calories'] = food.calories
    my_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=my_api_key)
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = "As a professional nutritionist suggest some meals to meet my remaining macros." \
        " My daily macros are: " + str(daily_macros) + \
        " I have already consumed: " + str(consumed) + "." \
        " Give 2 to 3 suggestions, of a dish that would fit best as the NEXT meal to eat." \
        " Provide the recipe if needed, but focus on the macros." \
        " Use the current time of the day to provide a meal that is appropriate (breakfast, lunch, dinner, snack)." \
    )
    print(response.text)
    remaining = {
        'protein': daily_macros['protein'] - consumed['protein'],
        'carbs': daily_macros['carbs'] - consumed['carbs'],
        'fats': daily_macros['fats'] - consumed['fats'],
        'calories': daily_macros['calories'] - consumed['calories'],
    }
    suggestions = []
    for food in available_foods:
        max_multiplier = min(
            remaining['protein'] / food.protein if food.protein > 0 else float('inf'),
            remaining['carbs'] / food.carbs if food.carbs > 0 else float('inf'),
            remaining['fats'] / food.fats if food.fats > 0 else float('inf'),
            remaining['calories'] / food.calories if food.calories > 0 else float('inf'),
        )

        if max_multiplier <= 0:
            continue  # skip foods that would exceed macros

        suggested_amount = max_multiplier * food.quantity
        unit = "unit" if food.quantity == 1 else "g"
        suggestion = f"{food.name}: up to {suggested_amount:.0f}{unit} ({food.protein:.1f}P / {food.carbs:.1f}C / {food.fats:.1f}F / {food.calories:.1F}Cal per {unit})"
        suggestions.append(suggestion)
    return suggestions



def load_eaten_foods():
    try:
        with open('eaten_foods.json', 'r') as file:
            try:
                data = json.load(file)
                if data.get('date') != str(datetime.date.today()):
                    print("Data is not from today. Starting with an empty list of eaten foods.")
                    return
                for item in data.get('foods', []):
                    food = Food(item['name'], item['protein'], item['carbs'], item['fats'], item['calories'], item['quantity'])
                    eaten_foods.append(food)
            except json.JSONDecodeError:
                print("Error decoding JSON. Starting with an empty list of eaten foods.")
    except FileNotFoundError:
        print("No previous food data found.")

def save_eaten_foods():
    with open('eaten_foods.json', 'w') as file:
        data = {
                'date': str(datetime.date.today()),
                'foods': [
                    {'name': food.name, 'protein': food.protein, 'carbs': food.carbs, 'fats': food.fats, 'calories' :food.calories, 'quantity': food.quantity}
                    for food in eaten_foods
                ]
            }
        json.dump(data, file)

def empty_eaten_foods():
    question = input("Do you want to clear the eaten foods? (yes/no): ")
    if question.lower() == 'yes':
        with open('eaten_foods.json', 'w') as file:
            json.dump({'date': str(datetime.date.today()), 'foods': []}, file)
        global eaten_foods
        eaten_foods = []
        print("Eaten foods cleared.")



