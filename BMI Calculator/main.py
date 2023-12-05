import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate BMI
def calculate_bmi(weight, height):
    try:
        bmi = weight / (height ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return None

# Function to save BMI data to SQLite database
def save_bmi_data(name, weight, height, bmi):
    connection = sqlite3.connect("bmi_data.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_data
                      (name TEXT, weight REAL, height REAL, bmi REAL)''')

    cursor.execute("INSERT INTO bmi_data VALUES (?, ?, ?, ?)", (name, weight, height, bmi))
    connection.commit()

    connection.close()

# Function to show BMI trends using Matplotlib
def show_bmi_trends():
    connection = sqlite3.connect("bmi_data.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bmi_data")
    data = cursor.fetchall()

    connection.close()

    if not data:
        messagebox.showinfo("No Data", "No BMI data available.")
        return

    names, bmis = zip(*[(row[0], row[3]) for row in data])

    plt.bar(names, bmis)
    plt.xlabel('User')
    plt.ylabel('BMI')
    plt.title('BMI Trends')
    plt.show()

# Function to handle button click
def on_calculate_button_click():
    name = name_entry.get()
    weight = float(weight_entry.get())
    height = float(height_entry.get())

    bmi = calculate_bmi(weight, height)

    if bmi is not None:
        category = classify_bmi(bmi)
        result_text.set(f'BMI: {bmi} - {category}')
        save_bmi_data(name, weight, height, bmi)
    else:
        result_text.set('Error: Height should be greater than 0.')

# Function to classify BMI into categories
def classify_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal'
    else:
        return 'Overweight'

# Create main window
window = tk.Tk()
window.title('BMI Calculator')

# Create and place widgets
tk.Label(window, text='Name:').grid(row=0, column=0, padx=10, pady=10)
tk.Label(window, text='Weight (kg):').grid(row=1, column=0, padx=10, pady=10)
tk.Label(window, text='Height (m):').grid(row=2, column=0, padx=10, pady=10)

name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1, padx=10, pady=10)

weight_entry = tk.Entry(window)
weight_entry.grid(row=1, column=1, padx=10, pady=10)

height_entry = tk.Entry(window)
height_entry.grid(row=2, column=1, padx=10, pady=10)

calculate_button = tk.Button(window, text='Calculate BMI', command=on_calculate_button_click)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(window, textvariable=result_text)
result_label.grid(row=4, column=0, columnspan=2, pady=10)

show_trends_button = tk.Button(window, text='Show BMI Trends', command=show_bmi_trends)
show_trends_button.grid(row=5, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
window.mainloop()
