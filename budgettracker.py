import json
import tkinter as tk
from tkinter import ttk

# Initialize budget data
budget_data = {
    "income": 0,
    "expenses": [],
}

# Function to save budget data to a file
def save_budget_data(data):
    with open("budget_data.json", "w") as file:
        json.dump(data, file)

# Function to load budget data from a file
def load_budget_data():
    try:
        with open("budget_data.json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return budget_data

# Function to add income
def add_income():
    amount = float(income_entry.get())
    budget_data["income"] += amount
    income_label.config(text=f"Income: ${budget_data['income']:.2f}")
    income_entry.delete(0, 'end')
    save_budget_data(budget_data)

# Function to add an expense
def add_expense():
    category = category_entry.get()
    amount = float(expense_entry.get())
    budget_data["expenses"].append({"category": category, "amount": amount})
    expense_entry.delete(0, 'end')
    category_entry.delete(0, 'end')
    save_budget_data(budget_data)

# Function to manually calculate the budget
def calculate_budget():
    remaining_budget = calculate_remaining_budget()
    remaining_budget_label.config(text=f"Remaining Budget: ${remaining_budget:.2f}")

# Function to calculate the remaining budget
def calculate_remaining_budget():
    income = budget_data["income"]
    expenses = sum(item["amount"] for item in budget_data["expenses"])
    return income - expenses

# Function to analyze expenses by category
def analyze_expenses():
    categories = {}
    for expense in budget_data["expenses"]:
        category = expense["category"]
        amount = expense["amount"]
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount
    return categories

# Create the main window
root = tk.Tk()
root.title("Budget Tracker")

# Configure window size and colors
root.geometry("600x400")
root.configure(bg="#f0f0f0")

# Create a styled frame for the title
title_frame = tk.Frame(root, bg="#007acc")
title_frame.pack(fill="x", pady=(10, 5))

# Create a label for the title
title_label = ttk.Label(title_frame, text="Budget Tracker", font=("Helvetica", 24), foreground="white", background="#007acc")
title_label.pack(pady=(5, 0))

# Create labels and entry fields with updated styles
income_label = ttk.Label(root, text=f"Income: ${budget_data['income']:.2f}", font=("Helvetica", 16))
income_label.pack(pady=10)

income_entry = ttk.Entry(root, font=("Helvetica", 14))
income_entry.pack()

income_button = ttk.Button(root, text="Add Income", command=add_income, style="TButton")
income_button.pack(pady=5)

category_entry = ttk.Entry(root, font=("Helvetica", 14))
category_entry.pack()

expense_entry = ttk.Entry(root, font=("Helvetica", 14))
expense_entry.pack()

expense_button = ttk.Button(root, text="Add Expense", command=add_expense, style="TButton")
expense_button.pack()

remaining_budget_label = ttk.Label(root, text=f"Remaining Budget: ${calculate_remaining_budget():.2f}", font=("Helvetica", 16))
remaining_budget_label.pack(pady=10)

# Create a listbox to display expense analysis
expense_listbox = tk.Listbox(root, font=("Helvetica", 14))
expense_listbox.pack()

# Function to update the expense listbox
def update_expense_listbox():
    expense_listbox.delete(0, 'end')
    expense_categories = analyze_expenses()
    for category, amount in expense_categories.items():
        expense_listbox.insert('end', f"{category}: ${amount:.2f}")

# Button to analyze expenses
analyze_button = ttk.Button(root, text="Analyze Expenses", command=update_expense_listbox, style="TButton")
analyze_button.pack()

# Button to manually calculate the budget
calculate_budget_button = ttk.Button(root, text="Calculate Budget", command=calculate_budget, style="TButton")
calculate_budget_button.pack()

# Load existing budget data
budget_data = load_budget_data()
income_label.config(text=f"Income: ${budget_data['income']:.2f}")
update_expense_listbox()

# Configure style for buttons
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=5, background="#007acc", foreground="white")
style.map("TButton", background=[("active", "#005f99")])

# Run the tkinter main loop
root.mainloop()
