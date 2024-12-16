import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="recipe-db.chkkm606ubqg.us-east-2.rds.amazonaws.com",  # Your RDS endpoint
    user="admin",  # Your RDS username
    password="recipeDB",  # Your RDS password
    database="recipes"  # Your database name
)

cursor = db.cursor()

# Fetch all recipes from the database
def fetch_recipes():
    cursor.execute("SELECT * FROM Recipes")  # Corrected table name with capital R
    rows = cursor.fetchall()
    for row in rows:
        recipe_text = f"Name: {row[1]}\nIngredients: {row[2]}\nInstructions: {row[3]}\nCuisine: {row[4]}\nDifficulty: {row[5]}\nPrep Time: {row[6]}\n\n"
        label_recipe = tk.Label(frame_content, text=recipe_text, bg='#f0f0f0', font=("Arial", 12), justify="left", anchor="w")
        label_recipe.grid(row=6, column=0, columnspan=6, padx=10, pady=5, sticky="w")


# Add new recipe to the database
def add_recipe():
    name = entry_name.get()
    # Gather ingredients and quantities
    ingredients = "\n".join(f"{ingredient_entry.get()} - {quantity_entry.get()}" for ingredient_entry, quantity_entry in ingredient_entries)
    instructions = text_instructions.get("1.0", tk.END).strip()
    difficulty = entry_difficulty.get()
    cuisine = entry_cuisine.get()
    prep_time = entry_prep_time.get()

    if name and ingredients and instructions and difficulty and cuisine and prep_time:
        query = "INSERT INTO Recipes (name, ingredients, instructions, difficulty, cuisine, prep_time) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, ingredients, instructions, difficulty, cuisine, prep_time))
        db.commit()

        messagebox.showinfo("Success", "Recipe added successfully!")
        entry_name.delete(0, tk.END)
        entry_difficulty.delete(0, tk.END)
        entry_cuisine.delete(0, tk.END)
        entry_prep_time.delete(0, tk.END)
        text_instructions.delete("1.0", tk.END)
        ingredient_entries.clear()
        fetch_recipes()
    else:
        messagebox.showwarning("Input Error", "All fields must be filled!")


# Add new ingredient entry
def add_ingredient():
    ingredient_frame = tk.Frame(frame_ingredients_scrollable, bg='#f0f0f0')
    ingredient_frame.grid(row=len(ingredient_entries), column=0, padx=10, pady=5, sticky="w")
    
    entry_ingredient = tk.Entry(ingredient_frame, width=30, font=("Arial", 12))
    entry_ingredient.grid(row=0, column=0, padx=5, pady=5)
    
    entry_quantity = tk.Entry(ingredient_frame, width=15, font=("Arial", 12))
    entry_quantity.grid(row=0, column=1, padx=5, pady=5)
    
    ingredient_entries.append((entry_ingredient, entry_quantity))
    update_scrollregion()


# Delete last ingredient
def delete_ingredient():
    if ingredient_entries:
        ingredient_frame = frame_ingredients_scrollable.grid_slaves(row=len(ingredient_entries)-1, column=0)[0]
        ingredient_frame.destroy()
        ingredient_entries.pop()
        update_scrollregion()


def update_scrollregion():
    """Update the scroll region of the canvas based on the number of ingredients."""
    frame_ingredients_canvas.update_idletasks()  # Update tasks before recalculating scrollregion
    frame_ingredients_canvas.config(scrollregion=frame_ingredients_canvas.bbox("all"))


# Create the main window
window = tk.Tk()
window.title("Recipe Manager")
window.configure(bg='#f0f0f0')
window.geometry("900x800")  # Initial window size

# Make the window resizable
window.grid_rowconfigure(0, weight=1, minsize=500)
window.grid_columnconfigure(0, weight=1, minsize=900)

# Create a Canvas for scrollable content
canvas = tk.Canvas(window)
canvas.grid(row=0, column=0, sticky="nsew")

# Create a scrollbar for the canvas
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Link scrollbar with the canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame to hold all the widgets (inside canvas)
frame_content = tk.Frame(canvas, bg='#f0f0f0')
canvas.create_window((0, 0), window=frame_content, anchor="nw")

# Configure frame to expand
frame_content.grid_rowconfigure(0, weight=1)
frame_content.grid_rowconfigure(1, weight=0)
frame_content.grid_rowconfigure(2, weight=0)
frame_content.grid_rowconfigure(3, weight=0)  # Make ingredients frame stretchable
frame_content.grid_columnconfigure(0, weight=1)  # Make the frame column stretchable

# Recipe Name Entry
label_name = tk.Label(frame_content, text="Recipe Name:", bg='#f0f0f0', font=("Arial", 12, "bold"))
label_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_name = tk.Entry(frame_content, width=40, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=10, pady=5)

# Difficulty Entry
label_difficulty = tk.Label(frame_content, text="Difficulty:", bg='#f0f0f0', font=("Arial", 12, "bold"))
label_difficulty.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_difficulty = tk.Entry(frame_content, width=15, font=("Arial", 12))
entry_difficulty.grid(row=1, column=1, padx=10, pady=5)

# Cuisine Entry
label_cuisine = tk.Label(frame_content, text="Cuisine:", bg='#f0f0f0', font=("Arial", 12, "bold"))
label_cuisine.grid(row=1, column=2, padx=10, pady=5, sticky="w")

entry_cuisine = tk.Entry(frame_content, width=15, font=("Arial", 12))
entry_cuisine.grid(row=1, column=3, padx=10, pady=5)

# Prep Time Entry
label_prep_time = tk.Label(frame_content, text="Prep Time:", bg='#f0f0f0', font=("Arial", 12, "bold"))
label_prep_time.grid(row=1, column=4, padx=10, pady=5, sticky="w")

entry_prep_time = tk.Entry(frame_content, width=15, font=("Arial", 12))
entry_prep_time.grid(row=1, column=5, padx=10, pady=5)

# Add Ingredient Button
button_add_ingredient = tk.Button(frame_content, text="Add Ingredient", command=add_ingredient, bg='#4CAF50', fg='white', font=("Arial", 12, "bold"), relief="raised", bd=3)
button_add_ingredient.grid(row=2, column=0, pady=10, sticky="w")

# Delete Ingredient Button
button_delete_ingredient = tk.Button(frame_content, text="Delete Ingredient", command=delete_ingredient, bg='#F44336', fg='white', font=("Arial", 12, "bold"), relief="raised", bd=3)
button_delete_ingredient.grid(row=2, column=1, pady=10, sticky="w")

# Ingredients Label
label_ingredients = tk.Label(frame_content, text="Ingredients:", bg='#f0f0f0', font=("Arial", 12, "bold"))
label_ingredients.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Ingredients List Scrollable Frame
frame_ingredients_canvas = tk.Canvas(frame_content, bg='#e6e6e6', height=150, width=400)
frame_ingredients_canvas.grid(row=3, column=1, columnspan=4, padx=10, pady=5, sticky="w")

# Scrollable Frame for Ingredients
frame_ingredients_scrollable = tk.Frame(frame_ingredients_canvas, bg='#e6e6e6')
frame_ingredients_canvas.create_window((0, 0), window=frame_ingredients_scrollable, anchor="nw")

scrollbar_ingredients = tk.Scrollbar(frame_ingredients_canvas, orient="vertical", command=frame_ingredients_canvas.yview)
scrollbar_ingredients.grid(row=0, column=1, sticky="ns")

frame_ingredients_canvas.configure(yscrollcommand=scrollbar_ingredients.set)
frame_ingredients_canvas.grid_propagate(False)  # Prevent it from resizing

ingredient_entries = []  # List of ingredient fields

# Instructions Entry
label_instructions = tk.Label(frame_content, text="Instructions:", bg='#f0f0f0', font=("Arial", 12, "bold"))
label_instructions.grid(row=4, column=0, padx=10, pady=5, sticky="w")

text_instructions = tk.Text(frame_content, height=6, width=40, font=("Arial", 12))
text_instructions.grid(row=5, column=0, padx=10, pady=5)

# Add Recipe Button
button_add = tk.Button(frame_content, text="Add Recipe", command=add_recipe, bg='#4CAF50', fg='white', font=("Arial", 12, "bold"), relief="raised", bd=3)
button_add.grid(row=6, column=0, padx=10, pady=10, sticky="w")

# Fetch Recipes Button
button_fetch = tk.Button(frame_content, text="Fetch Recipes", command=fetch_recipes, bg='#2196F3', fg='white', font=("Arial", 12, "bold"), relief="raised", bd=3)
button_fetch.grid(row=7, column=0, padx=10, pady=10, sticky="w")

# Configure scrolling area for content frame
frame_content.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Start with fetching recipes
fetch_recipes()

# Start the main event loop
window.mainloop()
