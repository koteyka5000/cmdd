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

def _encry(*args):
    from random import randint
    try:
        text = args[0]
    except Exception:
        return 'SyntaxError'

    alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", 
            "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", " "]

    publisher = text # исходный текст
    res = '' # блок в шестнадцатиричной системе
    block = '' # строка блоков
    key_dec = '' # строка ключей в dec
    key = '' # ключ 
    chain = '' # это итоговая цепочка
    count = 0 # первый счетчик для перебора букв и их намеров
    method = 0.00 # переменная для превращения каждого элемената в ирацианально число
    spam = 0 # блок в восьмеричной/десятичной системе
    rand1 = 0 # случайное число
    temp = [] # список для записи чисел после деления на π
    subsequence = [] # список с исходными намерами букв домноженый на 1000
    randl1 = [] # список ключей
    aelist = [] # список блоков
    pi = 3.141592653589793 # π

    #Перевод чисел в числовую последовательность по афавиту с коофициентом 1000
    def translation(count, subsequence):
        for i in publisher:
            while i != alphabet[count]:
                count +=1
            if i == alphabet[count]:
                subsequence.append((count+1)*1000)
                subsequence.append(0)
                count = 0

    # деление на π и округление до целого числа с кооффициентом 100
    def irationality(subsequence, method, temp):
        for y in subsequence:
            if y != 0:
                method = y/pi
                temp.append(round(method*100))
                #temp.append(0)

    # шифрование блоков и генерация ключей        
    def rationality(temp, rand1, randl1, spam, res, aelist):
        for u in temp: # u это один блок
            rand1 = randint(3,9) # рандомное число
            randl1.append(rand1) # добавляем это число в список 
            spam = int(oct(u)[2:]) # переводим u в восьмеричную систему
            spam = spam*rand1 # домнажаем на это то рандомное число
            spam = int(oct(spam)[2:]) # переводим это обратно в восьмеричную систему
            res = f'{spam:x}' # и теперь как десятичеую переводим в шестнадцатиричную
            aelist.append(res) # добавляем этот блок в список
    

    # Запуск системы

    def start():     
        translation(count=count, subsequence=subsequence)
        irationality(subsequence=subsequence, method=method, temp=temp)
        rationality(temp=temp, rand1=rand1, randl1=randl1, spam=spam, res=res, aelist=aelist)
        

    start()
    # генерация цепи              
    for t in randl1:
        key_dec += str(t)

    for z in aelist:
        block += str(z)
                    
    key = f'{int(key_dec):x}'
    chain = str(block) + ':' + str(key)
    return chain

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

