import random


cells = {'7': '7.png', 'b': 'banana.png', 'B': 'bigwin.png',
         'c': 'cherry.png', 'd': 'drain.png', 'l': 'lemon.png',
         'o': 'orange.png', 's': 'strawberry.png',
         'w': 'watermelon.png'}
combos = {'ccc': 10, 'bbb': 15, 'ddd': 20, 'lll': 25, 'ooo': 30, 'sss': 35,
          'www': 40, '777': 50, 'BBB': 100}
drawings = ['7', 'b', 'B', 'c', 'd', 'l', 'o', 's', 'w']
balance = 1000  # из базы данных
bet = 100  # будет брать из строки ввода ставку
win = 0
result = ''
pics = []
if 0 < bet <= balance:  # прокрутка
    count = 0
    while count < 3:  # иконочка
        result += random.choice(drawings)
        count += 1
    for i in result:
        pics.append(cells.get(i))  # картиночка
    if result in combos.keys():  # проверка результата на коэф
        win = bet * combos.get(result)
    elif result.count('B') == 2:
        win = bet * 5
    elif result.count('B') == 1:
        win = bet * 2
    else:
        win = -bet
else:
    result = 'неверная ставка или недостаточно средств'
    # сообщение это в строке ввода
balance += win
print(result, pics, win, balance)
