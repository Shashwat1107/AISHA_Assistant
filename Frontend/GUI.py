from typing import overload
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget,QLineEdit, QGridLayout,\
   QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt5.QtGui import QIcon, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get( "Assistantname" )
current_dir = os.getcwd()
old_chat_message=" "
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(Query):
    # sourcery skip: merge-else-if-into-elif, use-fstring-for-concatenation
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = [
    "what", "when", "where", "who", "whom", "whose", "which", "why","what's","where's","how's", "how",
    "is", "are", "am", "was", "were", "do", "does", "did", "can you", "could",
    "will", "would", "shall", "should", "may", "might", "have", "has", "had"
      ]

    # question_words = [
    #       "how", 'what', 'who', 'where', 'when', 'why', 'which', 'whose', 'whom', 'can you', "what's", "where's", "how's"
    # ]

    if any((word + " " in new_query) for word in question_words):
      if query_words[-1][-1] in ['.', '?', '!']:
                  new_query = new_query[:-1] + "?"
      else:
                  new_query += "?"
    else:
          if query_words[-1][-1] in ['.', '?', '!']:
                new_query = new_query[:-1] + "."
          else:
                new_query += '.'
    if("ayesha" in new_query.lower()):
          new_query = new_query.replace("ayesha", "aisha")

    return new_query.capitalize()

def SetMicrophoneStatus(Status):
    with open(rf"{TempDirPath}\Mic.data", 'w', encoding='utf-8') as file:
        file.write(Status)

def GetMicrophoneStatus():
    with open(rf"{TempDirPath}\Mic.data", 'r', encoding='utf-8') as file:
        status = file.read().strip()
    return status

def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}\Status.data", 'w', encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf"{TempDirPath}\Status.data", 'r', encoding='utf-8') as file:
        status = file.read().strip()
    return status

def MicButtonInit(): SetMicrophoneStatus("False")
def MicButtonClosed(): SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}\{Filename}"

def TempDirectoryPath(Filename):
    return rf"{TempDirPath}\{Filename}"
def ShowTextToScreen(Text):
     with open(rf"{TempDirPath}\Responses.data", 'w', encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: transparent;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDirectoryPath("AISHA_main.gif"))
        max_gif_size_W = 480; max_gif_size_H = 270
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()

        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)

        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical{
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::sub-line:vertical {
                background: black;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
            }
                           
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
    
    def loadMessages(self):
        global old_chat_message

        with open(TempDirectoryPath('Responses.data'), 'r', encoding='utf-8') as file:
            chat_message = file.read().strip()
            if chat_message is None:
                pass
            elif len(chat_message) <= 1:
                pass
            elif str(old_chat_message) == str(chat_message):
                pass
            else:
                self.addMessage(message=chat_message, color='Green')
                old_chat_message = chat_message
                
    def SpeechRecogText(self):
         with open(TempDirectoryPath('Status.data'), 'r', encoding='utf-8') as file:
            msgs = file.read().strip()
            self.label.setText(msgs)
    
    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
         
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('mic on.png'), 60, 60)
            MicButtonInit()
        else:
            self.load_icon(GraphicsDirectoryPath('mic off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled
    
    def addMessage(self, message, color='black'):
        cursor = self.chat_text_edit.textCursor()
        format1 = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10); formatm.setLeftMargin(10)
        format1.setForeground(QColor(color))
        cursor.setCharFormat(format1)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + '\n')
        self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):
     
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        gif_label = QLabel()
        movie= QMovie(GraphicsDirectoryPath("AISHA_main.gif"))
        gif_label.setMovie(movie)
        max_gif_size_H = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDirectoryPath("mic on.png"))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size: 16px; margin-bottom: 0px;")

        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), 'r', encoding='utf-8') as file:
            msgs = file.read().strip()
            self.label.setText(msgs)
    
    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('mic on.png'), 60, 60)
            MicButtonInit()
        else:
            self.load_icon(GraphicsDirectoryPath('mic off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled


class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        layout = QVBoxLayout()
        label = QLabel("Hello There!!!")

        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)

        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)

        home_button = QPushButton()
        home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("   Home")
        home_button.setStyleSheet("height:40px; line-height:40x; background-color:white; color:black")

        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("    Chat")
        message_button.setStyleSheet("height:40px; line-height:40x; background-color:white; color:black")

        minimize_button = QPushButton(); minimize_icon = QIcon(GraphicsDirectoryPath("Minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.clicked.connect(self.minimizeWindow)

        maximize_button = QPushButton(); maximize_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
        maximize_button.setIcon(maximize_icon)
        maximize_button.clicked.connect(self.maximizeWindow)

        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsDirectoryPath("Minimize2.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)

        close_button = QPushButton(); close_icon = QIcon(GraphicsDirectoryPath("Close.png"))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)

        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")

        title_label = QLabel(f" {str(Assistantname).upper()}    ")
        title_label.setStyleSheet("color:black; font-size: 18px;; background-color:white")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True; self.offset = None

    
    def minimizeWindow(self):
        self.parent().showMinimized()
        # super().showMinimized()
    def maximizeWindow(self):
        if self.parent().isMinimized():
            super().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)

        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)
    
    def closeWindow(self):
        self.parent().close()
    
    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()
    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        
        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        
        initScrn = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initScrn)
        self.current_screen = initScrn

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
    
    def initUI(self):
        desktop = QApplication.desktop()
        screen_w = desktop.screenGeometry().width()
        screen_h = desktop.screenGeometry().height()

        stacked_widget = QStackedWidget(self)
        initScrn = InitialScreen()

        msgScrn = MessageScreen()
        stacked_widget.addWidget(initScrn)
        stacked_widget.addWidget(msgScrn)

        self.setGeometry(0,0, screen_w , screen_h)
        self.setStyleSheet('background-color:black;')
        top_bar = CustomTopBar(self, stacked_widget)

        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInerface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    GraphicalUserInerface()

