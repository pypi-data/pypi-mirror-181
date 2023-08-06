import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import os


def gui_create_model(database):
    """GUI - Создание таблицы QModel, для отображения в окне программы."""
    list_users = database.getactive()
    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
    for row in list_users:
        user, ip, port, time = row
        user = QStandardItem(user)
        user.setEditable(False)
        ip = QStandardItem(ip)
        ip.setEditable(False)
        port = QStandardItem(str(port))
        port.setEditable(False)
        # Уберём миллисекунды из строки времени, т.к. такая точность не требуется.
        time = QStandardItem(str(time.replace(microsecond=0)))
        time.setEditable(False)
        list.appendRow([user, ip, port, time])
    return list


def create_stat_model(database):
    """GUI - Функция реализующая заполнение таблицы историей сообщений."""
    print('забираем из базы')
    # Список записей из базы
    hist_list = database.message_history()

    # Объект модели данных:
    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(
        ['Имя Клиента', 'Последний раз входил', 'Сообщений отправлено', 'Сообщений получено'])
    for row in hist_list:
        user, last_seen, sent, recvd = row
        user = QStandardItem(user)
        user.setEditable(False)
        last_seen = QStandardItem(str(last_seen.replace(microsecond=0))) if last_seen else QStandardItem('-')
        last_seen.setEditable(False)
        sent = QStandardItem(str(sent))
        sent.setEditable(False)
        recvd = QStandardItem(str(recvd))
        recvd.setEditable(False)
        list.appendRow([user, last_seen, sent, recvd])
    return list


class MainWindow(QMainWindow):
    """Класс основного окна сервера"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Кнопка выхода
        exitAction = QAction('Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        # Кнопка обновить список клиентов
        self.refresh_button = QAction('Обновить список', self)
        # Кнопка настроек сервера
        self.config_btn = QAction('Настройки сервера', self)

        # Кнопка вывести историю сообщений
        self.show_history_button = QAction('История клиентов', self)

        # Кнопка регистрации пользователя
        self.register_btn = QAction('Регистрация пользователя', self)

        # Кнопка удаления пользователя
        self.remove_btn = QAction('Удаление пользователя', self)

        # Статусбар
        # dock widget
        self.statusBar()

        # Тулбар
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)
        self.toolbar.addAction(self.register_btn)
        self.toolbar.addAction(self.remove_btn)

        # Настройки геометрии основного окна
        # Размер окна фиксирован потому что так быстрее.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Messaging Server alpha release')

        # Надпись о том, что ниже список подключённых клиентов
        self.label = QLabel('Список подключённых клиентов:', self)
        self.label.setFixedSize(540, 60)
        self.label.move(10, 25)

        # Окно со списком подключённых клиентов.
        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 85)
        self.active_clients_table.setFixedSize(780, 400)

        # Последним параметром отображаем окно.
        self.show()

    def create_users_model(self):
        """Метод заполняющий таблицу активных пользователей."""
        list_users = self.database.active_users_list()
        list = QStandardItemModel()
        list.setHorizontalHeaderLabels(
            ['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
        for row in list_users:
            user, ip, port, time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            # Уберём милисекунды из строки времени, т.к. такая точность не
            # требуется.
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            list.appendRow([user, ip, port, time])
        self.active_clients_table.setModel(list)
        self.active_clients_table.resizeColumnsToContents()
        self.active_clients_table.resizeRowsToContents()


class HistoryWindow(QDialog):
    """Класс окна с историей пользователей"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройки окна:
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # сбрасываем данные таблицы чтобы не сохранялись в db

        # Кнапка закрытия окна
        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close)

        # Лист с собственно историей
        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)

        self.show()


class ConfigWindow(QDialog):
    """Класс окна настроек"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройки окна
        self.setFixedSize(800, 600)
        self.setWindowTitle('Настройки сервера')

        # Надпись о файле базы данных:
        self.db_path_label = QLabel('Путь до файла базы данных: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(400, 40)

        # Строка с путём базы
        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(274, 40)
        self.db_path.move(10, 100)
        self.db_path.setReadOnly(True)

        # Кнопка выбора пути.
        self.db_path_select = QPushButton('Обзор...', self)
        self.db_path_select.move(300, 100)

        def open_file_dialog():
            """Метод обработчик открытия окна выбора папки"""
            global dialog
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            path = path.replace('/', '\\')
            self.db_path.insert(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        # Метка с именем поля файла базы данных
        self.db_file_label = QLabel('Имя файла базы данных: ', self)
        self.db_file_label.move(10, 200)
        self.db_file_label.setFixedSize(274, 40)

        # Поле для ввода имени файла
        self.db_file = QLineEdit(self)
        self.db_file.move(300, 200)
        self.db_file.setFixedSize(150, 40)

        # Метка с номером порта
        self.port_label = QLabel('Номер порта для соединений:', self)
        self.port_label.move(10, 350)
        self.port_label.setFixedSize(350, 40)

        # Поле для ввода номера порта
        self.port = QLineEdit(self)
        self.port.move(500, 350)
        self.port.setFixedSize(150, 40)

        # Метка с адресом для соединений
        self.ip_label = QLabel('С какого IP принимаем соединения:', self)
        self.ip_label.move(10, 400)
        self.ip_label.setFixedSize(350, 40)

        # Метка с напоминанием о пустом поле.
        self.ip_label_note = QLabel('* оставьте это поле пустым, чтобы принимать соединения с любых адресов.', self)
        self.ip_label_note.move(10, 425)
        self.ip_label_note.setFixedSize(800, 80)

        # Поле для ввода ip
        self.ip = QLineEdit(self)
        self.ip.move(500, 400)
        self.ip.setFixedSize(150, 40)

        # Кнопка сохранения настроек
        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(90, 520)

        # Кнопка закрытия окна
        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(275, 520)
        self.close_button.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HistoryWindow()
    # # ex = MainWindow()
    # # ex.statusBar().showMessage('Test Statusbar Message')
    # test_list = QStandardItemModel(ex)
    # test_list.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
    # test_list.appendRow([QStandardItem('1'), QStandardItem('2'), QStandardItem('3')])
    # test_list.appendRow([QStandardItem('4'), QStandardItem('5'), QStandardItem('6')])
    # ex.history_table.setModel(test_list)
    # # ex.active_clients_table.setModel(test_list)
    # # ex.active_clients_table.resizeColumnsToContents()
    # ex.history_table.resizeColumnsToContents()
    # # print('JKJKJK')
    # # app.exec_()
    # # print('END')
    # # app = QApplication(sys.argv)
    # # message = QMessageBox
    # # dial = ConfigWindow()
    #
    app.exec_()
