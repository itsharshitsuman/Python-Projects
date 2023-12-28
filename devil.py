# Importing required libraries
from bardapi import BardCookies
import datetime
import pyperclip
import pyautogui
import webbrowser
from time import sleep
import json
import keyboard
import speech_recognition as sr
import pyttsx3
from PyQt5 import QtWidgets, QtGui, QtCore

class DevilAssistantGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Initialize Bard API
        self.bard = None

        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Devil")
        self.resize(894, 580)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-22, -5, 911, 561))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("D:/make-an-ai-assistant-logo-with-dark-background-158959992.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 463, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.run_assistant)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 463, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.exit_assistant)
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 30, 411, 211))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("D:/Jarvis_Loading_Screen.gif"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 894, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Devil", "Devil Assistant"))
        self.pushButton.setText(_translate("Devil", "Run"))
        self.pushButton_2.setText(_translate("Devil", "Exit"))

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio).lower()
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

    def run_assistant(self):
        # Assistant introduction
        self.speak("Hello, I am Devil. How can I assist you?")

        # Get cookies
        cookie_dict = {
            "__Secure-1PSID": "dwg1uQj4sXOGZB_59XMh1QtmDnwZwQrehOEMJMQPCAF9okPEQg_0GC6_7tAyuAt1sR5_BQ.",
            "__Secure-1PSIDTS": "sidts-CjEBPVxjSj86LkjzCs0NVTKbOdVshOm6vnbEIDaSMDGQO8AddwhteU-xU3mEq2sI2uqcEAA",
            "__Secure-1PSIDCC": "ABTWhQEyUzax2C3x7Ern9gUmNKhGPrg0iIH5KgnvZU70yYnGrA8Y-gatPS4U9DGmWgfn_SItXw"
        }
        self.bard = BardCookies(cookie_dict=cookie_dict)

        # Main Execution
        while True:
            # Get user query
            query = self.listen()

            # Check for stop command
            if "stop" in query:
                self.speak("Goodbye!")
                break

            # Get response from Bard API
            results = self.bard.get_answer(query)['content']

            # Generate filename based on timestamp
            current_datetime = datetime.datetime.now()
            formatted_time = current_datetime.strftime("%H%M%S")
            filenamedate = str(formatted_time) + str(".txt")
            filenamedate = "Brain\\DataBase\\" + filenamedate

            # Save response to file and speak the response
            response_text = self.split_and_save_paragraphs(results, filename=filenamedate)
            self.speak(response_text)

    def exit_assistant(self):
        self.speak("Goodbye!")
        self.close()

    def split_and_save_paragraphs(self, data, filename):
        paragraphs = data.split('\n\n')
        with open(filename, 'w') as file:
            file.write(data)
        data = paragraphs[:2]
        separator = ', '
        joined_string = separator.join(data)
        return joined_string

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    devil_gui = DevilAssistantGUI()
    devil_gui.show()
    sys.exit(app.exec_())
