# Expense Tracker

import os

DATA_FILE = "my_data.txt"
BUDGET_FILE = "my_budget.txt"

# All transactions are stored in this list
records = []

# Monthly budget (0 means not set)
monthly_budget = 0


# ---------- File functions ----------

def load_data():
    global monthly_budget

    # Read transactions from file
    if os.path.exists(DATA_FILE):
        file = open(DATA_FILE, "r")
        for line in file:
            line = line.strip()
            if line == "":
                continue
            parts = line.split("|")
            item = {
                "type": parts[0],
                "amount": float(parts[1]),
                "category": parts[2],
                "date": parts[3],
                "note": parts[4]
            }
            records.append(item)
        file.close()

    # Read budget from file
    if os.path.exists(BUDGET_FILE):
        file = open(BUDGET_FILE, "r")
        monthly_budget = float(file.read())
        file.close()


def save_data():
    file = open(DATA_FILE, "w")
    for item in records:
        line = item["type"] + "|" + str(item["amount"]) + "|" + item["category"] + "|" + item["date"] + "|" + item["note"]
        file.write(line + "\n")
    file.close()


# ---------- Main features ----------

def add_income():
    amount = float(input("Income amount: "))
    date = input("Date (dd-mm-yyyy): ")
    note = input("Note: ")

    item = {
        "type": "Income",
        "amount": amount,
        "category": "Salary/Income",
        "date": date,
        "note": note
    }
    records.append(item)
    save_data()
    print("Income saved!")


def add_expense():
    amount = float(input("Expense amount: "))
    print("Examples: Food, Travel, Shopping, Bills, Entertainment")
    category = input("Category: ")
    date = input("Date (dd-mm-yyyy): ")
    note = input("Note: ")

    item = {
        "type": "Expense",
        "amount": amount,
        "category": category,
        "date": date,
        "note": note
    }
    records.append(item)
    save_data()
    print("Expense saved!")


def show_all():
    if len(records) == 0:
        print("Nothing to show yet.")
        return

    print("\nDate | Type | Category | Amount | Note")
    print("-" * 50)
    for item in records:
        print(item["date"], "|", item["type"], "|", item["category"], "|", item["amount"], "|", item["note"])


def show_summary():
    income = 0
    expense = 0

    for item in records:
        if item["type"] == "Income":
            income = income + item["amount"]
        else:
            expense = expense + item["amount"]

    print("\n--- Summary ---")
    print("Total Income  :", income)
    print("Total Expense :", expense)
    print("Balance       :", income - expense)


def set_budget():
    global monthly_budget
    monthly_budget = float(input("Enter monthly budget: "))

    file = open(BUDGET_FILE, "w")
    file.write(str(monthly_budget))
    file.close()
    print("Budget saved!")


def show_budget_left():
    if monthly_budget == 0:
        print("Budget is not set. Please set it first.")
        return

    spent = 0
    for item in records:
        if item["type"] == "Expense":
            spent = spent + item["amount"]

    left = monthly_budget - spent

    print("\n--- Budget ---")
    print("Budget    :", monthly_budget)
    print("Spent     :", spent)
    print("Remaining :", left)

    if left < 0:
        print("Alert: You spent more than your budget!")


def find_transaction():
    word = input("Search (category / note / date): ").lower()
    count = 0

    for item in records:
        if word in item["category"].lower() or word in item["note"].lower() or word in item["date"]:
            print(item["date"], "|", item["type"], "|", item["category"], "|", item["amount"], "|", item["note"])
            count = count + 1

    if count == 0:
        print("No result found.")


def month_report():
    month = input("Enter month (mm-yyyy), example 11-2026: ")

    income = 0
    expense = 0
    category_total = {}

    for item in records:
        # date is dd-mm-yyyy, so split it by "-"
        parts = item["date"].split("-")
        item_month = parts[1] + "-" + parts[2]

        if item_month == month:
            if item["type"] == "Income":
                income = income + item["amount"]
            else:
                expense = expense + item["amount"]
                cat = item["category"]
                if cat in category_total:
                    category_total[cat] = category_total[cat] + item["amount"]
                else:
                    category_total[cat] = item["amount"]

    print("\n--- Report for", month, "---")
    print("Income  :", income)
    print("Expense :", expense)
    print("Balance :", income - expense)

    print("\nExpense by category:")
    for cat in category_total:
        print(cat, "=", category_total[cat])


# ---------- Program starts here ----------

load_data()

running = True
while running:
    print("\n=========== MENU ===========")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Show All Transactions")
    print("4. Show Summary")
    print("5. Set Budget")
    print("6. Show Remaining Budget")
    print("7. Search")
    print("8. Monthly Report")
    print("9. Exit")

    option = input("Choose option: ")

    if option == "1":
        add_income()
    elif option == "2":
        add_expense()
    elif option == "3":
        show_all()
    elif option == "4":
        show_summary()
    elif option == "5":
        set_budget()
    elif option == "6":
        show_budget_left()
    elif option == "7":
        find_transaction()
    elif option == "8":
        month_report()
    elif option == "9":
        print("Bye!")
        running = False
    else:
        print("Wrong option, try again.")