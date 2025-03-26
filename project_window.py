import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Ferdi's Window Page")
window.geometry("400x300")

def botton_get():
    messagebox.showinfo("information", "You reach botton!")

botton = tk.Button(window, text="Click this Botton!", command=botton_get())
botton.pack(pady=20)

window.mainloop()