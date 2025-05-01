from tracker import *
import tkinter as tk
from tkinter import messagebox, ttk

root = tk.Tk()
root.title("Macro Tracker")
root.geometry("500x600")
# --- Basic UI Elements ---

# Dropdown: choose a food
food_names = [food.name for food in available_foods]
selected_food = tk.StringVar()
food_dropdown = ttk.Combobox(root, textvariable=selected_food, values=food_names)
food_dropdown.pack(pady=5)
food_dropdown.set("Choose a food")

# Entry: quantity
quantity_entry = tk.Entry(root)
quantity_entry.pack(pady=5)
quantity_entry.insert(0, "1")

# Button: add food
def add_food_gui():
    name = selected_food.get()
    quantity = quantity_entry.get()
    if not quantity.replace('.', '', 1).isdigit():
        messagebox.showerror("Error", "Quantity must be a number.")
        return
    matches = difflib.get_close_matches(name, food_names, n=1, cutoff=0.6)
    if not matches:
        messagebox.showerror("Error", f"No food matched.")
        return
    for food in available_foods:
        if food.name == matches[0]:
            multiplier = float(quantity) / food.quantity
            eaten_foods.append(Food(
                food.name,
                food.protein * multiplier,
                food.carbs * multiplier,
                food.fats * multiplier,
                quantity
            ))
            save_eaten_foods()
            update_ui()
            break

add_button = tk.Button(root, text="Add Food", command=add_food_gui)
add_button.pack(pady=5)


load_eaten_foods()
root.mainloop()

