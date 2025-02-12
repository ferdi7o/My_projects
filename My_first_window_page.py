import tkinter as tk

# create a windows
root = tk.Tk()
root.title("My Page")

# Window size
root.geometry("400x300")

# hactack
label = tk.Label(root, text="Merhaba, PyCharm!", font=("Arial", 14))
label.pack(pady=20)

# close button
button = tk.Button(root, text="Kapat", command=root.destroy)
button.pack()

root.mainloop()