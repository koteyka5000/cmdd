# globalsDict Это списк всех переменных в cmdd.py, это нужно например для взаимодействия с функциями или ткинтером
# Он передаётся как последний аргумент
# _ Нужно чтобы избежать конфликтов с другими функциями, название функции это то, что нужно будет вводить в cmd (Без _)

def checkCommand(cmd, *args):  # Проверка правильности введёной команды (Не обязательно, делается вручную)
    if cmd == 'shampoo':
        via = args[0]
        mark = args[1]
        ml = args[2]
        flush = args[3]
        return True if via == 'via' and flush == 'true' or flush == 'false' else False

    elif cmd == 'connect':
        try:
            ip = args[0]
            user = args[1]
            q = ip.split('.')
            for w in q:
                w = int(w)
                if not w <= 255 and w >= 0:
                    return False
        except Exception:
            return False
        return True

# Делать команды ниже.     _название(*args)

def _shampoo(*args):
    try:
        via = args[0]
        mark = args[1]
        ml = args[2]
        flush = args[3]
        
    except Exception:
        return 'SyntaxError1'
    if not checkCommand('shampoo', *args):  #
        return 'SyntaxError'

    if flush == 'true':
        return f'FLUSHED SHAMPOO via {mark}, {ml} Ml'
    else:
        return f'RUN SHAMPOO -> {mark}, {ml} Ml'

def _connect(*args):
    try:
        ip = args[0]
        user = args[1]
    except Exception:
        return 'SyntaxError'
    if not checkCommand('connect', *args):
        return 'connection refused! Incorrect IPv4 Adress'

    return f'connecting to {user} via IPv4: {ip}'
def _cls(*args):
    globalsDict = args[0]
    outputText = globalsDict['outputText']
    inputText = globalsDict['inputText']
    tk = globalsDict['tk']

    outputText.configure(state='normal')
    outputText.delete(1.0, tk.END)
    outputText.configure(state='disabled')
    inputText.delete(0, tk.END) 
    inputText.focus()
    return ''

def _test(*args):  # Для различных тестирований
    try:
        one = args[0]
        two = args[1]
    except Exception:
        return 'Err'
    print(f'{one}; {two} /\n{globals()}')
    return one, two

def _wifi(*args):
    try:
        user = 'uff'      # Пользователь
        action = args[0]  # on / off
        time = args[1]    # Время, на которое отключиться wifi
        wait = args[2]    # Сколько ждать перед отключение wifi
        globalsDict = args[3]
        root = globalsDict['root']
        send = globalsDict['send']
    except Exception:     # Пример:     wifi off 2 0
        return 'ERR: Синтаксис Пример: wifi off 2 0'

    if action == 'on': # Включить wifi
        send('on 0')
        return f'WiFi user={user} enabled'

    elif action == 'off': # Отключить wifi
        root.after(int(wait)*1000)       # Секунды -> миллисекунды
        print(f'Wait: {int(wait)*1000}') # Выводим сколько ждать
        send(f'off {time}')              # Посылаем запрос на отключение
        return f'WiFi user={user} disabled'

    #     return 'Что-то пошло не так'

