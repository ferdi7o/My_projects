import tkinter as tk
import random

# Başlangıç skorları
user_score = 0
cpu_score = 0

# Seçenekler
choices = ["Taş", "Kağıt", "Makas"]
emoji_map = {
    "Taş": "🪨",
    "Kağıt": "📄",
    "Makas": "✂️"
}

# Kazanma durumu
def determine_winner(user, cpu):
    if user == cpu:
        return "Beraber!"
    elif (user == "Taş" and cpu == "Makas") or \
         (user == "Kağıt" and cpu == "Taş") or \
         (user == "Makas" and cpu == "Kağıt"):
        return "Kullanıcı"
    else:
        return "Bilgisayar"

# Tıklama işlemi
def play(user_choice):
    global user_score, cpu_score

    cpu_choice = random.choice(choices)
    result = determine_winner(user_choice, cpu_choice)

    user_label.config(text=f"Sen: {emoji_map[user_choice]} ({user_choice})")
    cpu_label.config(text=f"Bilgisayar: {emoji_map[cpu_choice]} ({cpu_choice})")

    if result == "Kullanıcı":
        user_score += 1
        result_label.config(text="✔️ Sen kazandın!", fg="green")
    elif result == "Bilgisayar":
        cpu_score += 1
        result_label.config(text="❌ Bilgisayar kazandı!", fg="red")
    else:
        result_label.config(text="🤝 Berabere!", fg="gray")

    score_label.config(text=f"Skor • Sen: {user_score}  Bilgisayar: {cpu_score}")

    # 3 olan kazanır
    if user_score == 5:
        result_label.config(text="🏆 SEN KAZANDIN OYUNU!", fg="green")
        disable_buttons()
    elif cpu_score == 5:
        result_label.config(text="💀 Bilgisayar kazandı oyunu!", fg="red")
        disable_buttons()

def disable_buttons():
    for button in choice_buttons:
        button.config(state="disabled")

# Arayüz oluştur
root = tk.Tk()
root.title("Taş Kağıt Makas - Ferdi Edition 🎮")
root.geometry("500x400")
root.config(bg="#f0f0f0")

# Başlık
title = tk.Label(root, text="🎮 Taş - Kağıt - Makas", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# Skor
score_label = tk.Label(root, text="Skor • Sen: 0  Bilgisayar: 0", font=("Helvetica", 14), bg="#f0f0f0")
score_label.pack()

# Seçimler
user_label = tk.Label(root, text="Sen: -", font=("Helvetica", 16), bg="#f0f0f0")
cpu_label = tk.Label(root, text="Bilgisayar: -", font=("Helvetica", 16), bg="#f0f0f0")
user_label.pack(pady=5)
cpu_label.pack(pady=5)

# Sonuç
result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
result_label.pack(pady=10)

# Seçim butonları
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

choice_buttons = []
for choice in choices:
    btn = tk.Button(button_frame, text=emoji_map[choice], font=("Helvetica", 30), width=4,
                    command=lambda ch=choice: play(ch))
    btn.pack(side="left", padx=15)
    choice_buttons.append(btn)

# Uygulamayı başlat
root.mainloop()
