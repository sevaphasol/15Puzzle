import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget, QFileDialog, QShortcut
from PyQt5.Qt import QParallelAnimationGroup, QStatusBar, QFont, Qt
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtMultimedia import QSound
import sqlite3

from ui.MainScreen import Ui_MainWindow_Play
from ui.SettingsScreen import Ui_MainWindow_Settings
from ui.StartScreen import Ui_MainWindow_Start

from time import sleep, time
from random import shuffle, randint
from os import path


class StartScreen(QMainWindow, Ui_MainWindow_Start):  # стартовое окно
    def __init__(self, app_, main_window):
        super().__init__()
        self.initUI(app_, main_window)

    def initUI(self, app_, main_window):
        self.setupUi(self)
        self.app = app_  # длч отрисовки
        self.new_game_btn.clicked.connect(self.new_game)
        self.resume_game_btn.clicked.connect(self.resume_game)
        self.settings_btn.clicked.connect(self.open_settings)
        self.main_window = main_window  # для того чтобы можно было изменять основные перменные
        self.refresh_language()  # обновление языка
        self.label_gif1.setStyleSheet("image: url(images/other_images/left.png);"
                                      "border-radius: 10 px;")
        self.label_gif2.setStyleSheet("image: url(images/other_images/right.png);"
                                      "border-radius: 10 px;")
        # картинки по бокам

    def new_game(self):  # кнопка новая игра
        btn = self.new_game_btn  # для анимации
        if self.sender() == btn:
            if self.main_window.volume_is_on:  # если звук включен
                self.main_window.sound_buttons.play()
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/new_game_pushed.png);"
                              "border-radius: 10 px;")  # устанавливаем кнопку нажатия
            self.app.processEvents()  # прорисовщик
            sleep(0.1)  # анимация длится 10 миллисекунд
            btn.setStyleSheet(f"image: url(images/buttons_{self.main_window.language}/new_game_not_pushed.png);"
                              "border-radius: 10 px;")  # возвращаем прежнюю картинку
            self.app.processEvents()  # отрисовываем
        self.main_window.need_to_clear = True  # нужно ли очистить бд при
        # закрытии если честно не помню зачем но убирать страшно
        self.main_window.con = sqlite3.connect("my_game.sqlite3")  # БД
        self.main_window.cur = self.main_window.con.cursor()
        self.main_window.cur.execute("""
                DELETE FROM score
                """)  # чистим
        self.main_window.con.commit()
        self.main_window.cur.execute("""
                        CREATE TABLE IF NOT EXISTS score
                        ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [time] INTEGER, [steps] INTEGER)
                        """)  # создаем нужные строки
        self.main_window.con.commit()
        self.main_window.is_game_opened = False  # игра новая -> игру не открывали
        self.main_window.update_time_table(time_from_timer=False)  # обновляем табло
        # со временем но без взятия времени из таймера
        windows.setCurrentIndex(1)  # меняем экран на основной

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
        file_path = QFileDialog.getOpenFileName(  # диалог для выбора игры
            self, 'Выбрать игру', 'games',
            'БД (*.sqlite3)')[0]
        # ниже код нужен для проверки на то случай если пользователь захочет сохранить с именем промежуточной бд
        my_game_path = ''
        backslash = r"\ "  # почему то абспаф сохраняет путь с таким слэшем поэтому ниже я меняю его на обратный
        for i in path.abspath("my_game.sqlite3"):
            if i == backslash[0]:
                i = "/"
            my_game_path += i
        if file_path == my_game_path:
            warning = QMessageBox()  # если хочет сохранить с именем промежуточной бд появляется ошибка
            warning.setIcon(QMessageBox.Warning)
            # ниже зависимость от языка
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
        elif len(file_path) != 0:  # если выбран хоть какой то файл
            self.main_window.opened_con = sqlite3.connect(file_path)  # открываем выбранную бд
            self.main_window.con = sqlite3.connect("my_game.sqlite3")  # все равно нужна промежуточная бд
            self.main_window.opened_con.backup(target=self.main_window.con)  # записываем в промежуточную бд открытую бд
            self.main_window.cur = self.main_window.con.cursor()
            self.main_window.opened_cur = self.main_window.opened_con.cursor()
            self.main_window.is_game_opened = True  # игру открыли а не начали заново
            self.main_window.update_time_table(time_from_timer=False)
            windows.setCurrentIndex(1)  # меняем экран на основной

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
        self.main_window.previousIndex = 0  # предыдущее окно было стартовое
        # (для корректного возвращения из настроек обратно)
        windows.setCurrentIndex(2)  # меняем окно на настройки

    def refresh_language(self):
        # обновление языка
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
        self.app = app_  # для отрисовки
        self.language = "us"  # изначально язык английский
        self.cheats_on = False  # читы вырублены
        self.need_to_clear = True  # до сих пор не понимаю зачем она
        self.previousIndex = 0  # предыдущее окно
        self.info = QMessageBox()  # помощь
        # css
        self.ok = self.info.addButton(QMessageBox.Ok)
        self.ok.setFont(QFont("Comic Sans MS", 10))
        self.ok.setStyleSheet("background-color: rgb(210, 217, 255);")
        self.ok.clicked.connect(self.sound)
        self.info.setStyleSheet("background-color: rgb(149, 181, 255);")
        self.info.setFont(QFont("Comic Sans MS", 10))
        self.info.setWindowIcon(QIcon("images/icons/question_icon.png"))
        # типсы
        self.tips = [
            'Чтобы походить нажмите на кнопку с цифрой либо нажмите на кнопку w/a/s/d. \n'
            'w - верхняя кнопка, a - левая кнопка, s - нижняя кнопка, d - правая кнопка. \n'
            'Ходить можно только если кнопка находится на одной горизонтали или вертикали с пустой кнопкой. \n'
            'Ваша задача собрать все квадратики по порядку от 1 до 15. \n'
            'Вы играете на время. Время отображается на таймере. \n'
            'В таблице результатов отображаются времена прохождения. \n'
            'Вы можете сохранить игру при использовании вкладки игра наверху. \n'
            'Вы можете ходить назад с помощью кнопки "<-". \n'
            'В любой момент игры можно остановить таймер и соответсвенно запустить его. При остановке ходить нельзя. \n'
            'Для того чтобы начать новую игру (удалить историю времен), нажмите новая игра. \n'
            'Для перемешивания поля нажмите старт/рестарт. \n '
            'Вы можете включить и выключить звук при помощи кнопки звук. \n'
            'Нажав на кнопку настройки, вы попадете в настройки. \n'
            'Приятной игры! \n \n'
            'ДЛЯ ТЕСТОВ В НАСТРОЙКАХ СПРАВА СВЕРХУ НЕВИДИМАЯ КНОПКА ЧИТОВ',
            'To move, click on the button with the number. or press w/a/s/d. \n'
            'w - up button, a - left button, s - down button, d - right button. \n'
            'You can only move if the button is on the same horizontal or vertical as an empty button. \n'
            'Your task is to collect all the squares in order from 1 to 15. \n'
            'You are playing against the clock. The time is displayed on the timer. \n'
            'Transit times are displayed in the table "score". \n'
            'You can save your game by using the game tab at the top. \n'
            'You can walk backward with the "<-" button. \n'
            'At any time during the game, you can stop the timer and start it accordingly.'
            'You cannot walk when you have stopped the timer. \n'
            'To start a new game (delete history of times) press new game. \n'
            'Press start/restart to shuffle the field. \n'
            'You can turn the sound on/off using the sound button. \n'
            'Clicking on the settings button will take you to the settings. \n'
            'GLHF! \n \n'
            'FOR TESTS IN THE SETTINGS ON THE TOP RIGHT INVISIBLE CHEAT BUTTON '
        ]

        # ошибки
        self.warnings = ["Try another name.", "Попробуйте другое имя."]
        self.warnings2 = ["Are you sure? If you will continue your game history will be deleted.",
                          "Вы уверены? Если вы продолжите, текущий сеанс игры удалится."]
        self.warnings3 = ["This game had never been saved. Firstly you need to save it.",
                          "Эту игру еще никогда не сохраняли. Для начала сохраните ее."]

        # статусбар
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.clearMessage()
        self.statusBar.setFont(QFont("Comic Sans MS", 10))

        self.animation_back_move_btn = False  # изначально анимации хода назад нет

        # устанавливаем звук
        self.sound_play_buttons = QSound("sounds/play_button_sound.wav")
        self.sound_buttons = QSound("sounds/button_sound.wav")
        self.win_sound = QSound("sounds/win_sound.wav")

        self.won = False  # игрок еще не выиграл
        self.you_win_label.hide()  # покажется когда игрок выиграет

        self.speeds_of_play_buttons = {10: 0, 9: 100, 8: 200, 7: 300, 6: 400, 5: 500, 4: 600, 3: 700, 2: 800, 1: 1000}
        # скорость в миллисекундах анимации кнопок
        self.speed_of_play_buttons = 8  # изначально скорость=8

        self.opened_con = None  # если не откроют игру то открытого бд нет
        self.is_game_opened = False  # игру не открыли
        # если игру откроют в начальном экрне это все поменяется

        self.count_of_steps = 0  # ноль шагов

        self.moves = []  # ходы игрока можно через бд но мне лень

        self.timer = QTimer()  # создаем таймер
        self.start_time = time()
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
        self.save_as_action.triggered.connect(self.save_as)
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)  # для сохранения
        self.shortcut_save.activated.connect(self.save)
        self.shortcut_save_as = QShortcut(QKeySequence("Ctrl+Shift+S"), self)  # для сохранения новой игры
        self.shortcut_save_as.activated.connect(self.save_as)

        self.refresh_language()  # обновление языка

    def closeEvent(self, event):  # если игру закрывают чистим бд если какая-то
        # пременная выполняется до сих пор не понял что это
        if self.need_to_clear:
            self.clear_bd()
            self.con.close()
        event.accept()  # закрываем

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
        """)  # чистка промежуточного бд
        self.con.commit()

    def sound(self):
        if self.volume_is_on:  # если звук включен проигрываем звук неигровых кнопок
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

    def display_steps(self):  # отображение шагов
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

    def update_time_table(self, t=None, time_from_timer=True):  # обновление табла с временем
        # обновляем поле со временем всех прохождений
        if time_from_timer:  # если обновляем из за того что таймер обновился (игра выиграна)
            t = t.split(':')  # получаем строку
            tms = (int(t[0]) * 60 + int(t[1])) * 100 + int(t[2])  # выражаем время в мс
            self.cur.execute(f'''
            INSERT INTO score(time, steps) VALUES({tms}, {self.count_of_steps}) 
            ''')  # записываем в бд
            self.con.commit()
        self.cur.execute('''
        SELECT time, steps FROM score ORDER BY time LIMIT 3
        ''')  # берем первые три времени в отсортированной бд
        # по-хорошему надо удалять хотя бы первые 10 прохождений чтобы не засорялась память
        # но там проблема какая то что при удалении из бд индекс все равно сохраняется и не получается в общем
        times = self.cur.fetchall()  # записываем в список
        answer = ['\n']  # для красивого отображения пустая строка
        # кстати на фул хд экране может быть немножко кривовато потому что я делал на 4к
        for i in range(len(times)):  # проходимся по временам
            tms, steps = times[i]  # время шаги
            m = tms // 6000  # получаем минуты из мс
            s = (tms // 100) % 60  # получаем секунды из мс
            ms = tms - (m * 60 + s) * 100  # получаем все оставшееся
            m, s, ms = str(m), str(s), str(ms)  # делаем строки
            answer.append(f"  {i + 1}.{'0' * (2 - len(m)) + m}:"  # записываем все по красоте (умножать строку ноль)
                          f"{'0' * (2 - len(s)) + s}:"  # если во времени только одна цифра то нужен один
                          f"{'0' * (2 - len(ms)) + ms} \n"  # ноль если две то нулей не нужно
                          f"  {steps} steps  \n")
        self.time_table.setText("".join(answer))  # отображаем время на табло

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
        # стоп таймера
        self.statusBar.clearMessage()
        if not self.timer_is_started:
            if self.language == "us":
                self.statusBar.showMessage("Timer is already stopped")
            elif self.language == "ru":
                self.statusBar.showMessage("Таймер уже остановлен")
        btn = self.sender()  # для анимации
        if self.game_is_started and self.timer_is_started:
            self.stop_timer_time = time()  # время остановки
            self.timer.stop()  # стопим сам таймер
            self.timer_is_started = False  # таймер остановили
            if btn == self.stop_timer_btn:
                self.animation_of_button(btn)  # анимацию позже т.к в анимации мы ждем 10 мс
                # можно было сделать в отдельном потоке но мне лень
        else:
            if btn == self.stop_timer_btn:
                self.animation_of_button(btn)

    def checking(self):
        # проверка выиграл ли игрок
        # если пятнашки собраны или врублены читы
        if self.field == [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
                          self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty] or self.cheats_on:
            if self.volume_is_on:
                self.win_sound.play()
            self.won = True  # игрок выиграл
            self.game_is_started = False  # игра закончена
            self.timer.stop()  # стопим таймер
            self.timer_is_started = False  # таймер остановлен
            self.update_time_table(t=self.timer_label.text())  # обновляем таймер передаем ему время из таймера
            self.progressBar.setValue(100)  # собраны на 100 процентов
        else:
            self.won = False  # игрок не выиграл

    def checking_for_progress_bar(self):
        won = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
               self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty]
        # как выглядят собранные пятнашки
        percents = {0: 0,
                    1: 15,
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
                    15: 100}  # я же говорил что формулы никакой нет тут нет ничего интересного
        # если честно то формулу мне конечно лень делать но даже если ее сделать так как у меня бордер радиус стоит
        # на цсс то там если меньше какого то значение почему то слетает цсс и некрасиво получается
        for i in range(15, 0, -1):
            if self.field[:i] == won[:i]:  # проверяем на собранность
                self.progressBar.setValue(percents[i])  # ставим столько процентом на сколько совпадает
                break  # у вас мэтч
        else:  # ничего не совпало
            self.progressBar.setValue(percents[0])

    def my_move(self):
        self.statusBar.clearMessage()  # очищаем статус бар
        if self.game_is_started:  # если игра начата
            if not self.won and self.timer_is_started:
                """игрок еще не выиграл и таймер запущен"""
                btn = self.sender()  # кнопка которую нажали
                pos_of_btn = self.field.index(btn)  # где кнопка сейчас на поле
                x_btn, y_btn = self.positions[pos_of_btn]
                # координаты кнопки (для этого мне пришлось обойтись без лэйотов)
                pos_of_empty_btn = self.field.index(self.empty)  # где пустая кнопка сейчас на поле
                x_empty_btn, y_empty_btn = self.positions[pos_of_empty_btn]  # координаты пустой кнопки
                if x_btn == x_empty_btn:  # если пустая кнопка и кнопка которую нажали лежат на одной вертикали
                    if self.volume_is_on:  # звук
                        self.sound_play_buttons.play()
                    if y_btn > y_empty_btn:  # если кнопка ниже пустой кнопки мы двигаемся вверх
                        step = -4
                    else:
                        step = 4  # здесь двигаемя вниз
                    buttons = [(self.field[i], i) for i in range(pos_of_btn, pos_of_empty_btn, step)][::-1]
                    # берем все кнопки стоящие между пустой и нажатой кнопкой на вертикали включая нажатую кнопку
                    animation_group = QParallelAnimationGroup(self)  # группа кнопок для анимации
                    self.list_for_moves = []  # это для ходов назад
                    for button, pos in buttons:  # берем кнопку и ее номер на поле
                        new_x, new_y = self.positions[pos + step]  # берем следующую кнопку на вертикали
                        animation = QPropertyAnimation(button, b"pos", self)  # создаем анимацию
                        animation.setEndValue(QPoint(new_x, new_y))  # задаем конечные координаты
                        animation.setDuration(self.speeds_of_play_buttons[self.speed_of_play_buttons])
                        # задаем длительность в скорость кнопок
                        animation_group.addAnimation(animation)  # добавляем анимацию в группу анимаций
                        self.list_for_moves.append((button, self.positions[pos], (new_x, new_y)))
                        # добавляем в список для шагов назад
                    animation_group.start()  # запускаем анимацию как я понял она автоматически в другом потоке
                    self.moves.append(self.list_for_moves)  # добавляем в основной список для шагов назад
                    # делаем так потому что нам нужны вложенные списки
                    # они нужны для того что запускать обратную анимацию если что сразу группой кнопок
                    # (если ход был такой)
                    # дальше в заисимости от количества кнопок меняем их местами
                    # адаптивности под большие количетсва нет(
                    # она нужна была бы если я делал сложность игры
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
                elif y_btn == y_empty_btn:  # все то же самое но если кнопки на одной горизонтали
                    if self.volume_is_on:
                        self.sound_play_buttons.play()
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
                    # выводим ошибку в статус бар если кнопка ни на одной горизонтали ни на одной вертикали с пустой
                    if self.language == "us":
                        self.statusBar.showMessage("You can't move this button")
                    elif self.language == "ru":
                        self.statusBar.showMessage("Эта кнопка недоступна для движения")
                self.display_steps()  # обновляем шаги
                self.checking_for_progress_bar()  # обновляем проценты
                self.checking()  # проверяем вдруг игрок выиграл
                if self.won:  # если выиграл выводим сообщение
                    self.you_win_label.show()

            else:
                # игрок остановил таймер, но хочет пойти
                if self.language == "us":
                    self.statusBar.showMessage("Start the timer before doing a move")
                elif self.language == "ru":
                    self.statusBar.showMessage("Запусти таймер прежде чем ходить")
        else:
            # игрок еще не начал игру
            if self.language == "us":
                self.statusBar.showMessage("You should shuffle field first")
            elif self.language == "ru":
                self.statusBar.showMessage("Сперва перемешайте пятнашки")

    def move_with_keyboard(self, pos):
        self.statusBar.clearMessage()  # очищаем статус бар
        if self.game_is_started:  # если игра начата
            if not self.won and self.timer_is_started:
                pos_of_empty_btn = self.field.index(self.empty)  # где пустая кнопка сейчас на поле
                x_empty_btn, y_empty_btn = self.positions[pos_of_empty_btn]  # координаты пустой кнопки
                if 15 >= pos_of_empty_btn + pos >= 0:  # если кнопка которой мы хотим пойти существует на поле
                    btn = self.field[pos_of_empty_btn + pos]  # кнопка
                    pos_of_btn = self.field.index(btn)  # где кнопка сейчас на поле
                    if pos_of_btn % 4 == pos_of_empty_btn % 4 or pos_of_btn // 4 == pos_of_empty_btn // 4:
                        # если на одной вертикали или горизонтали
                        if self.volume_is_on:  # звук
                            self.sound_play_buttons.play()
                        animation = QPropertyAnimation(btn, b"pos", self)  # анимация
                        animation.setEndValue(QPoint(x_empty_btn, y_empty_btn))  # конечная координата
                        animation.setDuration(self.speeds_of_play_buttons[self.speed_of_play_buttons])  # время
                        animation.start()
                        self.moves.append([(btn, self.positions[pos_of_btn], (x_empty_btn, y_empty_btn))])  # ходы назад
                        self.field[pos_of_btn], self.field[pos_of_empty_btn] = \
                            self.field[pos_of_empty_btn], self.field[pos_of_btn]  # меняем местами в списке всех кнопок
                        self.count_of_steps += 1  # шаги
                        self.display_steps()  # обновляем шаги
                        self.checking_for_progress_bar()  # обновляем проценты
                        self.checking()  # проверяем вдруг игрок выиграл
                        if self.won:  # если выиграл выводим сообщение
                            self.you_win_label.show()
                else:
                    if self.language == "us":
                        self.statusBar.showMessage("You can't move this button")
                    elif self.language == "ru":
                        self.statusBar.showMessage("Эта кнопка недоступна для движения")
            else:
                if self.language == "us":
                    self.statusBar.showMessage("Start the timer before doing a move")
                elif self.language == "ru":
                    self.statusBar.showMessage("Запусти таймер прежде чем ходить")
        else:
            if self.language == "us":
                self.statusBar.showMessage("You should shuffle field first")
            elif self.language == "ru":
                self.statusBar.showMessage("Сперва перемешайте пятнашки")

    def keyPressEvent(self, event):
        #  ход с помощью клавиатуры
        key = event.key()
        if key == Qt.Key_A:  # a
            self.move_with_keyboard(-1)
        elif key == Qt.Key_W:  # w
            self.move_with_keyboard(-4)
        elif key == Qt.Key_D:  # d
            self.move_with_keyboard(1)
        elif key == Qt.Key_S:  # s
            self.move_with_keyboard(4)

    def back_move(self):
        # ход назад
        self.statusBar.clearMessage()  # очищаем статус бар
        btn = self.sender()  # анимация
        if btn == self.back_move_btn:
            self.animation_of_button(btn)
        if self.game_is_started:  # если игра начата
            if self.timer_is_started:  # еслитаймер запущен
                if bool(self.moves):  # если хоть какие то ходы были сделаны
                    buttons = self.moves.pop()  # берем последний ход
                    if not self.animation_back_move_btn:  # ели без анимации то просто перемещаем кнопки на свои места
                        for button, old_pos, pos in buttons[::-1]:
                            x1, y1 = old_pos
                            x2, y2 = pos
                            button.move(x1, y1)
                            self.empty.move(x2, y2)
                            btn_index = self.field.index(button)
                            empty_index = self.field.index(self.empty)
                            self.field[btn_index], self.field[empty_index] = self.field[empty_index], self.field[
                                btn_index]
                            self.count_of_steps -= 1  # -1 ход
                    else:  # если с анимацией
                        # принцип примерно такой же как с обычным ходом
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
                            self.count_of_steps -= 1  # -1 ход
                        animation_group.start()
                    self.display_steps()
                else:
                    # не сделал ни одного хода
                    if self.language == "us":
                        self.statusBar.showMessage("You should do a move first")
                    elif self.language == "ru":
                        self.statusBar.showMessage("Сперва сделайте ход")
            else:
                # не запустил таймер
                if self.language == "us":
                    self.statusBar.showMessage("You should start a timer first")
                elif self.language == "ru":
                    self.statusBar.showMessage("Сперва запустите таймер")
        else:
            # не начал игру
            if self.language == "us":
                self.statusBar.showMessage("You should start a game first")
            elif self.language == "ru":
                self.statusBar.showMessage("Сперва начните игру")

    def new_game(self):
        # новая игра
        self.statusBar.clearMessage()  # чистим статус бар
        btn = self.sender()  # для анимации
        if btn == self.new_game_btn:
            self.animation_of_button(btn)
        self.you_win_label.hide()  # убираем штуку с выигрышем
        self.game_is_started = False  # игра не начата (там нужно старт нажать)
        self.timer.stop()  # остновить таймер
        self.timer_is_started = False  # таймер остановлен
        self.timer_label.setText('00:00:00')  # обновляем поле с таймером
        self.time_table.setText('')  # обновляем табло
        self.count_of_steps = 0
        self.clear_bd()
        self.display_steps()
        self.restart_btn.setStyleSheet(f"image: url(images/buttons_{self.language}/start_not_pushed.png);"
                                       "border-radius: 10 px;")
        self.progressBar.setValue(0)  # ставим 0 процентов
        self.field = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
                      self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty]
        # ставим собранные пятнашки
        self.progressBar.setValue(0)
        for i in range(16):
            x, y = self.positions[i]
            self.field[i].move(x, y)
        for i in range(len(self.field) - 1):
            # ставим на игровые кнопки рандомные картинки
            self.field[i].setStyleSheet(f"image: url(images/play_buttons/{i + 1}/{randint(1, 3)}.png);"
                                        "background-color: Transparent;")

    def restart(self):
        # рестарт
        self.statusBar.clearMessage()  # чистим статус бар
        """перемешивание пятнашек"""
        btn = self.sender()  # для анимации
        if btn == self.restart_btn:
            if self.game_is_started:
                self.animation_of_button(btn, position="restart")
            else:
                self.animation_of_button(btn, position="start")
        # всякие параметры
        self.won = False
        self.you_win_label.hide()
        self.timer_create()
        self.intervals_of_stopping = []
        self.count_of_steps = 0
        self.game_is_started = True
        self.display_steps()
        self.moves.clear()
        self.progressBar.setValue(0)
        # тут генерируется такое поле которое можно собрать вообще
        is_generated = False  # еще не сгенерировано
        while not is_generated:  # пока поле не сгенерировано генерируем его
            shuffle(self.field)  # мешаем
            # проверяем на случай если рандомная мешалка собрала пятнашки хотя шансы этого стремятся к нулю
            if self.field != [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9,
                              self.l10, self.l11, self.l12, self.l13, self.l14, self.l15, self.empty]:
                # генерируется все по какой то формуле которую я нашел в интернете
                pos_of_empty_btn = self.field.index(self.empty)  # позиция пустой кнопки
                # записываем строку в которой стоит пустая кнопка
                if pos_of_empty_btn <= 3:
                    pos_of_empty_btn = 1
                elif 3 < pos_of_empty_btn <= 7:
                    pos_of_empty_btn = 2
                elif 7 < pos_of_empty_btn <= 11:
                    pos_of_empty_btn = 3
                else:
                    pos_of_empty_btn = 4
                control_sum = 0  # контрольная которая нужна в формуле
                for i in range(15):  # проходимся по всем кнопкам
                    number1 = self.field_values[self.field[i]]  # получаем цифру кнопки
                    if number1 != 0:  # если это не пустая кнопка
                        for j in range(i + 1, 16):  # проходимся по всем кнопкам которые впереди этой кнопки
                            number2 = self.field_values[self.field[j]]  # цифра второй кнопки
                            if number2 != 0:  # если это не пустая
                                if number1 > number2:
                                    control_sum += 1  # если исходная кнопка больше этой увеличиваем их количество
                control_sum += pos_of_empty_btn  # прибавляем строку на которой находится пустая кнопка
                if control_sum % 2 == 0:  # если контрольная сумма четная пятнашки можно собрать
                    is_generated = True
                # формула состоит так нам нужно пройтись по всем пятнашкам посчитать количетсво пятнашек меньше этой
                # потом посчитать так для всех пятнашек прибавить строку пустой кнопку и еслиэто четно то пятнашки можно
                # собрать
        for i in range(16):  # ставим кнопки на свои места
            x, y = self.positions[i]
            self.field[i].move(x, y)
        self.checking_for_progress_bar()  # проверяем на процент собранности на
        # случай если при перемешке уже часть собрана

    def volume(self):  # включаем выключаем звук
        btn = self.sender()  # для анимации
        if btn == self.volume_btn:
            if self.volume_is_on:
                self.animation_of_button(btn, position="on")
            else:
                self.animation_of_button(btn, position="off")
        self.volume_is_on = not self.volume_is_on  # меняем звук

    def settings(self):
        btn = self.sender()  # для анимации
        if btn == self.settings_btn:
            self.animation_of_button(btn)
        self.previousIndex = 1  # для корректного возращения назад
        if self.game_is_started and self.timer_is_started:
            self.stop_timer()  # если игра начата таймер останавливается
        windows.setCurrentIndex(2)  # переходим на найстройки

    def back_menu(self):
        # кнопка возращения на стартовый экран
        btn = self.sender()  # для анимации
        if btn == self.back_menu_btn:
            self.animation_of_button(btn)
        warning = QMessageBox()  # предупреждение
        warning.setIcon(QMessageBox.Warning)
        if self.language == "us":
            warning.setWindowTitle("Error")
        elif self.language == "ru":
            warning.setWindowTitle("Ошибка")
        ok = warning.addButton(QMessageBox.Ok)
        cancel = warning.addButton(QMessageBox.Cancel)
        ok.setFont(QFont("Comic Sans MS", 10))
        ok.setStyleSheet("background-color: rgb(210, 217, 255);")
        ok.clicked.connect(self.sound)
        ok.clicked.connect(self.if_button_ok)
        cancel.setFont(QFont("Comic Sans MS", 10))
        cancel.setStyleSheet("background-color: rgb(210, 217, 255);")
        cancel.clicked.connect(self.sound)
        warning.setStyleSheet("background-color: rgb(149, 181, 255);")
        warning.setFont(QFont("Comic Sans MS", 10))
        if self.language == "us":
            warning.setText(self.warnings2[0])
        if self.language == "ru":
            warning.setText(self.warnings2[1])
        warning.exec_()

    def if_button_ok(self):
        # если в предупреждении игрок нажал ок чистим бд
        self.cur.execute("""
                        DELETE FROM score
                        """)
        self.con.commit()
        self.new_game()  # обновляем все поле
        windows.setCurrentIndex(0)  # переходим на стартовый экран

    def show_dialog(self):
        # показ типсов
        btn = self.sender()
        if self.game_is_started and self.timer_is_started:
            self.stop_timer()  # если игра начата таймер останавливается
            self.timer_is_started = False
        if self.sender() == btn:
            self.animation_of_button(btn)
        self.info.exec_()

    def save(self):
        # сохранение уже существующей игры можно делать по шорткату
        if self.is_game_opened:  # если игра открыта то в нее сохраняем текующую игру
            self.con.backup(target=self.opened_con)
        else:
            # если же нет говорим что сначала нужно сохранить игра
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
                warning.setText(self.warnings3[0])
            if self.language == "ru":
                warning.setText(self.warnings3[1])
            warning.exec_()

    def save_as(self):
        # сохранить как сохраняем несуществующую игру
        # можно сохранить и существующую
        file_path = QFileDialog.getSaveFileName(  # игрок выбирает игру либо вводит новое название
            self, 'Выбрать картинку', 'games',
            'БД (*.sqlite3)')[0]
        my_game_path = ''
        backslash = r"\ "  # также как в открытии
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
        elif len(file_path) != 0:  # сохраняем
            self.con2 = sqlite3.connect(file_path)
            self.con.backup(target=self.con2)
            self.is_game_opened = True
            self.opened_con = self.con2


class SettingsScreen(QMainWindow, Ui_MainWindow_Settings):
    # настройки
    def __init__(self, app_, main_window, start_window):
        super().__init__()
        self.initUI(app_, main_window, start_window)

    def initUI(self, app_, main_window, start_window):
        self.setupUi(self)
        # всякие параметры
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
        # возвращение на предыдущий экран для этого нужна переменная предыдущий экран
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

    def refresh_speed_value(self):  # обновление скорости кнопок
        self.main_window.speed_of_play_buttons = self.speed_spin_box.value()

    def change_language(self, text):  # смена языка
        if text == "Русский":
            self.main_window.language = "ru"
        elif text == "English":
            self.main_window.language = "us"
        # везде обновляем язык
        self.refresh_language()
        self.main_window.refresh_language()
        self.start_window.refresh_language()

    def back_animation_refresh(self, text):  # обновление анимации хода назад
        self.main_window.animation_back_move_btn = (text == "Yes" or text == "Да")

    def cheats(self):  # читы
        self.main_window.cheats_on = not self.main_window.cheats_on

    def refresh_language(self):  # обновление языка
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
    # так как мы по сути закрываем стак виджет мы должны приравнять события закрытия
    windows.addWidget(start_screen)  # начальный экран
    windows.addWidget(play_screen)  # основной экран
    windows.addWidget(settings_screen)  # настройки
    windows.setWindowIcon(QIcon("images/icons/icon.png"))
    windows.setWindowTitle("15Puzzle")
    windows.setFixedSize(1063, 685)

    windows.show()
    sys.exit(app.exec())
