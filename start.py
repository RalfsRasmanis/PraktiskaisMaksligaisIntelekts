import sys
from game import GameWindow
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget,
    QVBoxLayout, QPushButton, QRadioButton,
    QButtonGroup, QSpinBox, QFrame
)
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush
from PyQt6.QtCore import Qt

# Frame for a game (struktura)
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

#The whole thing
class MainWindow(QMainWindow):
    def __init__(self): # Speles struktura
        super().__init__()
        self.setWindowTitle("Binārā Spēle")
        self.setFixedSize(820, 600)

        self.spinGarums = QSpinBox()
        self.radioCilveks = QRadioButton("Cilvēks")
        self.radioDators = QRadioButton("Dators")
        self.radioMinimax = QRadioButton("Minimax")
        self.radioAlphaBeta = QRadioButton("Alpha-Beta")

        self.buttonGroupKurs = QButtonGroup(self)
        self.buttonGroupAlg = QButtonGroup(self)

        self.btnSakt = QPushButton("▶  Sākt spēli")

        self._initUI()

    # Dizains
    def _initUI(self):
        self.setStyleSheet("QMainWindow { background-color: #101828; }")

        central = QWidget()
        central.setStyleSheet("background-color: transparent;")
        self.setCentralWidget(central)

        card = Card()
        card.setFixedSize(448, 522)

        logaIzkartojums = QVBoxLayout(central)
        logaIzkartojums.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logaIzkartojums.addWidget(card)

        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(25, 24, 25, 24)
        cardLayout.setSpacing(12)

        # Title
        labelNosaukums = QLabel("Binārā Spēle")
        labelNosaukums.setAlignment(Qt.AlignmentFlag.AlignCenter)
        labelNosaukums.setFont(QFont("Inter", 22, QFont.Weight.Medium))
        labelNosaukums.setStyleSheet("color: #FFFFFF; margin-bottom: 10px;")

        # String length
        labelGarums = QLabel("Virknes garums (15-25)")
        labelGarums.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        labelGarums.setStyleSheet("color: #D1D5DC;")

        self.spinGarums.setRange(15, 25)
        self.spinGarums.setValue(15)
        self.spinGarums.setFixedHeight(36)
        self.spinGarums.setFont(QFont("Inter", 10))
        self.spinGarums.setStyleSheet(self._spinboxStyle())

        # Who starts
        labelKurs = QLabel("Kurš sāk spēli?")
        labelKurs.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        labelKurs.setStyleSheet("color: #D1D5DC;")

        self.buttonGroupKurs.addButton(self.radioCilveks)
        self.buttonGroupKurs.addButton(self.radioDators)
        self._styleRadio(self.radioCilveks)
        self._styleRadio(self.radioDators)
        self.radioCilveks.setChecked(True)

        # Algoritms
        labelAlgoritms = QLabel("Algoritms")
        labelAlgoritms.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        labelAlgoritms.setStyleSheet("color: #D1D5DC;")

        self.buttonGroupAlg.addButton(self.radioMinimax)
        self.buttonGroupAlg.addButton(self.radioAlphaBeta)
        self._styleRadio(self.radioMinimax)
        self._styleRadio(self.radioAlphaBeta)
        self.radioMinimax.setChecked(True)

        # Start button
        self.btnSakt.setFixedHeight(40)
        self.btnSakt.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        self.btnSakt.setStyleSheet(self._startButtonStyle())
        self.btnSakt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btnSakt.clicked.connect(self._onSaktClicked)

        # Adding everything (Layout)
        cardLayout.addWidget(labelNosaukums)
        cardLayout.addSpacing(4)
        cardLayout.addWidget(labelGarums)
        cardLayout.addWidget(self.spinGarums)
        cardLayout.addSpacing(4)
        cardLayout.addWidget(labelKurs)
        cardLayout.addWidget(self.radioCilveks)
        cardLayout.addWidget(self.radioDators)
        cardLayout.addSpacing(4)
        cardLayout.addWidget(labelAlgoritms)
        cardLayout.addWidget(self.radioMinimax)
        cardLayout.addWidget(self.radioAlphaBeta)
        cardLayout.addSpacing(8)
        cardLayout.addWidget(self.btnSakt)

    # Styles
    def _styleRadio(self, radio: QRadioButton):
        radio.setFont(QFont("Inter", 10))
        radio.setFixedHeight(40)
        radio.setStyleSheet("""
            QRadioButton {
                color: #E5E7EB;
                background-color: rgba(54, 65, 83, 77);
                border-radius: 10px;
                padding-left: 12px;
                spacing: 8px;
            }
            QRadioButton:hover {
                background-color: rgba(54, 65, 83, 120);
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 1px solid #C27AFF;
                background-color: transparent;
            }
            QRadioButton::indicator:checked {
                background-color: #C27AFF;
                border: 1px solid #C27AFF;
                image: none;
            }
        """)

    def _spinboxStyle(self) -> str:
        return """
            QSpinBox {
                background-color: rgba(54, 65, 83, 128);
                color: #FFFFFF;
                border: 1px solid rgba(173, 70, 255, 77);
                border-radius: 8px;
                padding: 4px 12px;
            }
            QSpinBox:focus {
                border: 1px solid rgba(173, 70, 255, 153);
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background-color: rgba(54, 65, 83, 180);
                border-radius: 4px;
                margin: 2px 3px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: rgba(173, 70, 255, 120);
            }
            QSpinBox::up-arrow {
                image: none;
                width: 0; height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 5px solid #D1D5DC;
            }
            QSpinBox::down-arrow {
                image: none;
                width: 0; height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #D1D5DC;
            }
        """

    def _startButtonStyle(self) -> str:
        return """
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9810FA, stop:1 #E60076
                );
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                letter-spacing: -0.15px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #A930FF, stop:1 #F01088
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8508E0, stop:1 #CC0066
                );
            }
        """

    # Gradient background
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#101828"))
        gradient.setColorAt(0.5, QColor("#59168B"))
        gradient.setColorAt(1.0, QColor("#101828"))
        painter.fillRect(self.rect(), QBrush(gradient))

    # Button handlers
    def _onSaktClicked(self):
        garums = self.spinGarums.value()
        kurs = "Cilvēks" if self.radioCilveks.isChecked() else "Dators"
        alg = "Minimax" if self.radioMinimax.isChecked() else "Alpha-Beta"

        self.game_window = GameWindow(garums, kurs, alg)
        self.game_window.show()
        self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
