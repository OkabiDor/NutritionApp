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
result_label = tk.Label(root, text="Remaining Macros:\n"
                              f"Protein: {daily_macros['protein']:.1f}\n"
                              f"Carbs: {daily_macros['carbs']:.1f}\n"
                              f"Fats: {daily_macros['fats']:.1f}")
result_label.pack(pady=10)
eaten_foods_ui = ttk.Treeview(root, columns=("Food","Quantity", "Protein", "Carbs", "Fats"), show='headings')
eaten_foods_ui.heading("Food", text="Food")
eaten_foods_ui.column("Food", width=150, stretch=False)
eaten_foods_ui.heading("Quantity", text="Quantity")
eaten_foods_ui.column("Quantity", width=80, stretch=False)
eaten_foods_ui.heading("Protein", text="Protein")
eaten_foods_ui.column("Protein", width=80, stretch=False)
eaten_foods_ui.heading("Carbs", text="Carbs")
eaten_foods_ui.column("Carbs", width=80, stretch=False)
eaten_foods_ui.heading("Fats", text="Fats")
eaten_foods_ui.column("Fats", width=80, stretch=False)
eaten_foods_ui.pack(pady=10, fill=tk.X)

# Entry: quantity
quantity_entry = tk.Entry(root)
quantity_entry.pack(pady=5)
quantity_entry.insert(0, "1")
if messagebox.askyesno(title= "Load Data", message="Do you want to load previous data?"):
    load_eaten_foods()
    # Function to save eaten foods to a file


def update_ui():
    consumed = {'protein': 0, 'carbs': 0, 'fats': 0}
    for food in eaten_foods:
        consumed['protein'] += food.protein
        consumed['carbs'] += food.carbs
        consumed['fats'] += food.fats

    remaining = {
        'protein': daily_macros['protein'] - consumed['protein'],
        'carbs': daily_macros['carbs'] - consumed['carbs'],
        'fats': daily_macros['fats'] - consumed['fats']
    }

    result_label.config(text=f"Remaining Macros:\n"
                              f"Protein: {remaining['protein']:.1f}\n"
                              f"Carbs: {remaining['carbs']:.1f}\n"
                              f"Fats: {remaining['fats']:.1f}")
    eaten_foods_ui.delete(*eaten_foods_ui.get_children())
    for food in eaten_foods:
        eaten_foods_ui.insert("", "end", values=(food.name, food.quantity, food.protein, food.carbs, food.fats))
    


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


root.mainloop()

