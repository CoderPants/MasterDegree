import re
import sys
from threading import Thread

from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
import time


class GenerateTextApp():

    def __init__(self):
        Form, Window = uic.loadUiType("main_adaptive.ui")
        self._translate = QtCore.QCoreApplication.translate
        self.model = None
        self.tokenizer = None
        self.app = QApplication([])
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)
        self.workerThread = None

    def start(self):
        self.window.show()
        self.form.btnChoseModel.clicked.connect(self.onGetPathClicked)
        self.form.btnGenerate.clicked.connect(self.onGenerateClicked)
        sys.exit(self.app.exec())

    def showError(self, text, infoText, windowTitle):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(infoText)
        msg.setWindowTitle(windowTitle)
        msg.exec_()
        self.form.etOutput.setText('')

    def onGetPathClicked(self):
        dialog = QtWidgets.QFileDialog()
        data = dialog.getExistingDirectory(self.form.centralwidget, 'Выберите папку с моделью')
        self.form.tvModelPath.setText(self._translate("MainWindow", data))

    def onGenerateClicked(self):
        self.onGenerateClickedInternal()
        # try:
        #     if self.workerThread is None:
        #         self.workerThread = Thread(target=self.onGenerateClickedInternal)
        #         self.workerThread.start()
        #     else:
        #         self.showError('Идет генерация текста!', 'Подождите, пока завершится текущая генерация текста.', 'Ошибка')
        # except Exception as e:
        #     print(e)

    def onGenerateClickedInternal(self):
        print("in onGenerateClickedInternal")
        pathToModel = self.form.tvModelPath.text()
        print('Path ' + pathToModel)
        if len(pathToModel) == 0:
            self.showError('Не указан путь к модели!', 'Выберите путь до вашей модели (Выбрать модель).', 'Ошибка')
            return

        text = self.form.etInput.toPlainText()
        if len(text) == 0:
            self.showError('Нет изначального текста!', 'Введите любой текст в поле \"Введите начальный текст\".','Ошибка')
            return

        try:
            if self.tokenizer == None:
                print('Tokenizer is none')
                self.tokenizer = GPT2Tokenizer.from_pretrained(pathToModel)
            if self.model == None:
                print('Model is none')
                self.model = TFGPT2LMHeadModel.from_pretrained(pathToModel)
            input_ids = self.tokenizer.encode(text, return_tensors='tf')
            beam_output = self.model.generate(
                input_ids,
                max_length=1000,
                num_beams=5,
                temperature=0.7,
                no_repeat_ngram_size=2,
                num_return_sequences=5
            )
            res = self.tokenizer.decode(beam_output[0])
            res = re.sub('</s>', '', res)
            self.form.etOutput.setText(res)

            print('\n\n\n' + 'Result is: ' + str(res) + '\n\n\n')
        except Exception as e:
            self.showError('Ошибка в генерации текста!', 'Проверьте путь до вашей модели','Ошибка')
            print('Exception ' + str(e))
            tokenizer = None
            model = None
        finally:
            self.workerThread = None


    def generateText(self, pathToModel, startingText):
        if self.tokenizer == None:
            print('Tokenizer is none')
            self.tokenizer = GPT2Tokenizer.from_pretrained(pathToModel)
        if self.model == None:
            print('Model is none')
            self.model = TFGPT2LMHeadModel.from_pretrained(pathToModel)
        input_ids = self.tokenizer.encode(startingText, return_tensors='tf')
        beam_output = self.model.generate(
            input_ids,
            max_length=200,
            num_beams=5,
            temperature=0.7,
            no_repeat_ngram_size=2,
            num_return_sequences=5
        )
        res = self.tokenizer.decode(beam_output[0])
        res = re.sub('</s>', '', res)
        self.form.textEdit_2.setText(res)
