import tkinter as tk
from tkinter import messagebox, PhotoImage
import random
import pygame
from PIL import Image, ImageTk

# --- Ses ve Müzik Başlat ---
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)  # Sonsuz döngü

# Ses efektleri
clap_sound = pygame.mixer.Sound("assets/clap.wav")
sad_sound = pygame.mixer.Sound("assets/sad.wav")

# Global değişkenler
user_score = 0
cpu_score = 0
total_rounds = 0
max_score = 3

def reset_game():
    global user_score, cpu_score, total_rounds
    user_score = 0
    cpu_score = 0
    total_rounds = 0
    score_label.config(text="Skor • Sen: 0  Bilgisayar: 0")
    result_label.config(text="")
    stats_label.config(text="Toplam Oynanan Tur: 0")
    user_label.config(image=question_img)
    cpu_label.config(image=question_img)
    for btn in choice_buttons:
        btn.config(state="normal")

# Kazanma kontrolü
def determine_winner(user, cpu):
    if user == cpu:
        return "Beraber"
    elif (user == "Taş" and cpu == "Makas") or \
         (user == "Kağıt" and cpu == "Taş") or \
         (user == "Makas" and cpu == "Kağıt"):
        return "Kullanıcı"
    else:
        return "Bilgisayar"

# Oyun oynama
def play(user_choice):
    global user_score, cpu_score, total_rounds

    cpu_choice = random.choice(["Taş", "Kağıt", "Makas"])
    total_rounds += 1
    stats_label.config(text=f"Toplam Oynanan Tur: {total_rounds}")

    # Görsel güncelle
    user_label.config(image=images[user_choice])
    cpu_label.config(image=images[cpu_choice])

    result = determine_winner(user_choice, cpu_choice)

    if result == "Kullanıcı":
        user_score += 1
        result_label.config(text="✔️ Sen kazandın!", fg="green")
    elif result == "Bilgisayar":
        cpu_score += 1
        result_label.config(text="❌ Bilgisayar kazandı!", fg="red")
    else:
        result_label.config(text="🤝 Berabere!", fg="gray")

    score_label.config(text=f"Skor • Sen: {user_score}  Bilgisayar: {cpu_score}")

    if user_score == max_score:
        clap_sound.play()
        show_konfeti("🏆 TEBRİKLER! Oyunu Sen Kazandın!")
    elif cpu_score == max_score:
        sad_sound.play()
        show_konfeti("💀 Bilgisayar Kazandı!")

def show_konfeti(message):
    for btn in choice_buttons:
        btn.config(state="disabled")
    messagebox.showinfo("Oyun Bitti", message)

# --- Pencere ---
root = tk.Tk()
root.title("Taş Kağıt Makas - Ferdi Deluxe Edition 🎮")
root.geometry("400x700")
root.config(bg="#eaf4fc")

# --- Görseller ---
images = {
    "Taş": PhotoImage(file="assets/tas.png"),
    "Kağıt": PhotoImage(file="assets/kagit.png"),
    "Makas": PhotoImage(file="assets/makas.png")
}
question_img = PhotoImage(file="assets/question.png")

# --- Başlık ---
title = tk.Label(root, text="Taş - Kağıt - Makas", font=("Helvetica", 22, "bold"), bg="#eaf4fc")
title.pack(pady=10)

score_label = tk.Label(root, text="Skor • Sen: 0  Bilgisayar: 0", font=("Helvetica", 14), bg="#eaf4fc")
score_label.pack()

stats_label = tk.Label(root, text="Toplam Oynanan Tur: 0", font=("Helvetica", 12), bg="#eaf4fc")
stats_label.pack(pady=5)

# --- Seçim Görselleri ---
user_label = tk.Label(root, image=question_img, bg="#eaf4fc")
cpu_label = tk.Label(root, image=question_img, bg="#eaf4fc")
user_label.pack(pady=5)
cpu_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), bg="#eaf4fc")
result_label.pack(pady=10)

# --- Seçim Butonları ---
button_frame = tk.Frame(root, bg="#eaf4fc")
button_frame.pack(pady=10)

choice_buttons = []
for choice in ["Taş", "Kağıt", "Makas"]:
    btn = tk.Button(button_frame, image=images[choice], command=lambda ch=choice: play(ch))
    btn.pack(side="left", padx=10)
    choice_buttons.append(btn)

# --- Yeni Oyun ---
reset_button = tk.Button(root, text="🔁 Yeni Oyun", font=("Helvetica", 12), command=reset_game)
reset_button.pack(pady=20)

# --- Başlat ---
root.mainloop()
