import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame

# Pygame for sound
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

win_sound = pygame.mixer.Sound("assets/clap.wav")
lose_sound = pygame.mixer.Sound("assets/sad.wav")
touch_sound = pygame.mixer.Sound("assets/touch.wav")



def play_win_sound():
    win_sound.play()

def play_lose_sound():
    lose_sound.play()

def play_touch_sound():
    if not is_muted:
        touch_sound.play()


# Globals
player_score = 0
computer_score = 0
total_rounds = 0
is_muted = False

# Main window
root = tk.Tk()
root.title("Taş Kağıt Makas - Ferdi Gradient Edition")
root.geometry("360x640")
root.resizable(False, False)

# Background image
bg_image = Image.open("assets/background_gradient.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Mute Button
def toggle_mute():
    global is_muted
    if is_muted:
        pygame.mixer.music.unpause()
        mute_btn.config(text="🔊")
    else:
        pygame.mixer.music.pause()
        mute_btn.config(text="🔇")
    is_muted = not is_muted

mute_btn = tk.Button(root, text="🔊", font=("Arial", 12), command=toggle_mute, bg="white")
mute_btn.place(x=10, y=10)

# Title
title = tk.Label(root, text="ROCK PAPER SCISSORS", font=("Helvetica", 18, "bold"), bg="#ffffff")
title.pack(pady=(50, 10))

# Score Frame
score_frame = tk.Frame(root, bg="white")
score_frame.pack(pady=10)

you_score_frame = tk.Label(score_frame, text="YOU\n0", font=("Arial", 16, "bold"), bg="#00CED1", fg="white", width=10, height=3)
you_score_frame.grid(row=0, column=0, padx=20)

comp_score_frame = tk.Label(score_frame, text="COMPUTER\n0", font=("Arial", 16, "bold"), bg="#9370DB", fg="white", width=10, height=3)
comp_score_frame.grid(row=0, column=1, padx=20)

# Images
choices = ["rock", "paper", "scissors"]
image_dict = {
    "rock": ImageTk.PhotoImage(Image.open("assets/tas.png").resize((80, 80))),
    "paper": ImageTk.PhotoImage(Image.open("assets/kagit.png").resize((80, 80))),
    "scissors": ImageTk.PhotoImage(Image.open("assets/makas.png").resize((80, 80))),
    "question": ImageTk.PhotoImage(Image.open("assets/question.png").resize((80, 80)))
}

# Player & Computer Choice Display
image_frame = tk.Frame(root, bg="white")
image_frame.pack(pady=10)

player_img_label = tk.Label(image_frame, image=image_dict["question"], bg="white")
player_img_label.grid(row=0, column=0, padx=20)

computer_img_label = tk.Label(image_frame, image=image_dict["question"], bg="white")
computer_img_label.grid(row=0, column=1, padx=20)

# Round counter
round_label = tk.Label(root, text="Round: 0", font=("Arial", 12), bg="#ffffff")
round_label.pack(pady=10)

# Game Logic
def determine_winner(player, computer):
    global player_score, computer_score, total_rounds
    total_rounds += 1
    round_label.config(text=f"Round: {total_rounds}")

    player_img_label.config(image=image_dict[player])
    computer_img_label.config(image=image_dict[computer])

    if player == computer:
        return
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        player_score += 1
        you_score_frame.config(text=f"YOU\n{player_score}")
    else:
        computer_score += 1
        comp_score_frame.config(text=f"COMPUTER\n{computer_score}")

    check_game_end()

def check_game_end():
    if player_score == 5 or computer_score == 5:
        winner = "You win! 🎉" if player_score == 5 else "Computer wins! 😢"
        messagebox.showinfo("Game Over", winner)
        if player_score == 5:
            play_win_sound()
        else:
            play_lose_sound()
        reset_game()

def player_choice(choice):
    play_touch_sound()
    computer = random.choice(choices)
    determine_winner(choice, computer)

def reset_game():
    global player_score, computer_score, total_rounds
    player_score = 0
    computer_score = 0
    total_rounds = 0
    you_score_frame.config(text="YOU\n0")
    comp_score_frame.config(text="COMPUTER\n0")
    round_label.config(text="Round: 0")
    player_img_label.config(image=image_dict["question"])
    computer_img_label.config(image=image_dict["question"])

# Choice Buttons
button_frame = tk.Frame(root, bg="#462E9D")  # Aynı mor ton
button_frame.pack(pady=10)

rock_btn = tk.Button(button_frame, image=image_dict["rock"], command=lambda: player_choice("rock"), borderwidth=0)
rock_btn.grid(row=0, column=0, padx=10)

paper_btn = tk.Button(button_frame, image=image_dict["paper"], command=lambda: player_choice("paper"), borderwidth=0)
paper_btn.grid(row=0, column=1, padx=10)

scissors_btn = tk.Button(button_frame, image=image_dict["scissors"], command=lambda: player_choice("scissors"), borderwidth=0)
scissors_btn.grid(row=0, column=2, padx=10)

# New Game & Exit
bottom_frame = tk.Frame(root, bg="#462E9D")  # Arka planla uyumlu
bottom_frame.pack(pady=15)

tk.Button(bottom_frame, text="New Game", command=reset_game, font=("Arial", 12), bg="#FF69B4", fg="black", borderwidth=0).grid(row=0, column=0, padx=10)
tk.Button(bottom_frame, text="Çıkış", command=root.quit, font=("Arial", 12), bg="gray", fg="white", borderwidth=0).grid(row=0, column=1, padx=10)

root.mainloop()
