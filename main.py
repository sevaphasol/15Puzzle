import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget, QFileDialog
from PyQt5.Qt import QParallelAnimationGroup, QStatusBar, QFont
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
import sqlite3

from MainScreen import Ui_MainWindow_Play
from SettingsScreen import Ui_MainWindow_Settings
from StartScreen import Ui_MainWindow_Start

from time import sleep, time
from random import shuffle, randint
from os import path


class StartScreen(QMainWindow, Ui_MainWindow_Start):
    def __init__(self, app_, main_window):
        super().__init__()
        self.initUI(app_, main_window)

    def initUI(self, app_, main_window):
        self.setupUi(self)
        self.app = app_
        self.new_game_btn.clicked.connect(self.new_game)
        self.resume_game_btn.clicked.connect(self.resume_game)
        self.settings_btn.clicked.connect(self.open_settings)
        self.main_window = main_window
        self.refresh_language()
        self.label_gif1.setStyleSheet("image: url(images/other_images/left.png);"
                                      "border-radius: 10 px;")
        self.label_gif2.setStyleSheet("image: url(images/other_images/right.png);"
                                      "border-radius: 10 px;")

    def new_game(self):
        btn = self.new_game_btn
        if self.sender() == btn:
            if self.main_window.volume_is_on:
                self.main_window.sound_buttons.play()
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/new_game_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
            sleep(0.1)
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/new_game_not_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
        self.main_window.need_to_clear = True
        self.main_window.con = sqlite3.connect("my_game.sqlite3")
        self.main_window.cur = self.main_window.con.cursor()
        self.main_window.cur.execute("""
                DELETE FROM score
                """)
        self.main_window.con.commit()
        self.main_window.cur.execute("""
                        CREATE TABLE IF NOT EXISTS score
                        ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [time] INTEGER, [steps] INTEGER)
                        """)
        self.main_window.con.commit()
        self.main_window.update_time_table(False)
        windows.setCurrentIndex(1)

    def resume_game(self):
        btn = self.resume_game_btn
        if self.sender() == btn:
            if self.main_window.volume_is_on:
                self.main_window.sound_buttons.play()
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/resume_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
            sleep(0.1)
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/resume_not_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
        self.main_window.need_to_clear = False
        file_path = QFileDialog.getOpenFileName(
            self, 'Выбрать игру', '',
            'БД (*.sqlite3)')[0]
        my_game_path = ''
        backslash = r"\ "
        for i in path.abspath("my_game.sqlite3"):
            if i == backslash[0]:
                i = "/"
            my_game_path += i
        if file_path == my_game_path:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Warning)
            if self.main_window.language == "us":
                warning.setWindowTitle("Error")
            elif self.main_window.language == "ru":
                warning.setWindowTitle("Ошибка")
            ok = warning.addButton(QMessageBox.Ok)
            ok.setFont(QFont("Comic Sans MS", 10))
            ok.setStyleSheet("background-color: rgb(210, 217, 255);")
            ok.clicked.connect(self.main_window.sound)
            warning.setStyleSheet("background-color: rgb(149, 181, 255);")
            warning.setFont(QFont("Comic Sans MS", 10))
            if self.main_window.language == "us":
                warning.setText(self.main_window.warnings[0])
            if self.main_window.language == "ru":
                warning.setText(self.main_window.warnings[1])
            warning.exec_()
        elif len(file_path) != 0:
            self.main_window.opened_con = sqlite3.connect(file_path)
            self.main_window.con = sqlite3.connect("my_game.sqlite3")
            self.main_window.opened_con.backup(target=self.main_window.con)
            self.main_window.cur = self.main_window.con.cursor()
            self.main_window.opened_cur = self.main_window.opened_con.cursor()
            self.main_window.update_time_table(False)
            windows.setCurrentIndex(1)

    def open_settings(self):
        btn = self.settings_btn
        if self.sender() == btn:
            if self.main_window.volume_is_on:
                self.main_window.sound_buttons.play()
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/settings_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
            sleep(0.1)
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/settings_not_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
        self.main_window.previousIndex = 0
        windows.setCurrentIndex(2)

    def refresh_language(self):
        self.new_game_btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}"
                                        f"/new_game_not_pushed.png);"
                                        "border-radius: 10 px;")
        self.resume_game_btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}"
                                           f"/resume_not_pushed.png);"
                                           "border-radius: 10 px;")
        self.settings_btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/"
                                        f"settings_not_pushed.png);"
                                        "border-radius: 10 px;")
        if self.main_window.language == "us":
            self.heading_label.setText("15Puzzle")
        elif self.main_window.language == "ru":
            self.heading_label.setText("Пятнашки")


class PlayScreen(QMainWindow, Ui_MainWindow_Play):
    def __init__(self, app_):
        super().__init__()
        self.initUI(app_)

    def initUI(self, app_):
        self.setupUi(self)
        self.app = app_
        self.language = "us"
        self.cheats_on = False
        self.need_to_clear = True
        self.previousIndex = 0
        self.info = QMessageBox()
        self.ok = self.info.addButton(QMessageBox.Ok)
        self.ok.setFont(QFont("Comic Sans MS", 10))
        self.ok.setStyleSheet("background-color: rgb(210, 217, 255);")
        self.ok.clicked.connect(self.sound)
        self.info.setStyleSheet("background-color: rgb(149, 181, 255);")
        self.info.setFont(QFont("Comic Sans MS", 10))
        self.info.setWindowIcon(QIcon("images/icons/question_icon.png"))
        self.tips = ["Нажмите на пятнашку(кнопку с цифрой), чтобы походить.\n"
                     "Ходить можно если рядом либо на одной вертикали или горизонтали с пятнашкой"
                     " есть свободное поле.\n"
                     "Вы выигрываите если пятнашки расставлены по порядку от одного до пятнадцати.\n"
                     "Слева от поля расположено табло с результатами прохождения(время прохождения).\n"
                     "Ниже него показано количество шагов, которые Вы сделали за игру.\n"
                     "Над игровым полем расположен таймер, отображающий время прохождения текущей игры.\n"
                     "Его можно остановить кнопками стар и стоп, расположенными слева от таймера.\n"
                     "При остановленном таймере ходить нельзя.\n"
                     "Под игровым полем расположен прогресс вашего прохождения.\n"
                     "Кнопка новая игра обновляет результаты всех прохождений и расставляет пятнашки по порядку.\n"
                     "Кнопка старт/рестарт перемешивает поле.\n"
                     "С помощью кнопки звук Вы можете включить или выключить звук.\n"
                     "Кнопка настройки перенаправляет вас в настройки, где Вы можете установить различные параметры.\n"
                     "Приятной игры!",
                     "Click on the play button (number button) to do a move.\n"
                     "You can move if there is a free field next to either"
                     " on the same vertical or horizontal line with the clicked button.\n"
                     "You win if the buttons are arranged in order from one to fifteen.\n"
                     "To the left of the field there is a scoreboard with the passage results (passage time).\n"
                     "Below it shows the number of steps that you took during the game.\n"
                     "Above the playing field, there is a timer that displays the time of the current game.\n"
                     "It can be stopped by using the start and stop buttons located to the left of the timer.\n"
                     "When the timer is stopped, you cannot do a move.\n"
                     "Below the playing field is the progress of your passage.\n"
                     "The new game button updates the results of all passages and puts the play buttons in order.\n"
                     "The start / restart button shuffles the field.\n"
                     "With the sound button you can turn the sound on or off.\n"
                     "The settings button redirects you to the settings where you can set various parameters.\n"
                     "Good luck have fun!"]
        self.warnings = ["Try another name", "Попробуйте другое имя"]

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.clearMessage()
        self.statusBar.setFont(QFont("Comic Sans MS", 10))

        self.animation_back_move_btn = False

        # устанавливаем звук
        self.sound_play_buttons = QSound("sounds/play_button_sound.wav")
        self.sound_buttons = QSound("sounds/button_sound.wav")
        self.win_sound = QSound("sounds/win_sound.wav")

        self.won = False
        self.you_win_label.hide()  # покажется когда игрок выиграет

        self.speeds_of_play_buttons = {10: 0, 9: 100, 8: 200, 7: 300, 6: 400, 5: 500, 4: 600, 3: 700, 2: 800, 1: 1000}
        self.speed_of_play_buttons = 8

        self.count_of_steps = 0

        self.moves = []

        self.timer = QTimer()  # создаем таймер
        self.start_time = time()
        self.times = []
        self.timer_is_started = False
        self.stop_timer_time = 0
        self.start_timer_time = 0
        self.intervals_of_stopping = []
        # сюда будут записываться время, которое прошло с момента остановки таймера
        # до начала таймера, потом все будет суммироваться и вычитаться из общего времени

        self.game_is_started = False
        self.field = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
                      self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty]  # создаем поле
        self.empty.hide()  # пустое поле невидимое
        self.field_values = {self.l1: 1,
                             self.l2: 2,
                             self.l3: 3,
                             self.l4: 4,
                             self.l5: 5,
                             self.l6: 6,
                             self.l7: 7,
                             self.l8: 8,
                             self.l9: 9,
                             self.l10: 10,
                             self.l11: 11,
                             self.l12: 12,
                             self.l13: 13,
                             self.l14: 14,
                             self.l15: 15,
                             self.empty: 0
                             }  # номер каждой кнопки, понадобится для правильного перемешивания
        self.positions = [(i.x(), i.y()) for i in self.field]  # координаты игровых кнопок

        for i in range(len(self.field) - 1):
            # ставим на игровые кнопки картинки
            self.field[i].setStyleSheet(f"image: url(images/play_buttons/{i + 1}/{randint(1, 3)}.png);"
                                        "background-color: Transparent;")
            self.field[i].clicked.connect(self.my_move)

        self.new_game_btn.clicked.connect(self.new_game)
        self.restart_btn.clicked.connect(self.restart)
        self.volume_is_on = True  # звук при входе включен
        self.volume_btn.clicked.connect(self.volume)
        self.settings_btn.clicked.connect(self.settings)
        self.start_timer_btn.clicked.connect(self.start_timer)
        self.stop_timer_btn.clicked.connect(self.stop_timer)
        self.tips_btn.clicked.connect(self.show_dialog)
        self.back_move_btn.clicked.connect(self.back_move)
        self.back_menu_btn.clicked.connect(self.back_menu)
        self.save_action.triggered.connect(self.save)

        self.refresh_language()

    def closeEvent(self, event):
        if self.need_to_clear:
            self.clear_bd()
            self.con.close()
        event.accept()

    def refresh_language(self):
        # картинки для каждой кнопки на первом месте если она нажата на втором если не нажата
        # для рестарта и звука есть два положения для рестарта старт и рестарт для звук включен и выключен
        # для каждого положения свои картинки
        self.images = {self.new_game_btn: (f"images/buttons_{self.language}/new_game_pushed.png",
                                           f"images/buttons_{self.language}/new_game_not_pushed.png"),
                       self.restart_btn: {"start": (f"images/buttons_{self.language}/start_pushed.png",
                                                    f"images/buttons_{self.language}/restart_not_pushed.png"),
                                          "restart": (f"images/buttons_{self.language}/restart_pushed.png",
                                                      f"images/buttons_{self.language}/restart_not_pushed.png")},
                       self.volume_btn: {"on": (f"images/buttons_{self.language}/volume_on_pushed.png",
                                                f"images/buttons_{self.language}/volume_off_not_pushed.png"),
                                         "off": (f"images/buttons_{self.language}/volume_off_pushed.png",
                                                 f"images/buttons_{self.language}/volume_on_not_pushed.png")},
                       self.settings_btn: (f"images/buttons_{self.language}/settings_pushed.png",
                                           f"images/buttons_{self.language}/settings_not_pushed.png"),
                       self.start_timer_btn: (f"images/buttons_{self.language}/start_timer_pushed.png",
                                              f"images/buttons_{self.language}/start_timer_not_pushed.png"),
                       self.stop_timer_btn: (f"images/buttons_{self.language}/stop_timer_pushed.png",
                                             f"images/buttons_{self.language}/stop_timer_not_pushed.png"),
                       self.tips_btn: (f"images/buttons_{self.language}/tips_pushed.png",
                                       f"images/buttons_{self.language}/tips_not_pushed.png"),
                       self.back_move_btn: (f"images/buttons_{self.language}/back_move_pushed.png",
                                            f"images/buttons_{self.language}/back_move_not_pushed.png"),
                       self.back_menu_btn: (f"images/buttons_{self.language}/back_pushed.png",
                                            f"images/buttons_{self.language}/back_not_pushed.png"),
                       }

        # ставим картинки на кнопки
        self.new_game_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/new_game_not_pushed.png);"
                                        "border-radius: 10 px;")
        if not self.game_is_started:
            self.restart_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/start_not_pushed.png);"
                                           "border-radius: 10 px;")
        else:
            self.restart_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/"
                                           f"restart_not_pushed.png);"
                                           "border-radius: 10 px;")
        if self.volume_is_on:
            self.volume_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/volume_on_not_pushed.png);"
                                          "border-radius: 10 px;")
        else:
            self.volume_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/volume_off_not_pushed.png);"
                                          "border-radius: 10 px;")
        self.settings_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/settings_not_pushed.png);"
                                        "border-radius: 10 px;")
        self.start_timer_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/start_timer_not_pushed.png);"
                                           "border-radius: 10 px;")
        self.stop_timer_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/stop_timer_not_pushed.png);"
                                          "border-radius: 10 px;")
        self.tips_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/tips_not_pushed.png);"
                                    "border-radius: 10 px;")
        self.back_move_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/back_move_not_pushed.png);"
                                         "border-radius: 10 px;")
        self.back_menu_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/back_not_pushed.png);"
                                         "border-radius: 10 px;")
        self.you_win_label.setStyleSheet(f"image: url(images/instant_images_{self.language}/you_win.png);")
        if self.language == "ru":
            self.score_label.setText("Результаты")
            self.steps_label_2.setText("Шаги:")
            self.info.setText(self.tips[0])
            self.info.setWindowTitle("Помощь")
        elif self.language == "us":
            self.score_label.setText("Score")
            self.steps_label_2.setText("Steps:")
            self.info.setText(self.tips[1])
            self.info.setWindowTitle("Tips")

    def clear_bd(self):
        self.cur.execute("""
        DELETE FROM score
        """)
        self.con.commit()

    def sound(self):
        if self.volume_is_on:  # если звук включен проигрываем звук
            self.sound_buttons.play()

    def animation_of_button(self, btn, position=""):
        # анимация не игровых кнопок (новая игра, рестарт, звук, настройки, стоп и старт таймер)
        self.sound()
        # если кнопка не имеет двоякого положения (старт, рестар, включен, выключен) просто берем две картинки
        # если двоякое положение есть обращаемся по этому положению и берем две картинки
        if position == "":
            first_image = self.images[btn][0]
            second_image = self.images[btn][1]
        else:
            first_image = self.images[btn][position][0]
            second_image = self.images[btn][position][1]
        btn.setStyleSheet(f"image: url({first_image});"  # устнаваливаем первую картинку (кнопка нажата)
                          "border-radius: 10 px;")
        self.app.processEvents()  # прорисовщик
        sleep(0.1)  # анимация длится 0.1 секунды
        btn.setStyleSheet(f"image: url({second_image});"  # устанавливем вторую картинку (кнопка отжата)
                          "border-radius: 10 px;")
        self.app.processEvents()  # прорисовщик

    def display_steps(self):
        # отображение количества шагов
        self.steps_label.setText(str(self.count_of_steps))

    def timer_create(self):
        # создание таймера
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_update)
        self.start_time = time()
        self.timer_is_started = True
        self.timer.start(10)
        # таймер будет обновлятся каждые десять миллисекунд (таймер отображает только десятки миллисекунд)

    def timer_update(self):
        # обновляем время на таймере (каждые 10 миллисекунд)
        my_time = round(time() - self.start_time - sum(self.intervals_of_stopping), 2)
        # из нынешнего выремени вычитаем время начала таймера и сумму
        # временных отрезков между началом и остановкой таймера
        # получаем время на таймере
        m = str(int(my_time // 60))  # находим минуты
        s = str(int(my_time % 60))  # находим секунды
        ms = str(int(my_time * 100 % 100))  # находим сотые секунд (десятки миллисекунд)
        # my_time это десятичная дробь поэтому умножая на 100 и находя остаток от деления на 100
        # мы находим две цифры после запятой

        # приводим все к одной строке и выводим
        # цифр в числе либо одна либо две, если одна, то будет один ноль,
        # если два, то нулей не будет (для красивого вывода)
        self.timer_label.setText(f"{'0' * (2 - len(m)) + m}:"
                                 f"{'0' * (2 - len(s)) + s}:"
                                 f"{'0' * (2 - len(ms)) + ms}")

    def update_time_table(self, t):
        # обновляем поле со временем всех прохождений
        if t:
            t = t.split(':')
            tms = (int(t[0]) * 60 + int(t[1])) * 100 + int(t[2])
            self.cur.execute(f'''
            INSERT INTO score(time, steps) VALUES({tms}, {self.count_of_steps}) 
            ''')
            self.con.commit()
        self.cur.execute('''
        SELECT time, steps FROM score ORDER BY time LIMIT 3
        ''')
        times = self.cur.fetchall()
        answer = ['\n']
        for i in range(len(times)):
            tms, steps = times[i]
            m = tms // 6000
            s = (tms // 100) % 60
            ms = tms - (m * 60 + s) * 100
            m, s, ms = str(m), str(s), str(ms)
            answer.append(f"  {i + 1}.{'0' * (2 - len(m)) + m}:"
                          f"{'0' * (2 - len(s)) + s}:"
                          f"{'0' * (2 - len(ms)) + ms} \n"
                          f"  {steps} steps  \n")
        self.time_table.setText("".join(answer))

    def start_timer(self):
        self.statusBar.clearMessage()
        if self.timer_is_started:
            if self.language == "us":
                self.statusBar.showMessage("Timer is already started")
            elif self.language == "ru":
                self.statusBar.showMessage("Таймер уже запущен")
        if not self.game_is_started:
            if self.language == "us":
                self.statusBar.showMessage("You can't start timer if you didn't start the game")
            elif self.language == "ru":
                self.statusBar.showMessage("Таймер будет запущен если ты начнешь игру")
        # запуск таймера
        btn = self.sender()  # для анимации
        # если игра началась и таймер остановлен то можно заупстить таймер
        if self.game_is_started and not self.timer_is_started:
            self.start_timer_time = time()  # время начала таймера
            # добавляем временной отрезок с последней остановки таймера (если остановки не было вычтет 0)
            self.intervals_of_stopping.append(self.start_timer_time - self.stop_timer_time)
            self.timer.start()
            self.timer_is_started = True
            if btn == self.start_timer_btn:
                self.animation_of_button(btn)
        else:
            if btn == self.start_timer_btn:
                self.animation_of_button(btn)

    def stop_timer(self):
        self.statusBar.clearMessage()
        if not self.timer_is_started:
            if self.language == "us":
                self.statusBar.showMessage("Timer is already stopped")
            elif self.language == "ru":
                self.statusBar.showMessage("Таймер уже остановлен")
        btn = self.sender()  # для анимации
        if self.game_is_started and self.timer_is_started:
            self.stop_timer_time = time()
            self.timer.stop()
            self.timer_is_started = False
            if btn == self.stop_timer_btn:
                self.animation_of_button(btn)
        else:
            if btn == self.stop_timer_btn:
                self.animation_of_button(btn)

    def checking(self):
        """проверка выиграл ли игрок"""
        if self.field == [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
                          self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty] or self.cheats_on:
            if self.volume_is_on:
                self.win_sound.play()
            self.won = True
            self.game_is_started = False
            self.timer.stop()
            self.timer_is_started = False
            self.update_time_table(self.timer_label.text())
        else:
            self.won = False

    def checking_for_progress_bar(self):
        won = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
               self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty]
        percents = {1: 15,
                    2: 20,
                    3: 25,
                    4: 30,
                    5: 35,
                    6: 40,
                    7: 45,
                    8: 50,
                    9: 55,
                    10: 60,
                    11: 65,
                    12: 70,
                    13: 75,
                    14: 80,
                    15: 100}
        for i in range(1, 16):
            if self.field[:i] == won[:i]:
                self.progressBar.setValue(percents[i])

    def my_move(self):
        self.statusBar.clearMessage()
        if self.game_is_started:
            if not self.won and self.timer_is_started:
                """игрок еще не выиграл и таймер запущен"""
                btn = self.sender()
                pos_of_btn = self.field.index(btn)
                x_btn, y_btn = self.positions[pos_of_btn]
                pos_of_empty_btn = self.field.index(self.empty)
                x_empty_btn, y_empty_btn = self.positions[pos_of_empty_btn]
                if x_btn == x_empty_btn:
                    if y_btn > y_empty_btn:
                        step = -4
                    else:
                        step = 4
                    buttons = [(self.field[i], i) for i in range(pos_of_btn, pos_of_empty_btn, step)][::-1]
                    animation_group = QParallelAnimationGroup(self)
                    self.list_for_moves = []
                    for button, pos in buttons:
                        new_x, new_y = self.positions[pos + step]
                        animation = QPropertyAnimation(button, b"pos", self)
                        animation.setEndValue(QPoint(new_x, new_y))
                        animation.setDuration(self.speeds_of_play_buttons[self.speed_of_play_buttons])
                        animation_group.addAnimation(animation)
                        self.list_for_moves.append((button, self.positions[pos], (new_x, new_y)))
                    animation_group.start()
                    self.moves.append(self.list_for_moves)
                    if len(buttons) == 1:
                        self.field[pos_of_btn], self.field[pos_of_btn + step] = \
                            self.field[pos_of_empty_btn], self.field[pos_of_btn]
                        self.count_of_steps += 1
                    elif len(buttons) == 2:
                        self.field[pos_of_btn], self.field[pos_of_btn + step], \
                        self.field[pos_of_btn + 2 * step] = \
                            self.field[pos_of_empty_btn], self.field[pos_of_btn], \
                            self.field[pos_of_btn + step]
                        self.count_of_steps += 2
                    elif len(buttons) == 3:
                        self.field[pos_of_btn], self.field[pos_of_btn + step], \
                        self.field[pos_of_btn + 2 * step], self.field[pos_of_btn + 3 * step] = \
                            self.field[pos_of_empty_btn], self.field[pos_of_btn], \
                            self.field[pos_of_btn + step], self.field[pos_of_btn + 2 * step]
                        self.count_of_steps += 3
                elif y_btn == y_empty_btn:
                    if x_btn > x_empty_btn:
                        step = -1
                    else:
                        step = 1
                    buttons = [(self.field[i], i) for i in range(pos_of_btn, pos_of_empty_btn, step)][::-1]
                    animation_group = QParallelAnimationGroup(self)
                    self.list_for_moves = []
                    for button, pos in buttons:
                        new_x, new_y = self.positions[pos + step]
                        animation = QPropertyAnimation(button, b"pos", self)
                        animation.setEndValue(QPoint(new_x, new_y))
                        animation.setDuration(self.speeds_of_play_buttons[self.speed_of_play_buttons])
                        animation_group.addAnimation(animation)
                        self.list_for_moves.append((button, self.positions[pos], (new_x, new_y)))
                    animation_group.start()
                    self.moves.append(self.list_for_moves)
                    if len(buttons) == 1:
                        self.field[pos_of_btn], self.field[pos_of_btn + step] = \
                            self.field[pos_of_empty_btn], self.field[pos_of_btn]
                        self.count_of_steps += 1
                    elif len(buttons) == 2:
                        self.field[pos_of_btn], self.field[pos_of_btn + step], \
                        self.field[pos_of_btn + 2 * step] = \
                            self.field[pos_of_empty_btn], self.field[pos_of_btn], \
                            self.field[pos_of_btn + step]
                        self.count_of_steps += 2
                    elif len(buttons) == 3:
                        self.field[pos_of_btn], self.field[pos_of_btn + step], \
                        self.field[pos_of_btn + 2 * step], self.field[pos_of_btn + 3 * step] = \
                            self.field[pos_of_empty_btn], self.field[pos_of_btn], \
                            self.field[pos_of_btn + step], self.field[pos_of_btn + 2 * step]
                        self.count_of_steps += 3
                else:
                    if self.language == "us":
                        self.statusBar.showMessage("You can't move this button")
                    elif self.language == "ru":
                        self.statusBar.showMessage("Эта кнопка недоступна для движения")
                self.sound_play_buttons.play()
                self.display_steps()
                self.checking_for_progress_bar()
                self.checking()
                if self.won:
                    """если игрок выиграл
                    появляется сообщение о выигрыше"""
                    self.you_win_label.show()

            else:
                if self.language == "us":
                    self.statusBar.showMessage("Start the timer before doing a move")
                elif self.language == "ru":
                    self.statusBar.showMessage("Запусти таймер прежде чем ходить")
                """игрок выиграл но все равно пытается сделать ход"""
        else:
            if self.language == "us":
                self.statusBar.showMessage("You should shuffle field first")
            elif self.language == "ru":
                self.statusBar.showMessage("Сперва перемешайте пятнашки")
            """начальное поле игрок еще не перемешал пятнашки"""

    def back_move(self):
        self.statusBar.clearMessage()
        btn = self.sender()
        if btn == self.back_move_btn:
            self.animation_of_button(btn)
        if self.game_is_started:
            if self.timer_is_started:
                if bool(self.moves):
                    buttons = self.moves.pop()
                    if not self.animation_back_move_btn:
                        for button, old_pos, pos in buttons[::-1]:
                            x1, y1 = old_pos
                            x2, y2 = pos
                            button.move(x1, y1)
                            self.empty.move(x2, y2)
                            btn_index = self.field.index(button)
                            empty_index = self.field.index(self.empty)
                            self.field[btn_index], self.field[empty_index] = self.field[empty_index], self.field[
                                btn_index]
                            self.count_of_steps -= 1
                    else:
                        animation_group = QParallelAnimationGroup(self)
                        for button, old_pos, pos in buttons[::-1]:
                            x1, y1 = old_pos
                            x2, y2 = pos
                            animation = QPropertyAnimation(button, b"pos", self)
                            animation.setEndValue(QPoint(x1, y1))
                            animation.setDuration(self.speeds_of_play_buttons[self.speed_of_play_buttons])
                            animation_group.addAnimation(animation)
                            self.empty.move(x2, y2)
                            btn_index = self.field.index(button)
                            empty_index = self.field.index(self.empty)
                            self.field[btn_index], self.field[empty_index] = self.field[empty_index], self.field[
                                btn_index]
                            self.count_of_steps -= 1
                        animation_group.start()
                    self.display_steps()
                else:
                    if self.language == "us":
                        self.statusBar.showMessage("You should do a move first")
                    elif self.language == "ru":
                        self.statusBar.showMessage("Сперва сделайте ход")
            else:
                if self.language == "us":
                    self.statusBar.showMessage("You should start a timer first")
                elif self.language == "ru":
                    self.statusBar.showMessage("Сперва запустите таймер")
        else:
            if self.language == "us":
                self.statusBar.showMessage("You should start a game first")
            elif self.language == "ru":
                self.statusBar.showMessage("Сперва начните игру")

    def new_game(self):
        """новая игра, обновляется таймер, информация о времени, кнопка рестарт и поле"""
        self.statusBar.clearMessage()
        btn = self.sender()  # для анимации
        if btn == self.new_game_btn:
            self.animation_of_button(btn)
        self.you_win_label.hide()
        self.game_is_started = False
        self.timer.stop()
        self.timer_is_started = False
        self.timer_label.setText('00:00:00')
        self.times = []
        self.time_table.setText('')
        self.count_of_steps = 0
        self.clear_bd()
        self.display_steps()
        self.restart_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/start_not_pushed.png);"
                                       "border-radius: 10 px;")
        self.field = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
                      self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty]
        self.progressBar.setValue(0)
        for i in range(16):
            x, y = self.positions[i]
            self.field[i].move(x, y)
        for i in range(len(self.field) - 1):
            # ставим на игровые кнопки картинки
            self.field[i].setStyleSheet(f"image: url(images/play_buttons/{i + 1}/{randint(1, 3)}.png);"
                                        "background-color: Transparent;")

    def restart(self):
        self.statusBar.clearMessage()
        """перемешивание пятнашек"""
        btn = self.sender()  # для анимации
        if btn == self.restart_btn:
            if self.game_is_started:
                self.animation_of_button(btn, position="restart")
            else:
                self.animation_of_button(btn, position="start")
        self.won = False
        self.you_win_label.hide()
        self.timer_create()
        self.intervals_of_stopping = []
        self.count_of_steps = 0
        self.game_is_started = True
        self.display_steps()
        self.moves.clear()
        self.progressBar.setValue(0)
        is_generated = False
        while not is_generated:
            """генерация поля таким образом, чтоб пятнашки можно было собрать"""
            shuffle(self.field)
            if self.field != [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
                              self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty]:
                pos_of_empty_btn = self.field.index(self.empty)
                if pos_of_empty_btn <= 3:
                    pos_of_empty_btn = 1
                elif 3 < pos_of_empty_btn <= 7:
                    pos_of_empty_btn = 2
                elif 7 < pos_of_empty_btn <= 11:
                    pos_of_empty_btn = 3
                else:
                    pos_of_empty_btn = 4
                control_sum = 0
                for i in range(15):
                    number1 = self.field_values[self.field[i]]
                    if number1 != 0:
                        for j in range(i + 1, 16):
                            number2 = self.field_values[self.field[j]]
                            if number2 != 0:
                                if number1 > number2:
                                    control_sum += 1
                control_sum += pos_of_empty_btn
                if control_sum % 2 == 0:
                    is_generated = True
        for i in range(16):
            x, y = self.positions[i]
            self.field[i].move(x, y)
        self.checking_for_progress_bar()

    def volume(self):
        btn = self.sender()  # для анимации
        if btn == self.volume_btn:
            if self.volume_is_on:
                self.animation_of_button(btn, position="on")
            else:
                self.animation_of_button(btn, position="off")
        self.volume_is_on = not self.volume_is_on

    def settings(self):
        btn = self.sender()  # для анимации
        if btn == self.settings_btn:
            self.animation_of_button(btn)
        self.previousIndex = 1
        windows.setCurrentIndex(2)

    def back_menu(self):
        btn = self.sender()
        if btn == self.back_menu_btn:
            self.animation_of_button(btn)
        windows.setCurrentIndex(0)

    def show_dialog(self):
        btn = self.sender()
        if self.sender() == btn:
            self.animation_of_button(btn)
        self.info.exec_()

    def save(self):
        file_path = QFileDialog.getSaveFileName(
            self, 'Выбрать картинку', '',
            'БД (*.sqlite3)')[0]
        my_game_path = ''
        backslash = r"\ "
        for i in path.abspath("my_game.sqlite3"):
            if i == backslash[0]:
                i = "/"
            my_game_path += i
        if file_path == my_game_path:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Warning)
            if self.language == "us":
                warning.setWindowTitle("Error")
            elif self.language == "ru":
                warning.setWindowTitle("Ошибка")
            ok = warning.addButton(QMessageBox.Ok)
            ok.setFont(QFont("Comic Sans MS", 10))
            ok.setStyleSheet("background-color: rgb(210, 217, 255);")
            ok.clicked.connect(self.sound)
            warning.setStyleSheet("background-color: rgb(149, 181, 255);")
            warning.setFont(QFont("Comic Sans MS", 10))
            if self.language == "us":
                warning.setText(self.warnings[0])
            if self.language == "ru":
                warning.setText(self.warnings[1])
            warning.exec_()
        elif len(file_path) != 0:
            self.con2 = sqlite3.connect(file_path)
            self.con.backup(target=self.con2)


class SettingsScreen(QMainWindow, Ui_MainWindow_Settings):
    def __init__(self, app_, main_window, start_window):
        super().__init__()
        self.initUI(app_, main_window, start_window)

    def initUI(self, app_, main_window, start_window):
        self.setupUi(self)
        self.app = app_
        self.main_window = main_window
        self.start_window = start_window
        self.back_btn.clicked.connect(self.back_to_menu)
        self.speed_spin_box.setValue(self.main_window.speed_of_play_buttons)
        self.speed_spin_box.valueChanged.connect(self.refresh_speed_value)
        self.language_comboBox.activated[str].connect(self.change_language)
        self.language_comboBox.addItem("English")
        self.language_comboBox.addItem("Русский")
        self.back_comboBox.activated[str].connect(self.back_animation_refresh)
        self.cheat_button.clicked.connect(self.cheats)
        self.refresh_language()

    def back_to_menu(self):
        btn = self.back_btn
        if self.sender() == btn:
            # анимация
            if self.main_window.volume_is_on:
                self.main_window.sound_buttons.play()
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/back_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
            sleep(0.1)
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/back_not_pushed.png);"
                              "border-radius: 10 px;")
            self.app.processEvents()
        if self.main_window.previousIndex == 1:
            windows.setCurrentIndex(1)
        elif self.main_window.previousIndex == 0:
            windows.setCurrentIndex(0)

    def refresh_speed_value(self):
        self.main_window.speed_of_play_buttons = self.speed_spin_box.value()

    def change_language(self, text):
        if text == "Русский":
            self.main_window.language = "ru"
        elif text == "English":
            self.main_window.language = "us"
        self.refresh_language()
        self.main_window.refresh_language()
        self.start_window.refresh_language()

    def back_animation_refresh(self, text):
        self.main_window.animation_back_move_btn = (text == "Yes" or text == "Да")

    def cheats(self):
        self.main_window.cheats_on = not self.main_window.cheats_on

    def refresh_language(self):
        self.back_btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/back_not_pushed.png);"
                                    "border-radius: 10 px;")
        if self.main_window.language == "ru":
            self.settings_label.setText("Настройки")
            self.speed_label.setText("Скорость")
            self.language_label.setText("Язык")
            self.back_move_label.setText("Анимация хода назад")
            self.language_label.setText("Язык")
            self.back_comboBox.clear()
            if self.main_window.animation_back_move_btn:
                self.back_comboBox.addItem("Да")
                self.back_comboBox.addItem("Нет")
            else:
                self.back_comboBox.addItem("Нет")
                self.back_comboBox.addItem("Да")
        elif self.main_window.language == "us":
            self.settings_label.setText("Settings")
            self.speed_label.setText("Speed")
            self.language_label.setText("Language")
            self.back_move_label.setText("Backtrack animation")
            self.back_comboBox.clear()
            if self.main_window.animation_back_move_btn:
                self.back_comboBox.addItem("Yes")
                self.back_comboBox.addItem("No")
            else:
                self.back_comboBox.addItem("No")
                self.back_comboBox.addItem("Yes")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    play_screen = PlayScreen(app)
    start_screen = StartScreen(app, play_screen)
    settings_screen = SettingsScreen(app, play_screen, start_screen)

    windows = QStackedWidget()
    windows.closeEvent = play_screen.closeEvent
    windows.addWidget(start_screen)
    windows.addWidget(play_screen)
    windows.addWidget(settings_screen)
    windows.setWindowIcon(QIcon("images/icons/icon.png"))
    windows.setWindowTitle("15Puzzle")
    windows.setFixedSize(1063, 685)

    windows.show()
    sys.exit(app.exec())
