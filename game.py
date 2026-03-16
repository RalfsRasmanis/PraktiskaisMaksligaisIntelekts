import time, statistics

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush
from PyQt6.QtCore import Qt, QTimer

from engine import (
    generate_random_numbers, apply_move_multiplayer, game_end,
    change_player, best_move, get_ai_move, minimax_stats,
    alphabeta_stats, save_game_stats_to_csv
)

from stats import StatsWindow


class Card(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setStyleSheet("""
            QFrame#Card {
                background-color: rgba(30, 41, 57, 230);
                border: 1px solid rgba(173, 70, 255, 77);
                border-radius: 14px;
            }
        """)


class Сipari(QLabel):
    def __init__(self, value, parent=None):
        super().__init__(str(value), parent)
        self.setFixedSize(46, 46)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if value == 1:
            bg = """
                qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #AD46FF, stop:1 #F6339A
                )
            """
        else:
            bg = """
                qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4A5565, stop:1 #364153
                )
            """

        self.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                border-radius: 10px;
                color: white;
                font-family: Inter;
                font-size: 18px;
                font-weight: 700;
            }}
        """)


class PairButton(QPushButton):
    def __init__(self, index, parent=None):
        super().__init__("—", parent)
        self.index = index
        self.setFixedSize(34, 16)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(43,127,255,50);
                border: 1px solid rgba(81,162,255,130);
                border-radius: 8px;
                color: #51A2FF;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(43,127,255,90);
            }
        """)


class GameWindow(QMainWindow):
    def __init__(self, garums, kurs, alg):
        super().__init__()

        # Nemam no start window info
        self.garums = garums
        self.kurs = kurs
        self.alg = alg

        self.state = {
            "sequence": generate_random_numbers(garums),
            "scores": {
                "Cilvēks": 0,
                "Dators": 0
            },
            "current_player": kurs,
            "algorithm": alg
        }

        self.game_over = False

        self.current_game_move_times = []
        self.current_game_saved = False

        minimax_stats.reset()
        alphabeta_stats.reset()

        self.setWindowTitle("Binārā Spēle")
        self.setFixedSize(980, 640)

        self.initUI()
        self.refresh_ui()

        if self.state["current_player"] == "Dators":
            QTimer.singleShot(700, self.computer_turn)

    def initUI(self):
        self.setStyleSheet("QMainWindow { background-color: #101828; }")

        central = QWidget()
        central.setStyleSheet("background-color: transparent;")
        self.setCentralWidget(central)

        outerLayout = QVBoxLayout(central)
        outerLayout.setContentsMargins(40, 40, 40, 40)

        self.card = Card()
        outerLayout.addWidget(self.card)

        self.cardLayout = QVBoxLayout(self.card)
        self.cardLayout.setContentsMargins(24, 24, 24, 24)
        self.cardLayout.setSpacing(18)

        # HEADER
        headerLayout = QHBoxLayout()

        titleBlock = QVBoxLayout()
        titleBlock.setSpacing(2)

        self.titleLabel = QLabel("Binārā Spēle")
        self.titleLabel.setFont(QFont("Inter", 20, QFont.Weight.Medium))
        self.titleLabel.setStyleSheet("color:#FFFFFF")
        titleBlock.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel("")
        self.subtitleLabel.setFont(QFont("Inter", 10))
        self.subtitleLabel.setStyleSheet("color:#99A1AF")
        titleBlock.addWidget(self.subtitleLabel)

        headerLayout.addLayout(titleBlock)
        headerLayout.addStretch()

        # Statistikas button
        self.statsButton = QPushButton("▥ Statistika")
        self.statsButton.setFixedHeight(32)
        self.statsButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(89,22,139,77);
                border: 1px solid rgba(173,70,255,128);
                border-radius: 8px;
                color: #E9D7FE;
                padding: 0 14px;
                font-family: Inter;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(89,22,139,110);
            }
        """)
        self.statsButton.clicked.connect(self.open_stats_window)
        headerLayout.addWidget(self.statsButton)

        self.newGameButton = QPushButton("↻ Jauna")
        self.newGameButton.setFixedHeight(32)
        self.newGameButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(134,16,67,77);
                border: 1px solid rgba(246,51,154,128);
                border-radius: 8px;
                color: #FCCEE8;
                padding: 0 14px;
                font-family: Inter;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(134,16,67,110);
            }
        """)
        self.newGameButton.clicked.connect(self.go_to_start_screen)
        headerLayout.addWidget(self.newGameButton)

        self.restartButton = QPushButton("↻ Restart")
        self.restartButton.setFixedHeight(32)
        self.restartButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(21,93,252,90);
                border: 1px solid rgba(81,162,255,150);
                border-radius: 8px;
                color: #FFFFFF;
                padding: 0 14px;
                font-family: Inter;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(21,93,252,130);
            }
        """)
        self.restartButton.clicked.connect(self.restart_game)
        self.restartButton.hide()
        headerLayout.addWidget(self.restartButton)

        self.cardLayout.addLayout(headerLayout)

        # SCORES
        scoreLayout = QHBoxLayout()
        scoreLayout.setSpacing(20)

        self.humanFrame = QFrame()
        self.humanFrame.setFixedHeight(120)
        self.humanFrame.setStyleSheet("""
            QFrame{
                background: rgba(28,57,142,80);
                border: 2px solid #51A2FF;
                border-radius: 14px;
            }
        """)

        humanLayout = QVBoxLayout(self.humanFrame)
        humanLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        humanLayout.setSpacing(4)

        self.humanName = QLabel("Cilvēks")
        self.humanName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humanName.setFont(QFont("Inter", 11))
        self.humanName.setStyleSheet("""
            color:#99A1AF;
            background:transparent;
            border:none;
        """)
        self.humanName.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.humanScore = QLabel("0")
        self.humanScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humanScore.setFont(QFont("Inter", 26, QFont.Weight.Bold))
        self.humanScore.setStyleSheet("""
            color:#51A2FF;
            background:transparent;
            border:none;
        """)
        self.humanScore.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        humanLayout.addWidget(self.humanName)
        humanLayout.addWidget(self.humanScore)

        self.compFrame = QFrame()
        self.compFrame.setFixedHeight(120)
        self.compFrame.setStyleSheet("""
            QFrame{
                background: rgba(54,65,83,77);
                border: 2px solid rgba(74,85,101,77);
                border-radius: 14px;
            }
        """)

        compLayout = QVBoxLayout(self.compFrame)
        compLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        compLayout.setSpacing(4)

        self.compName = QLabel("Dators")
        self.compName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.compName.setFont(QFont("Inter", 11))
        self.compName.setStyleSheet("""
            color:#99A1AF;
            background:transparent;
            border:none;
        """)
        self.compName.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.compScore = QLabel("0")
        self.compScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.compScore.setFont(QFont("Inter", 26, QFont.Weight.Bold))
        self.compScore.setStyleSheet("""
            color:#C27AFF;
            background:transparent;
            border:none;
        """)
        self.compScore.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        compLayout.addWidget(self.compName)
        compLayout.addWidget(self.compScore)

        scoreLayout.addWidget(self.humanFrame)
        scoreLayout.addWidget(self.compFrame)

        self.cardLayout.addLayout(scoreLayout)

        # TURN LABEL
        self.turnLabel = QLabel("")
        self.turnLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turnLabel.setFixedSize(150, 36)
        self.turnLabel.setStyleSheet("""
            QLabel{
                background-color: rgba(21,93,252,204);
                border-radius: 8px;
                color:white;
                font-family: Inter;
                font-size:13px;
            }
        """)
        self.cardLayout.addWidget(self.turnLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        # BOARD
        self.boardFrame = QFrame()
        self.boardFrame.setStyleSheet("""
            QFrame{
                background-color: rgba(16,24,40,128);
                border:1px solid rgba(173,70,255,51);
                border-radius:14px;
            }
        """)

        self.boardLayout = QVBoxLayout(self.boardFrame)
        self.boardLayout.setContentsMargins(18, 18, 18, 18)
        self.boardLayout.setSpacing(12)

        self.sequenceLayout = QVBoxLayout()
        self.sequenceLayout.setSpacing(10)
        self.boardLayout.addLayout(self.sequenceLayout)

        self.remainingLabel = QLabel("")
        self.remainingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.remainingLabel.setStyleSheet("color:#99A1AF")
        self.boardLayout.addWidget(self.remainingLabel)

        self.cardLayout.addWidget(self.boardFrame)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#101828"))
        gradient.setColorAt(0.5, QColor("#59168B"))
        gradient.setColorAt(1.0, QColor("#101828"))
        painter.fillRect(self.rect(), QBrush(gradient))

    def refresh_ui(self):
        self.humanScore.setText(str(self.state["scores"]["Cilvēks"]))
        self.compScore.setText(str(self.state["scores"]["Dators"]))
        self.subtitleLabel.setText(
            f'{self.state["algorithm"]} | Garums: {len(self.state["sequence"])}'
        )
        self.remainingLabel.setText(
            f'Atlikusī virkne: {len(self.state["sequence"])}'
        )

        if game_end(self.state["sequence"]):
            self.game_over = True
            self.show_game_over()
        else:
            self.game_over = False
            self.restartButton.hide()

            if self.state["current_player"] == "Cilvēks":
                self.turnLabel.setText("Tavs gājiens")
            else:
                self.turnLabel.setText("Datora gājiens")

        self.clear_layout(self.sequenceLayout)

        # Lai visi cipari būtu vairākās rindās un nepazustu poga starp rindām
        max_per_row = 8
        start = 0
        sequence = self.state["sequence"]

        while start < len(sequence):
            rowLayout = QHBoxLayout()
            rowLayout.setSpacing(8)
            rowLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            end = min(start + max_per_row, len(sequence))

            for i in range(start, end):
                rowLayout.addWidget(Сipari(sequence[i]))

                # Pievieno pogu arī rindas beigās,
                # ja nākamais skaitlis eksistē nākamajā rindā
                if i < len(sequence) - 1:
                    btn = PairButton(i)
                    btn.clicked.connect(lambda _, idx=i: self.human_move(idx))
                    btn.setEnabled(self.state["current_player"] == "Cilvēks" and not self.game_over)
                    rowLayout.addWidget(btn)

            self.sequenceLayout.addLayout(rowLayout)
            start = end

    def human_move(self, index):
        if self.state["current_player"] != "Cilvēks" or self.game_over:
            return

        apply_move_multiplayer(
            self.state["sequence"],
            index,
            self.state["current_player"],
            self.state["scores"]
        )
        self.state["current_player"] = change_player(self.state["current_player"])

        self.refresh_ui()

        if not game_end(self.state["sequence"]):
            QTimer.singleShot(700, self.computer_turn)

    def computer_turn(self):
        if game_end(self.state["sequence"]) or self.game_over:
            return

        start_time = time.perf_counter()

        if self.state["algorithm"] == "Minimax":
            ai_scores = [
                self.state["scores"]["Cilvēks"],
                self.state["scores"]["Dators"]
            ]

            index, _ = best_move(
                self.state["sequence"],
                ai_scores,
                1,
                minimax_stats
            )
        else:
            index = get_ai_move(
                self.state["sequence"],
                self.state["scores"],
                alphabeta_stats
            )

        end_time = time.perf_counter()
        move_time_ms = (end_time - start_time) * 1000
        self.current_game_move_times.append(move_time_ms)

        apply_move_multiplayer(
            self.state["sequence"],
            index,
            self.state["current_player"],
            self.state["scores"]
        )
        self.state["current_player"] = change_player(self.state["current_player"])

        self.refresh_ui()

    def restart_game(self):
        self.state = {
            "sequence": generate_random_numbers(self.garums),
            "scores": {
                "Cilvēks": 0,
                "Dators": 0
            },
            "current_player": self.kurs,
            "algorithm": self.alg
        }
        self.game_over = False
        self.current_game_move_times = []
        self.current_game_saved = False

        minimax_stats.reset()
        alphabeta_stats.reset()

        self.restartButton.hide()
        self.refresh_ui()

        if self.state["current_player"] == "Dators":
            QTimer.singleShot(700, self.computer_turn)

    def go_to_start_screen(self):
        from start import MainWindow

        self.start_window = MainWindow()
        self.start_window.show()
        self.hide()

    def open_stats_window(self):
        self.stats_window = StatsWindow(algorithm_name=self.alg)
        self.stats_window.show()

    def show_game_over(self):
        if self.state["scores"]["Cilvēks"] > self.state["scores"]["Dators"]:
            self.turnLabel.setText("Tu uzvarēji!")
            winner = "Cilvēks"
        elif self.state["scores"]["Dators"] > self.state["scores"]["Cilvēks"]:
            self.turnLabel.setText("Dators uzvar!")
            winner = "Dators"
        else:
            self.turnLabel.setText("Neizšķirts!")
            winner = "Draw"

        avg_time = 0
        if self.current_game_move_times:
            avg_time = round(statistics.mean(self.current_game_move_times), 2)

        if not self.current_game_saved:
            if self.state["algorithm"] == "Minimax":
                algorithm_name = "minimax"
                used_stats = minimax_stats
            else:
                algorithm_name = "alphabeta"
                used_stats = alphabeta_stats

            save_game_stats_to_csv(
                "game_stats.csv",
                algorithm_name,
                winner,
                self.state["scores"],
                used_stats,
                avg_time
            )

            self.current_game_saved = True

        self.restartButton.show()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())