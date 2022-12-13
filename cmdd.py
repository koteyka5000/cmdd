import tkinter as tk
from socket import socket, AF_INET, SOCK_STREAM
from tkinter import messagebox as mb
from colorama import init, Fore
import commands
init(autoreset=False)


isConnect = False  # Осуществлять выход в локальную сеть как сервер?
isDebug = False  # Режим вывода ошибок в терминал cmdd

# Время для анимации плавного вывода. По умолчанию 50
TIME_TO_SCROLL = 50

if isConnect:
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    s = socket(AF_INET, SOCK_STREAM)  # Создается сокет протокола TCP
    s.bind(('localhost', PORT))  # Присваиваем ему порт 10000
    s.listen(10)  # Максимальное количество одновременных запросов
    print(f'{Fore.CYAN}Запрос на соединение\nПорт: {PORT}\nАдрес: {HOST}')
    client, addr = s.accept()  # акцептим запрос на соединение


def send(data):
    client.send(data.encode('utf-8'))  # передаем данные, предварительно упаковав их в байты


root = tk.Tk()
root.geometry('400x300')
root['bg'] = 'cyan'
root.title('Cmd')
root.resizable(False, False)

inputTextVar = tk.StringVar(root)

outputText = tk.Text(root, height=11, width=45, state=tk.DISABLED)
outputText.place(x=20, y=100)

inputText = tk.Entry(root, textvariable=inputTextVar, width=50)
inputText.place(x=20, y=30)

COMMANDS_WIFI = ('wifi',)

def run(commandIn):  # Распределитель команд
    command = commandIn.split()
    command, *args = command

    if command in COMMANDS_WIFI and isConnect == False: # Проверяем, есть ли подключение для особых команд
        return 'ERR: Для данной команды необходин доступ в localhost'

    if command == 'kill':  # Принудительно закрываем приложение
        if isConnect:      # Если подключались к сети
            s.close()      # Закрываем соединение
        kill(1)            # Закрываем приложение

    if command[0] == '>':  # Ожидание перед выполнением команды (Пример: >4 shampoo... перед выполнение будет задержка 4 сек) 
        root.after(int(command[1:]) * 1000)  # Секунды -> миллисекунды
        command, *args = args
    return connect(command, *args)  # Выполняем команду

def my_exec(code):  # Украденый код со stackoverflow))
    exec('global i; i = %s' % code)  # Это необходимо, чтобы получить return из exec()
    global i
    return i

def connect(command, *args):  # Обработка команд
    try:
        return my_exec(f"commands._{command}(*{args}, globals())")  # Система запуска команды из другого файла
    except Exception as e:
        if isDebug:
            return f'IncorrectCommandError ({e})'  # Выводим ошибку если включен isDebug
        return 'IncorrectCommandError'   # В противном случае подробно ошибку не выводим


def kill(event):  # Выход
    exit(144)


def beautifulPrint(text):  # Красивый вывод
    if text == '':  # Если cls
        return      # Закрываем функцию
    for letter in text:
        root.after(TIME_TO_SCROLL)
        write(letter)
        root.update()
    write('\n')


def write(text):  # Запись в текстовое поле
    outputText.configure(state=tk.NORMAL)
    outputText.insert(tk.END, text)
    outputText.configure(state=tk.DISABLED)

#  start -> run -> connect
def start(event=None):  # Запуск комманды
    command = inputTextVar.get()
    if len(command) == 0:
        output = 'EmptyStringError'
    else:
        output = run(command)
    beautifulPrint(output)


tk.Button(root, bg='cyan', text='Enter', command=start).place(x=345, y=25)
root.bind('<Alt_L>', start)
root.bind('<Return>', start)
root.bind('<Escape>', kill)


def on_closing():
    if isConnect:  # Если подключены
        if mb.askyesno("Предупреждение", "После выхода связь с клиентом не получится восстановить\nВыйти?"):
            print(f'{Fore.RED}Отключение')
            root.destroy()
    else:
        print(f'{Fore.RED}Отключение')
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)  # Перехват закрытия cmdd в функцию on_closing

root.mainloop()
