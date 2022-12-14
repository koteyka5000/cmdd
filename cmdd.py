import tkinter as tk
from socket import socket, AF_INET, SOCK_STREAM
from tkinter import messagebox as mb
from colorama import init, Fore
from pyperclip import copy as pyperCopy
init(autoreset=False)
try:
    import commands
except Exception:
    mb.showwarning('Не найден файл', "Не найден файл с командами, доступны только основные команды")

# Константы (Можно менять)

COMMANDS_WIFI = ('wifi',)  # Команды, для которых нужен выход в localhost
DEFAULT_COMMANDS = 'cls', 'kill'
TIME_TO_SCROLL = 50     # Время для анимации плавного вывода. По умолчанию 50
err_count = 1  # Используется при закрытии программы во время печати (Забей)
isConnect = False  # Осуществлять выход в локальную сеть как сервер?
isDebug = 1    # Режим вывода ошибок в терминал cmdd

# Настройки окна Ткинтера
# ==========================

# По умолчанию: 400x300 (1000х600)
ROOT_SIZE_X = 1000  # Длинна в пикселях
ROOT_SIZE_Y = 600   # Высота в пикселях

# Рекомендуемые значения
DEFAULT_SIZES_X = {400: 45, 700: 82, 1000: 120}  # ROOT_SIZE_X: WIDTH_OUTPUT_X
DEFAULT_SIZES_Y = {300: 11, 600: 30}             # ROOT_SIZE_Y: WIDTH_OUTPUT_Y

# Тема
THEME = 'dark'  # dark / light

# ==========================


# Важные переменные (Нельзя менять)

TIME_TO_SCROLL_DEFAULT = TIME_TO_SCROLL + 0  # Исользуется, чтобы откатить время при использовании аттрибута --fast (Строка 104)
is_copy = False


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


if THEME == 'dark':
    BG_COLOR = 'gray'
    BG_OUTPUT_COLOR = 'gray60'
elif THEME == 'light':
    BG_COLOR = 'cyan'
    BG_OUTPUT_COLOR = 'white'
else:  #  Кастомная тема
    BG_COLOR = ''            # Цвет фона
    BG_OUTPUT_COLOR = ''     # Цвет консоли для вывода


root = tk.Tk()
root.geometry(f'{ROOT_SIZE_X}x{ROOT_SIZE_Y}')
root['bg'] = BG_COLOR
root.title('Cmd')
root.resizable(False, False)

inputTextVar = tk.StringVar(root)

if ROOT_SIZE_X in DEFAULT_SIZES_X:
    WIDTH_OUTPUT_X = DEFAULT_SIZES_X[ROOT_SIZE_X]
else:
    WIDTH_OUTPUT_X = int(ROOT_SIZE_X / 8.98888)

if ROOT_SIZE_Y in DEFAULT_SIZES_Y:
    WIDTH_OUTPUT_Y = DEFAULT_SIZES_Y[ROOT_SIZE_Y]
else:
    WIDTH_OUTPUT_Y = int(ROOT_SIZE_Y / 27.2727272727)

outputText = tk.Text(root, height=WIDTH_OUTPUT_Y, width=WIDTH_OUTPUT_X, state=tk.DISABLED, bg=BG_OUTPUT_COLOR)
outputText.place(x=20, y=100)

inputText = tk.Entry(root, textvariable=inputTextVar, width=50)
inputText.place(x=20, y=30)





def run(commandIn):  # Распределитель команд
    global TIME_TO_SCROLL
    command = commandIn.split()
    command, *args = command

    if command in COMMANDS_WIFI and isConnect == False: # Проверяем, есть ли подключение для особых команд
        return 'ERR: Для данной команды необходин доступ в localhost'

    if command[0] == '>':  # Ожидание перед выполнением команды (Пример: >4 shampoo... перед выполнение будет задержка 4 сек) 
        root.after(int(command[1:]) * 1000)  # Секунды -> миллисекунды
        command, *args = args

    if command in DEFAULT_COMMANDS:  # Если команда входит в стандартные
        output = eval(f'_cmd_{command}({args})')  # Вызываем её
    else:  # Если команда не входит в стандартные
        output = connect(command, *args)  # Выполняем команду

    if type(output) == tuple:
        result = output[0]
        arg = output[1]
        if arg == '--fast':
            TIME_TO_SCROLL = 15
        if is_copy:
            pyperCopy(result)
        return result

    if is_copy:
        pyperCopy(output)
    return output

# Сборник команд по умолчанию

def _cmd_cls(*args):
        outputText.configure(state='normal')
        outputText.delete(1.0, tk.END)
        outputText.configure(state='disabled')
        inputText.delete(0, tk.END) 
        inputText.focus()
        return ''
    
def _cmd_kill(*args):
        if isConnect:      # Если подключались к сети
            s.close()      # Закрываем соединение
        kill(1)            # Закрываем приложение


def connect(command, *args):  # Обработка команд
    if isDebug:
        return eval(f"commands._{command}(*{args}, globals())")  # Система запуска команды из другого файла
    else:
        try:
            return eval(f"commands._{command}(*{args}, globals())")  # Система запуска команды из другого файла 
        except Exception as e:
            return 'IncorrectCommandError'   # В противном случае подробно ошибку не выводим


def kill(event):  # Выход
    exit(0)


def beautifulPrint(text):  # Красивый вывод
    global TIME_TO_SCROLL, TIME_TO_SCROLL_DEFAULT
    if text == '':  # Если cls
        return      # Закрываем функцию
    for letter in text:
        root.after(TIME_TO_SCROLL)
        write(letter)
        root.update()
    write('\n')
    TIME_TO_SCROLL = TIME_TO_SCROLL_DEFAULT + 0


def write(text):  # Запись в текстовое поле
    try:
        outputText.configure(state=tk.NORMAL)
        outputText.insert(tk.END, text)
        outputText.configure(state=tk.DISABLED)
    except Exception:
        global err_count
        print(f'{Fore.RED}Отключение во время печати {Fore.CYAN}<{err_count}>')
        err_count += 1

#  start -> run -> connect
def start(event=None):  # Запуск комманды
    command = inputTextVar.get()
    if len(command) == 0:
        output = 'EmptyStringError'
    else:
        output = run(command)
    beautifulPrint(output)

def clsInput(event=None):
    inputText.delete(0, tk.END) 
    inputText.focus()

def copyResult(event=None):
    global is_copy
    is_copy = True
    start()

tk.Button(root, bg=BG_COLOR, text='Copy', command=copyResult).place(x=345, y=25)
root.bind('<Alt_L>', start)
root.bind('<Return>', start)
root.bind('<Escape>', kill)
root.bind('<Alt_R>', clsInput)


def on_closing():
    if isConnect:  # Если подключены
        if mb.askyesno("Предупреждение", "После выхода связь с клиентом не получится восстановить\nВыйти?"):
            print(f'{Fore.RED}Отключение')
            root.destroy()
    else:
        print(f'{Fore.RED}Отключение')
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)  # Перехват закрытия cmdd в функцию on_closing
inputText.focus()
root.mainloop()
