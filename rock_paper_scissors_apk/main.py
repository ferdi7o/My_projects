from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from random import choice
import sys

# Window.size = (360, 640)  # KALDIRILDI: Mobilde sabit boyut verme!

class RPSGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_score = 0
        self.computer_score = 0
        self.total_rounds = 0
        self.is_muted = False
        self.choices = ["rock", "paper", "scissors"]

        self.sounds = {
            "music": SoundLoader.load("assets/music.mp3"),
            "win": SoundLoader.load("assets/clap.wav"),
            "lose": SoundLoader.load("assets/sad.wav"),
            "touch": SoundLoader.load("assets/touch.wav")
        }

        if self.sounds["music"]:
            self.sounds["music"].loop = True
            self.sounds["music"].volume = 0.3
            self.sounds["music"].play()

        # Arka plan
        self.bg = Image(source="assets/background.png", allow_stretch=True, keep_ratio=False,
                        size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        self.add_widget(self.bg)

        # Mute butonu
        self.mute_btn = Button(
            background_normal="assets/unmute.png",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"x": 0.02, "top": 0.98},
            on_press=self.toggle_mute
        )

        self.add_widget(self.mute_btn)

        # Başlık
        self.title = Label(text="ROCK PAPER SCISSORS", font_size='20sp', size_hint=(1, None), height=40,
                           pos_hint={"top": 0.9}, halign="center")
        self.add_widget(self.title)

        # Skorlar
        self.player_label = Label(text="YOU\n0", font_size='18sp', size_hint=(.3, .1),
                                  pos_hint={"x": 0.05, "top": 0.75})
        self.computer_label = Label(text="COMPUTER\n0", font_size='18sp', size_hint=(.3, .1),
                                    pos_hint={"right": 0.95, "top": 0.75})
        self.add_widget(self.player_label)
        self.add_widget(self.computer_label)

        # Seçim ikonları
        self.player_image = Image(source="assets/question.png", size_hint=(.25, .15),
                                  pos_hint={"x": 0.1, "top": 0.6})
        self.computer_image = Image(source="assets/question.png", size_hint=(.25, .15),
                                    pos_hint={"right": 0.9, "top": 0.6})
        self.add_widget(self.player_image)
        self.add_widget(self.computer_image)

        # Round sayacı
        self.round_label = Label(text="Round: 0", font_size='14sp', size_hint=(None, None), height=30,
                                 pos_hint={"center_x": 0.5, "top": 0.48})
        self.add_widget(self.round_label)

        # Oyun butonları
        self.rock_btn = Button(background_normal="assets/rock.png", size_hint=(.25, .15),
                               pos_hint={"x": 0.05, "top": 0.38})
        self.paper_btn = Button(background_normal="assets/paper.png", size_hint=(.25, .15),
                                pos_hint={"center_x": 0.5, "top": 0.38})
        self.scissors_btn = Button(background_normal="assets/scissors.png", size_hint=(.25, .15),
                                   pos_hint={"right": 0.95, "top": 0.38})

        self.rock_btn.bind(on_press=lambda x: self.player_choice("rock"))
        self.paper_btn.bind(on_press=lambda x: self.player_choice("paper"))
        self.scissors_btn.bind(on_press=lambda x: self.player_choice("scissors"))

        self.add_widget(self.rock_btn)
        self.add_widget(self.paper_btn)
        self.add_widget(self.scissors_btn)

        # Yeni Oyun ve Çıkış Butonları
        self.reset_btn = Button(
            text="Yeni Oyun",
            size_hint=(.4, None),
            height=70,  # 40 yerine 70 yaptık
            font_size='20sp',  # Yazı boyutu büyüdü
            background_color=(0.2, 0.6, 0.8, 1),
            pos_hint={"x": 0.05, "y": 0.02}
        )

        self.exit_btn = Button(
            text="Çıkış",
            size_hint=(.4, None),
            height=70,  # 40 yerine 70 yaptık
            font_size='20sp',
            background_color=(1, 0.3, 0.3, 1),
            pos_hint={"right": 0.95, "y": 0.02}
        )

        self.reset_btn.bind(on_press=lambda x: self.reset_game())
        self.exit_btn.bind(on_press=lambda x: sys.exit())

        self.add_widget(self.reset_btn)
        self.add_widget(self.exit_btn)

    def toggle_mute(self, instance):
        if self.sounds["music"]:
            self.is_muted = not self.is_muted
            new_icon = "assets/mute.png" if self.is_muted else "assets/unmute.png"
            self.mute_btn.background_normal = new_icon
            self.sounds["music"].volume = 0 if self.is_muted else 0.3

    def play_sound(self, key):
        if not self.is_muted and self.sounds[key]:
            self.sounds[key].play()

    def player_choice(self, choice_str):
        self.play_sound("touch")
        computer = choice(self.choices)
        self.update_round(choice_str, computer)

    def update_round(self, player, computer):
        self.total_rounds += 1
        self.round_label.text = f"Round: {self.total_rounds}"

        self.player_image.source = f"assets/{player}.png"
        self.computer_image.source = f"assets/{computer}.png"

        if player == computer:
            return
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            self.player_score += 1
            self.player_label.text = f"YOU\n{self.player_score}"
        else:
            self.computer_score += 1
            self.computer_label.text = f"COMPUTER\n{self.computer_score}"

        self.check_game_end()

    def check_game_end(self):
        if self.player_score == 5 or self.computer_score == 5:
            if self.player_score == 5:
                self.play_sound("win")
            else:
                self.play_sound("lose")
            self.show_popup("Oyun Bitti", "Yeni bir oyun başlatabilirsiniz.")

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.total_rounds = 0
        self.player_label.text = "YOU\n0"
        self.computer_label.text = "COMPUTER\n0"
        self.round_label.text = "Round: 0"
        self.player_image.source = "assets/question.png"
        self.computer_image.source = "assets/question.png"

    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=message)
        btn = Button(text="Tamam", size_hint_y=None, height=40)
        layout.add_widget(label)
        layout.add_widget(btn)
        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(300, 200))
        btn.bind(on_press=popup.dismiss)
        popup.open()

class RPSApp(App):
    def build(self):
        return RPSGame()

if __name__ == "__main__":
    RPSApp().run()
