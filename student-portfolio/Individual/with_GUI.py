import tkinter as tk
from tkinter import messagebox
import json
import os


# Define Account class
class Account:
    def __init__(self, acc_no, name, address, phone, amt=0.0):
        self.acc_no = acc_no
        self.name = name
        self.address = address
        self.phone = phone
        self.amt = amt

    def to_dict(self):
        return {
            "acc_no": self.acc_no,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "amt": self.amt
        }

    @staticmethod
    def from_dict(data):
        return Account(data['acc_no'], data['name'], data['address'], data['phone'], data['amt'])


# File to store account data
data_file = "accounts.json"


# Load data from the JSON file
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            data = json.load(file)
            # Convert the dictionary back to Account objects
            return [Account.from_dict(acc) for acc in data]
    return []


# Save data to the JSON file
def save_data(accounts):
    with open(data_file, "w") as file:
        # Convert Account objects to dictionaries before saving
        json.dump([acc.to_dict() for acc in accounts], file, indent=4)


# Function to view all accounts
def view_accounts():
    accounts = load_data()
    if not accounts:
        messagebox.showinfo("No records found", "No records found.")
        return

    account_list = "\n".join([f"ACC. NO: {acc.acc_no}, NAME: {acc.name}, PHONE: {acc.phone}" for acc in accounts])

    messagebox.showinfo("Accounts", account_list)


# Function to edit account details
def edit_account():
    def save_changes():
        acc_no = int(acc_no_entry.get())
        account = next((acc for acc in accounts if acc.acc_no == acc_no), None)

        if account:
            if address_var.get():
                account.address = address_var.get()
            if phone_var.get():
                account.phone = phone_var.get()

            save_data(accounts)
            messagebox.showinfo("Success", "Account updated successfully.")
        else:
            messagebox.showwarning("Account not found", "Account not found.")

    accounts = load_data()

    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Account")

    tk.Label(edit_window, text="Enter Account Number:").grid(row=0, column=0)
    acc_no_entry = tk.Entry(edit_window)
    acc_no_entry.grid(row=0, column=1)

    tk.Label(edit_window, text="New Address:").grid(row=1, column=0)
    address_var = tk.StringVar()
    address_entry = tk.Entry(edit_window, textvariable=address_var)
    address_entry.grid(row=1, column=1)

    tk.Label(edit_window, text="New Phone:").grid(row=2, column=0)
    phone_var = tk.StringVar()
    phone_entry = tk.Entry(edit_window, textvariable=phone_var)
    phone_entry.grid(row=2, column=1)

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=3, columnspan=2)


# Function to perform deposit or withdrawal transactions
def transact():
    def process_transaction():
        acc_no = int(acc_no_entry.get())
        account = next((acc for acc in accounts if acc.acc_no == acc_no), None)

        if account:
            transaction_choice = trans_choice_var.get()
            amount = float(amount_entry.get())

            if transaction_choice == 1:  # Deposit
                account.amt += amount
                messagebox.showinfo("Success", f"Deposited ${amount}. New balance: ${account.amt}")
            elif transaction_choice == 2:  # Withdraw
                if amount <= account.amt:
                    account.amt -= amount
                    messagebox.showinfo("Success", f"Withdrew ${amount}. New balance: ${account.amt}")
                else:
                    messagebox.showwarning("Insufficient funds", "Insufficient funds.")
            save_data(accounts)
        else:
            messagebox.showwarning("Account not found", "Account not found.")

    accounts = load_data()

    trans_window = tk.Toplevel(window)
    trans_window.title("Transaction")

    tk.Label(trans_window, text="Enter Account Number:").grid(row=0, column=0)
    acc_no_entry = tk.Entry(trans_window)
    acc_no_entry.grid(row=0, column=1)

    tk.Label(trans_window, text="Transaction Amount:").grid(row=1, column=0)
    amount_entry = tk.Entry(trans_window)
    amount_entry.grid(row=1, column=1)

    trans_choice_var = tk.IntVar()

    tk.Radiobutton(trans_window, text="Deposit", variable=trans_choice_var, value=1).grid(row=2, column=0)
    tk.Radiobutton(trans_window, text="Withdraw", variable=trans_choice_var, value=2).grid(row=2, column=1)

    process_button = tk.Button(trans_window, text="Process Transaction", command=process_transaction)
    process_button.grid(row=3, columnspan=2)


# Function to delete an account
def delete_account():
    def delete():
        accounts = load_data()  # Move loading inside the delete function
        acc_no = int(acc_no_entry.get())
        account = next((acc for acc in accounts if acc.acc_no == acc_no), None)

        if account:
            accounts = [acc for acc in accounts if acc.acc_no != acc_no]
            save_data(accounts)
            messagebox.showinfo("Success", f"Account {acc_no} deleted successfully.")
        else:
            messagebox.showwarning("Account not found", "Account not found.")

    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Account")

    tk.Label(delete_window, text="Enter Account Number:").grid(row=0, column=0)
    acc_no_entry = tk.Entry(delete_window)
    acc_no_entry.grid(row=0, column=1)

    delete_button = tk.Button(delete_window, text="Delete Account", command=delete)
    delete_button.grid(row=1, columnspan=2)


# Function to create a new account
def create_account():
    def save_account():
        acc_no = int(acc_no_entry.get())
        name = name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        amt = float(amt_entry.get())

        accounts = load_data()

        if any(acc.acc_no == acc_no for acc in accounts):
            messagebox.showwarning("Account Exists", f"Account number {acc_no} already exists.")
            return

        new_account = Account(acc_no, name, address, phone, amt)
        accounts.append(new_account)

        save_data(accounts)
        messagebox.showinfo("Success", "Account created successfully.")
        create_window.destroy()

    create_window = tk.Toplevel(window)
    create_window.title("Create Account")

    tk.Label(create_window, text="Enter Account Number:").grid(row=0, column=0)
    acc_no_entry = tk.Entry(create_window)
    acc_no_entry.grid(row=0, column=1)

    tk.Label(create_window, text="Enter Name:").grid(row=1, column=0)
    name_entry = tk.Entry(create_window)
    name_entry.grid(row=1, column=1)

    tk.Label(create_window, text="Enter Address:").grid(row=2, column=0)
    address_entry = tk.Entry(create_window)
    address_entry.grid(row=2, column=1)

    tk.Label(create_window, text="Enter Phone:").grid(row=3, column=0)
    phone_entry = tk.Entry(create_window)
    phone_entry.grid(row=3, column=1)

    tk.Label(create_window, text="Enter Initial Deposit:").grid(row=4, column=0)
    amt_entry = tk.Entry(create_window)
    amt_entry.grid(row=4, column=1)

    save_button = tk.Button(create_window, text="Create Account", command=save_account)
    save_button.grid(row=5, columnspan=2)


# Main window
window = tk.Tk()
window.title("Bank Account Management System")

# Main menu buttons
tk.Button(window, text="Create Account", command=create_account).pack(pady=10)
tk.Button(window, text="View Accounts", command=view_accounts).pack(pady=10)
tk.Button(window, text="Edit Account", command=edit_account).pack(pady=10)
tk.Button(window, text="Transaction (Deposit/Withdraw)", command=transact).pack(pady=10)
tk.Button(window, text="Delete Account", command=delete_account).pack(pady=10)

window.mainloop()