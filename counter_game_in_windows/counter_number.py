import tkinter as tk
from tkinter import messagebox

counter = 0

def increase_counter():
    global counter
    counter += 1
    label.config(text=f"Click: {counter}")
    if counter >= 10:
        show_message()

def show_message():
    messagebox.showinfo("Wrong - infromation", "Game Over!")
    root.destroy()

root = tk.Tk()
root.title("Click Counter")
root.geometry("300x200")

label = tk.Label(root, text="Number: 0", font=("Helvetica", 24))
label.pack(pady=20)

# Buton
button = tk.Button(root, text="Click!", command=increase_counter, font=("Helvetica", 16))
button.pack()

root.mainloop()