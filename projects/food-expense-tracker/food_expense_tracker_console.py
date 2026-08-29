"""
Expense Tracker (Food Expenses)

Name: Ayalew Cherenet
Course: Programming I
Date: December 26, 2025

Extra Credit Implemented:
- Save & Load (JSON file)
- Delete Expense
- Input Validation (amount must be a valid number and >= 0)
"""

import json
import os

DATA_FILE = "expenses.json"
VALID_CATEGORIES = {"Breakfast", "Lunch", "Dinner", "Snack"}


def display_menu():
    print("\n=== Food Expense Tracker ===")
    print("1. Add food expense")
    print("2. View all food expenses")
    print("3. View total food spending")
    print("4. View food spending by category")
    print("5. Delete an expense (extra credit)")
    print("6. Quit")


def load_expenses(filename=DATA_FILE):
    """Load expenses from a JSON file. Returns a list."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            # Ensure each item looks like an expense dict
            cleaned = []
            for item in data:
                if isinstance(item, dict):
                    cleaned.append({
                        "description": str(item.get("description", "")).strip(),
                        "amount": float(item.get("amount", 0)),
                        "category": str(item.get("category", "Uncategorized")).strip()
                    })
            return cleaned
        return []
    except (json.JSONDecodeError, OSError, ValueError):
        # If file is corrupted or unreadable, start fresh safely
        return []


def save_expenses(expenses, filename=DATA_FILE):
    """Save expenses to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2)
    except OSError:
        print("\nWarning: Could not save expenses to file.")


def get_valid_amount(prompt="Amount: $"):
    """Keep asking until the user enters a valid non-negative number."""
    while True:
        raw = input(prompt).strip()
        try:
            amount = float(raw)
            if amount < 0:
                print("Amount must be 0 or greater. Try again.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number (example: 12.50).")


def get_valid_category():
    """Ask for a category and normalize it."""
    while True:
        cat = input("Category (Breakfast, Lunch, Dinner, Snack): ").strip()
        # Normalize capitalization: "lunch" -> "Lunch"
        cat_norm = cat.capitalize()
        if cat_norm in VALID_CATEGORIES:
            return cat_norm
        print("Invalid category. Please type: Breakfast, Lunch, Dinner, or Snack.")


def add_expense(expenses):
    description = input("\nFood Merchant/Description: ").strip()
    if not description:
        description = "Unknown"

    amount = get_valid_amount("Amount: $")
    category = get_valid_category()

    expenses.append({
        "description": description,
        "amount": amount,
        "category": category
    })

    save_expenses(expenses)
    print("\n✅ Expense added and saved!")


def view_expenses(expenses):
    if not expenses:
        print("\nNo food expenses recorded yet.")
        return

    print("\n--- All Food Expenses ---")
    print(f"{'#':<4}{'Merchant/Description':<28}{'Category':<12}{'Amount':>10}")
    print("-" * 54)

    total = 0.0
    for i, exp in enumerate(expenses, start=1):
        desc = exp.get("description", "")
        cat = exp.get("category", "Uncategorized")
        amt = float(exp.get("amount", 0))
        total += amt
        print(f"{i:<4}{desc[:26]:<28}{cat:<12}${amt:>9.2f}")

    print("-" * 54)
    print(f"{'':<44}Total: ${total:>.2f}")


def view_total(expenses):
    total = sum(float(exp.get("amount", 0)) for exp in expenses)
    print(f"\nTotal food spending: ${total:.2f}")


def view_by_category(expenses):
    if not expenses:
        print("\nNo food expenses recorded yet.")
        return

    cat_input = input("\nEnter a category (Breakfast/Lunch/Dinner/Snack): ").strip().capitalize()
    if cat_input not in VALID_CATEGORIES:
        print("Invalid category.")
        return

    total_cat = sum(
        float(exp.get("amount", 0))
        for exp in expenses
        if str(exp.get("category", "")).strip().capitalize() == cat_input
    )
    print(f"\nTotal spent on {cat_input}: ${total_cat:.2f}")


def delete_expense(expenses):
    if not expenses:
        print("\nNo expenses to delete.")
        return

    view_expenses(expenses)
    while True:
        choice = input("\nEnter the # of the expense to delete (or press Enter to cancel): ").strip()
        if choice == "":
            print("Delete cancelled.")
            return
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(expenses):
            print("That number is out of range. Try again.")
            continue

        removed = expenses.pop(idx)
        save_expenses(expenses)
        print(f"\n🗑️ Deleted: {removed.get('description','(unknown)')} - ${float(removed.get('amount',0)):.2f}")
        return


def main():
    expenses = load_expenses()
    if expenses:
        print(f"Loaded {len(expenses)} saved expense(s) from {DATA_FILE}.")
    else:
        print("No saved expenses found. Starting fresh.")

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_total(expenses)
        elif choice == "4":
            view_by_category(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            print("\nThanks for using the Food Expense Tracker!")
            break
        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()
