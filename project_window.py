import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Ferdi's Window Page")
window.geometry("400x300")

etiket = tk.Label(window, text="Your name:")
etiket.pack(pady=5)

entry_box = tk.Entry(window)
entry_box.pack(pady=5)

def show_message():
    mesage = entry_box.get()
    messagebox.showinfo("WRONG - information", f"Your name is {mesage}")

buton = tk.Button(window, text="Show message!", command=show_message)
buton.pack(pady=10)

close = tk.Button(window, text="Close", command=window.destroy)
close.pack(pady=50)

exit = tk.Button(window, text="Exit", command= window.destroy)
exit.pack()
window.mainloop()