import tkinter as tk
import random
import math

WIDTH = 800
HEIGHT = 600

# Renkler
colors = ["#FFC0CB", "#87CEFA", "#7FFFD4", "#FFD700", "#ADFF2F", "#FF69B4", "#40E0D0"]

# Mesajlar
messages = [
    "Sen bir sanatçısın 🎨",
    "Hayal gücünün sınırı yok 🚀",
    "Kodla evren yaratıyorsun 🌌",
    "Bu sadece başlangıç 🔥",
    "Ferdi'nin evreni yükleniyor... ⏳",
    "Bir yıldız doğuyor ⭐",
    "Şu an evrende bir şekil dans ediyor..."
]

# Ana pencere
root = tk.Tk()
root.title("🌈 Dreamland: Canlı Tuval")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

floating_shapes = []


def create_floating_shape():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(20, 60)
    color = random.choice(colors)
    shape_type = random.choice(["oval", "star", "bubble"])

    if shape_type == "oval":
        shape = canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
    elif shape_type == "bubble":
        shape = canvas.create_oval(x, y, x + size, y + size, fill="", outline=color, width=2)
    else:  # yıldız
        points = []
        for i in range(5):
            angle = i * (2 * math.pi / 5)
            outer_x = x + size * math.cos(angle)
            outer_y = y + size * math.sin(angle)
            points.extend([outer_x, outer_y])
        shape = canvas.create_polygon(points, fill=color, outline="white")

    floating_shapes.append((shape, random.uniform(0.5, 1.5)))


def animate():
    for shape, speed in floating_shapes:
        canvas.move(shape, 0, -speed)
        coords = canvas.coords(shape)
        if coords and coords[1] < -50:
            canvas.delete(shape)
            floating_shapes.remove((shape, speed))
    root.after(30, animate)


def burst(event):
    for _ in range(10):
        create_floating_shape()
    message = random.choice(messages)
    canvas.create_text(event.x, event.y, text=message, fill=random.choice(colors), font=("Helvetica", 14, "bold"))


# Her 500ms'de yeni şekil üret
def generate_shapes():
    create_floating_shape()
    root.after(500, generate_shapes)


# Renkleri yavaşça değiştir
def color_cycle():
    color = random.choice(colors)
    canvas.config(bg=color)
    root.after(3000, color_cycle)


# Tıklama olayı
canvas.bind("<Button-1>", burst)

# Başlat
generate_shapes()
animate()
color_cycle()
root.mainloop()
