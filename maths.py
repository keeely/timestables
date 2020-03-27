#!/usr/bin/env python3


import sys
import random
import time
from pathlib import Path

from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QLabel, QHBoxLayout, QMessageBox
from PySide2.QtGui import  QFont, QIntValidator
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QSoundEffect

MAX_QUESTION = 39


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.sound = QSoundEffect()
        self.sound.setVolume(0.5)
        self.sound.setLoopCount(1)

        self.reset_timer()

        self.layout = QHBoxLayout()
        self.question = 0
        self.answer = -1

        self.label = QLabel()
        f = QFont("Arial", 120, QFont.Bold)
        self.label.setFont(f)
        self.layout.addWidget(self.label)
        self.edit = QLineEdit()
        self.edit.setMaxLength(3)
        self.edit.setFixedWidth(250)
        self.edit.setFont(f)
        self.edit.setValidator(QIntValidator())
        self.layout.addWidget(self.edit)

        self.setWindowTitle("")
        self.setLayout(self.layout)

        self.next_question()


    def random_from_dir(self, path):
        parent = Path(path)
        index = []
        for fname in parent.iterdir():
            index.append(fname)
        sound = index[random.randrange(len(index))]
        return sound


    def play_sound(self, path):
        sound_filepath = QUrl.fromLocalFile(str(path))
        self.sound.setSource(sound_filepath)
        self.sound.play()


    def random_good_sound(self):
        sound = self.random_from_dir("good")
        self.play_sound(sound)


    def random_bad_sound(self):
        sound = self.random_from_dir("bad")
        self.play_sound(sound)


    def reset_timer(self):
        self.play_sound("start/goodluckyoullneedit.wav")
        mbox = QMessageBox()
        mbox.setText("Time starts when you press enter")
        mbox.exec()
        self.play_sound("start/letsgo.wav")
        self.time_started = time.time()
        self.time_ending = self.time_started + 3 * 60


    def set_random_question(self):
        primary = 7
        secondary = random.randrange(13)
        order = random.randrange(2)
        if order == 0:
            self.label.setText(f"{primary} x {secondary} =")
        else:
            self.label.setText(f"{secondary} x {primary} =")
        self.answer = primary * secondary


    def set_orange_question(self, index):
        primary, secondary = orange_test_sheet[index]
        self.label.setText(f"{primary} x {secondary} =")
        self.answer = primary * secondary


    def next_question(self):

        remain = int(self.time_ending - time.time())
        if remain < 0:
            remain = 0

        if self.question != 0:
            if remain == 0:
                self.random_bad_sound()
                mbox = QMessageBox()
                mbox.setText("SORRY, you are out of time!")
                mbox.exec()
                self.reset_timer()
                remain = int(self.time_ending - time.time())
                self.question = 0

            elif int(self.edit.text()) != self.answer:
                self.random_bad_sound()
                mbox = QMessageBox()
                mbox.setText("Answer was wrong, should be %d.  Back to the start!" % self.answer)
                mbox.exec()
                self.reset_timer()
                remain = int(self.time_ending - time.time())
                self.question = 0
            else:
                self.random_good_sound()

        if self.question == MAX_QUESTION:
            mbox = QMessageBox()
            mbox.setText("You made it!")
            mbox.exec()
            sys.exit()

        self.set_random_question()
        #self.set_orange_question(self.question)

        self.edit.clear()
        self.question += 1
        self.setWindowTitle("Question %d/%d seconds remaining: %d" % (self.question, MAX_QUESTION, remain))


    def keyPressEvent(self, event):
        if event.key() == 0x1000004:
            if self.edit.text():
                self.next_question()


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
