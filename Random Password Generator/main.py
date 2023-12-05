import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        # Variables to store user preferences
        self.length_var = tk.IntVar(value=12)
        self.use_letters_var = tk.BooleanVar(value=True)
        self.use_numbers_var = tk.BooleanVar(value=True)
        self.use_symbols_var = tk.BooleanVar(value=True)

        # Variable to store the generated password
        self.generated_password_var = tk.StringVar(value="")

        # Create and pack GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for password length
        length_label = ttk.Label(self.root, text="Password Length:")
        length_entry = ttk.Entry(self.root, textvariable=self.length_var, width=5)
        length_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        length_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Checkbuttons for character types with tooltips
        letters_check = ttk.Checkbutton(self.root, text="Include Letters", variable=self.use_letters_var, command=self.show_tooltip_letters)
        numbers_check = ttk.Checkbutton(self.root, text="Include Numbers", variable=self.use_numbers_var, command=self.show_tooltip_numbers)
        symbols_check = ttk.Checkbutton(self.root, text="Include Symbols", variable=self.use_symbols_var, command=self.show_tooltip_symbols)
        letters_check.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        numbers_check.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        symbols_check.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        # Button to generate password
        generate_button = ttk.Button(self.root, text="Generate Password", command=self.generate_password)
        generate_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Entry to display generated password
        password_entry = ttk.Entry(self.root, textvariable=self.generated_password_var, state='readonly', font='TkFixedFont')
        password_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W + tk.E)

        # Button to copy password to clipboard
        copy_button = ttk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.grid(row=6, column=0, columnspan=2, pady=5)

    def show_tooltip_letters(self):
        messagebox.showinfo("Include Letters", "Include both uppercase and lowercase letters for better security.")

    def show_tooltip_numbers(self):
        messagebox.showinfo("Include Numbers", "Include numeric digits to enhance password strength.")

    def show_tooltip_symbols(self):
        messagebox.showinfo("Include Symbols", "Include symbols such as ! @ # $ % for added complexity.")

    def generate_password(self):
        # Define character sets based on user preferences
        letters = string.ascii_letters if self.use_letters_var.get() else ""
        numbers = string.digits if self.use_numbers_var.get() else ""
        symbols = string.punctuation if self.use_symbols_var.get() else ""

        # Combine character sets
        all_characters = letters + numbers + symbols

        if not all_characters:
            messagebox.showwarning("Warning", "Please select at least one character type.")
            return

        # Generate the password
        password = ''.join(random.choice(all_characters) for _ in range(self.length_var.get()))

        # Display the generated password in the Entry widget
        self.generated_password_var.set(password)

        # Return the password (useful for copy_to_clipboard)
        return password

    def copy_to_clipboard(self):
        # Get the generated password
        password = self.generate_password()

        # Copy the password to the clipboard
        pyperclip.copy(password)
        messagebox.showinfo("Clipboard", "Password copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
