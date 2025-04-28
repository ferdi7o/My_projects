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
from kivy.animation import Animation
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
        self.game_over = False
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

        # Ayarlar (Settings) butonu
        self.settings_btn = Button(background_normal="assets/settings.png", size_hint=(None, None), size=(100, 100),
                                   pos_hint={"right": 0.98, "top": 0.98}, on_press=self.open_settings)
        self.add_widget(self.settings_btn)

        # Kazanma/Kaybetme/Beraberlik yazısı
        self.result_label = Label(
            text="",
            font_size='24sp',
            color=(1, 1, 1, 1),  # Başlangıçta görünmez gibi beyaz
            bold=True,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.52}
        )
        self.add_widget(self.result_label)

    def show_game_over_popup(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        if self.player_score == 5:
            result_text = "Tebrikler! Kazandın! 🎉"
            image_source = "assets/trophy.png"
        else:
            result_text = "Üzgünüm! Kaybettin! 😢"
            image_source = "assets/sad.png"

        img = Image(source=image_source, size_hint=(1, 0.7), allow_stretch=True, keep_ratio=True)
        label = Label(text=result_text, halign="center", font_size='24sp', size_hint=(1, 0.3))

        layout.add_widget(img)
        layout.add_widget(label)

        popup = Popup(title="Oyun Bitti", content=layout, size_hint=(1, 0.9), auto_dismiss=True)
        popup.open()

    def show_result(self, text, color):
        self.result_label.text = text
        self.result_label.color = color
        self.result_label.font_size = 36  # Başlangıç boyutunu büyüttüm (24 yerine 36)

        anim = (
                Animation(font_size=64, duration=0.3, t='out_quad') +  # büyürken daha büyük
                Animation(font_size=64, duration=0.2, t='out_quad')  # küçülürken yine büyük kalsın
        )
        anim.start(self.result_label)

    def open_settings(self, instance):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Müzik Aç/Kapa Switch
        music_btn = Button(
            text="Müzik: Açık" if not self.is_muted else "Müzik: Kapalı",
            size_hint=(1, None),
            height=50
        )
        music_btn.bind(on_press=self.toggle_music)

        # Ses Seviyesi Slider
        from kivy.uix.slider import Slider
        volume_slider = Slider(min=0, max=1, value=self.sounds["music"].volume if self.sounds["music"] else 0.5)
        volume_slider.bind(value=self.set_volume)

        # Gece Modu (Tema değişimi) Buton
        theme_btn = Button(
            text="Gece Moduna Geç",
            size_hint=(1, None),
            height=50
        )
        theme_btn.bind(on_press=self.toggle_theme)

        layout.add_widget(music_btn)
        layout.add_widget(Label(text="Ses Seviyesi"))
        layout.add_widget(volume_slider)
        layout.add_widget(theme_btn)

        self.settings_popup = Popup(title="Ayarlar", content=layout, size_hint=(0.9, 0.8))
        self.settings_popup.open()

    def toggle_music(self, instance):
        self.is_muted = not self.is_muted
        if self.sounds["music"]:
            if self.is_muted:
                self.sounds["music"].stop()
                instance.text = "Müzik: Kapalı"
            else:
                self.sounds["music"].play()
                instance.text = "Müzik: Açık"

    def set_volume(self, instance, value):
        if self.sounds["music"]:
            self.sounds["music"].volume = value

    def toggle_theme(self, instance):
        if self.bg.source == "assets/background.png":
            self.bg.source = "assets/dark_background.png"  # Gece modu arka planı (sen hazırlarsan)
            instance.text = "Gündüz Moduna Geç"
        else:
            self.bg.source = "assets/background.png"
            instance.text = "Gece Moduna Geç"

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
        if self.game_over:
            self.show_game_over_popup()
            return

        self.play_sound("touch")
        computer = choice(self.choices)
        self.update_round(choice_str, computer)

    def update_round(self, player, computer):
        self.total_rounds += 1
        self.round_label.text = f"Round: {self.total_rounds}"

        self.player_image.source = f"assets/{player}.png"
        self.computer_image.source = f"assets/{computer}.png"

        # Önce sonucu göster
        if player == computer:
            self.show_result("Draw", (1, 1, 0, 1))  # Sarı renk
        elif (player == "rock" and computer == "scissors") or \
                (player == "paper" and computer == "rock") or \
                (player == "scissors" and computer == "paper"):
            self.player_score += 1
            self.player_label.text = f"YOU\n{self.player_score}"
            self.show_result("You Win", (0, 1, 0, 1))  # Yeşil renk
        else:
            self.computer_score += 1
            self.computer_label.text = f"COMPUTER\n{self.computer_score}"
            self.show_result("You Lose", (1, 0, 0, 1))  # Kırmızı renk

        self.check_game_end()

    def check_game_end(self):
        if self.player_score == 5 or self.computer_score == 5:
            self.game_over = True  # <-- oyun bittiğini işaretle
            if self.player_score == 5:
                self.play_sound("win")
            else:
                self.play_sound("lose")
            self.show_popup("Oyun Bitti", "Yeni bir oyun başlatabilirsiniz.")

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.total_rounds = 0
        self.result_label.text = ""
        self.game_over = False
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
