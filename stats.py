import csv
import os
import statistics

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush
from PyQt6.QtCore import Qt


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


class StatBox(QFrame):
    def __init__(self, title, value, border_color, value_color, parent=None):
        super().__init__(parent)
        self.setObjectName("StatBox")
        self.setStyleSheet(f"""
            QFrame#StatBox {{
                background-color: rgba(30, 41, 57, 180);
                border: 1px solid {border_color};
                border-radius: 14px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        self.titleLabel = QLabel(title)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setFont(QFont("Inter", 12))
        self.titleLabel.setStyleSheet(
            "color: #99A1AF; background: transparent; border: none;"
        )

        self.valueLabel = QLabel(str(value))
        self.valueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.valueLabel.setFont(QFont("Inter", 22, QFont.Weight.Bold))
        self.valueLabel.setStyleSheet(
            f"color: {value_color}; background: transparent; border: none;"
        )

        layout.addWidget(self.titleLabel)
        layout.addWidget(self.valueLabel)

    def set_value(self, value):
        self.valueLabel.setText(str(value))


class StatsWindow(QMainWindow):
    def __init__(self, algorithm_name="Minimax"):
        super().__init__()

        self.algorithm_name = algorithm_name
        self.filename = "game_stats.csv"

        self.setWindowTitle("Spēles Statistika")
        self.setFixedSize(980, 420)

        self.initUI()
        self.load_stats()

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
        self.cardLayout.setContentsMargins(28, 24, 28, 24)
        self.cardLayout.setSpacing(22)

        self.titleLabel = QLabel("Spēles Statistika")
        self.titleLabel.setFont(QFont("Inter", 20, QFont.Weight.Medium))
        self.titleLabel.setStyleSheet("color: #FFFFFF;")
        self.cardLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(f"Algoritms: {self.algorithm_name}")
        self.subtitleLabel.setFont(QFont("Inter", 11))
        self.subtitleLabel.setStyleSheet("color: #99A1AF;")
        self.cardLayout.addWidget(self.subtitleLabel)

        boxesLayout = QHBoxLayout()
        boxesLayout.setSpacing(20)

        self.gamesBox = StatBox(
            "Kopā spēles",
            0,
            "rgba(81,162,255,120)",
            "#51A2FF"
        )
        self.nodesGenBox = StatBox(
            "Vid. ģenerētas",
            0,
            "rgba(0,255,160,120)",
            "#00F5A0"
        )
        self.nodesEvalBox = StatBox(
            "Vid. pārbaudītas",
            0,
            "rgba(194,122,255,120)",
            "#C27AFF"
        )
        self.timeBox = StatBox(
            "Vid. laiks (ms)",
            0,
            "rgba(255,153,0,120)",
            "#FF9800"
        )

        boxesLayout.addWidget(self.gamesBox)
        boxesLayout.addWidget(self.nodesGenBox)
        boxesLayout.addWidget(self.nodesEvalBox)
        boxesLayout.addWidget(self.timeBox)

        self.cardLayout.addLayout(boxesLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#101828"))
        gradient.setColorAt(0.5, QColor("#59168B"))
        gradient.setColorAt(1.0, QColor("#101828"))
        painter.fillRect(self.rect(), QBrush(gradient))

    def get_algorithm_key(self):
        if self.algorithm_name == "Minimax":
            return "minimax"
        return "alphabeta"

    def load_stats(self):
        if not os.path.isfile(self.filename):
            self.gamesBox.set_value(0)
            self.nodesGenBox.set_value(0)
            self.nodesEvalBox.set_value(0)
            self.timeBox.set_value(0)
            return

        rows = []
        algorithm_key = self.get_algorithm_key()

        with open(self.filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["algorithm"] == algorithm_key:
                    rows.append(row)

        if not rows:
            self.gamesBox.set_value(0)
            self.nodesGenBox.set_value(0)
            self.nodesEvalBox.set_value(0)
            self.timeBox.set_value(0)
            return

        games_count = len(rows)
        avg_generated = round(
            sum(int(row["generated_nodes"]) for row in rows) / games_count, 2
        )
        avg_evaluated = round(
            sum(int(row["evaluated_nodes"]) for row in rows) / games_count, 2
        )
        avg_time = round(
            sum(float(row["avg_move_time_ms"]) for row in rows) / games_count, 2
        )

        self.gamesBox.set_value(games_count)
        self.nodesGenBox.set_value(avg_generated)
        self.nodesEvalBox.set_value(avg_evaluated)
        self.timeBox.set_value(avg_time)