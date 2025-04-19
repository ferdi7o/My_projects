import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame

# Pygame for sound
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # Loop music

win_sound = pygame.mixer.Sound("clap.wav")
lose_sound = pygame.mixer.Sound("sad.wav")

def play_win_sound():
    win_sound.play()

def play_lose_sound():
    lose_sound.play()

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
bg_image = Image.open("background_gradient.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Top mute button
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
title = tk.Label(root, text="ROCK PAPER SCISSORS", font=("Helvetica", 18, "bold"), bg="white")
title.pack(pady=(50, 10))

# Images
choices = ["rock", "paper", "scissors"]
image_dict = {
    "rock": ImageTk.PhotoImage(Image.open("tas.png").resize((80, 80))),
    "paper": ImageTk.PhotoImage(Image.open("kagit.png").resize((80, 80))),
    "scissors": ImageTk.PhotoImage(Image.open("makas.png").resize((80, 80))),
    "question": ImageTk.PhotoImage(Image.open("question.png").resize((80, 80)))
}

# === SCORE AND IMAGE AREA ===
center_frame = tk.Frame(root, bg="white")
center_frame.pack(pady=10)

# Scores (You / Computer)
score_frame = tk.Frame(center_frame, bg="white")
score_frame.pack(pady=10)

you_score_frame = tk.Label(score_frame, text="YOU\n0", font=("Arial", 16, "bold"), bg="#00CED1", fg="white", width=10, height=3)
you_score_frame.grid(row=0, column=0, padx=20)

comp_score_frame = tk.Label(score_frame, text="COMPUTER\n0", font=("Arial", 16, "bold"), bg="#9370DB", fg="white", width=10, height=3)
comp_score_frame.grid(row=0, column=1, padx=20)

# Player & Computer Images
images_frame = tk.Frame(center_frame, bg="white")
images_frame.pack(pady=10)

player_img_label = tk.Label(images_frame, image=image_dict["question"])
player_img_label.grid(row=0, column=0, padx=40)

computer_img_label = tk.Label(images_frame, image=image_dict["question"])
computer_img_label.grid(row=0, column=1, padx=40)

# Round counter
round_label = tk.Label(root, text="Round: 0", font=("Arial", 12), bg="white")
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
        play_win_sound()
    else:
        computer_score += 1
        comp_score_frame.config(text=f"COMPUTER\n{computer_score}")
        play_lose_sound()

    check_game_end()

def check_game_end():
    if player_score == 3 or computer_score == 3:
        winner = "You win! 🎉" if player_score == 3 else "Computer wins! 😢"
        messagebox.showinfo("Game Over", winner)
        reset_game()

def player_choice(choice):
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

# Choice buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

rock_btn = tk.Button(button_frame, image=image_dict["rock"], command=lambda: player_choice("rock"))
rock_btn.grid(row=0, column=0, padx=10)

paper_btn = tk.Button(button_frame, image=image_dict["paper"], command=lambda: player_choice("paper"))
paper_btn.grid(row=0, column=1, padx=10)

scissors_btn = tk.Button(button_frame, image=image_dict["scissors"], command=lambda: player_choice("scissors"))
scissors_btn.grid(row=0, column=2, padx=10)

# New Game & Exit buttons
bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack(pady=15)

tk.Button(bottom_frame, text="New Game", command=reset_game, font=("Arial", 12), bg="#FF69B4").grid(row=0, column=0, padx=10)
tk.Button(bottom_frame, text="Çıkış", command=root.quit, font=("Arial", 12), bg="gray").grid(row=0, column=1, padx=10)

root.mainloop()
