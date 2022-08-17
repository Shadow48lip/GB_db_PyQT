"""
 ======================= Потоки и многозадачность ============================
 ----------------------------- GUI и потоки ----------------------------------

 ------------------- Основное приложение "Поисковика" ------------------------

 Библиотека Qt имеет специальный класс QThread, представляющий собой "обёртку"
 над потоками, специфичными для конкретной платформы.

 При использовании QThread возможны два варианта:
  - создать класс-наследник QObject со всеми необходимыми функциями, а затем
    выполнить метод moveToThread(), чтобы поместить экземпляр класса в поток
     (предпочтительное решение)
  - создать класс-наследник QThread и реализовать метод run (не универсальное решение)
"""

import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot

from queue import Queue

from finder import Finder
from search_form import Ui_FinderForm


class FinderMonitor(QObject):
    """
    Класс-монитор, принимающий результаты поиска из очереди результатов
    Данный класс будет помещён в отдельный поток QThread
    """

    gotData = pyqtSignal(tuple)
    finished = pyqtSignal(int)

    def __init__(self, parent, urls, text):
        super().__init__()
        self.parent = parent
        self.urls = urls
        self.text = text
        self.res_queue = Queue()
        self.finder = Finder(self.text, self.res_queue)

    def search_text(self):
        """
        Запуск поиска.
        Поиск будет выполняться в отдельном потоке
        """

        self.finder.search_in_urls(self.urls)
        # Текущая функция будет: 
        #    - принимать результаты из очереди;
        #    - создавать сигналы для взаимодействия с GUI
        while True:
            data = self.res_queue.get()
            if data is None:
                break
            self.gotData.emit(data)
            self.res_queue.task_done()

        self.res_queue.task_done()
        self.finished.emit(0)

    def stop(self):
        self.finder.stop_search()


class ProgressDialog(QtWidgets.QDialog):
    """
    Класс GUI-формы "Поисковика"
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_FinderForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_search)
        self.ui.pushButton_2.clicked.connect(self.stop_search)
        self.monitor = None
        self.is_active = False
        self.progress = 0
        self.prog_val = 1

    @pyqtSlot(tuple)
    def update_results(self, data):
        """ Отображение результатов поиска """

        self.ui.plainTextEdit.appendPlainText("++ {} ++".format(data[0]))
        for text in data[1]:
            self.ui.plainTextEdit.appendPlainText(" " + text)
        self.ui.plainTextEdit.appendPlainText("")

    @pyqtSlot()
    def update_progress(self):
        """ Изменение строки прогресса """

        self.progress += self.prog_val
        self.ui.progressBar.setValue(int(self.progress))

    def stop_search(self):
        """ Остановка поиска """

        if self.monitor is not None:
            self.is_active = False
            self.monitor.stop()

    def finished(self):
        """ Действия при завершении поиска """

        self.is_active = False
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.setEnabled(True)
            
    def start_search(self):
        """ Запуск поиска """

        if not self.is_active:
            self.ui.plainTextEdit.clear()
            self.is_active = True
            urls = self.ui.plainTextEdit_2.toPlainText().split('\n')
            text = self.ui.lineEdit.text()

            # Сброс значения прогресса и вычисление единицы прогресса
            self.progress = 0
            self.prog_val = 100 / len(urls)

            self.monitor = FinderMonitor(self, urls, text)
            self.monitor.gotData.connect(self.update_results)
            self.monitor.gotData.connect(self.update_progress)

            # Создание потока и помещение объекта-монитора в этот поток
            self.thread = QThread()
            self.monitor.moveToThread(self.thread)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton.setEnabled(False)

            # ---------- Важная часть - связывание сигналов и слотов ----------
            # При запуске потока будет вызван метод search_text
            self.thread.started.connect(self.monitor.search_text)

            # При завершении поиска необходимо завершить поток и изменить GUI    
            self.monitor.finished.connect(self.thread.quit)
            self.monitor.finished.connect(self.finished)

            # Завершение процесса поиска по кнопке "Остановить"
            self.ui.pushButton_2.clicked.connect(self.monitor.stop)

            # Запуск потока, который запустит self.monitor.search_text
            self.thread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    progress = ProgressDialog()
    progress.show()
    sys.exit(app.exec_())
