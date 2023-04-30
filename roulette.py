from random import choice


balance = 1000  # баланс
bet = 100  # ставка
picked_color = '#FF0000'  # выбранный цвет из блока выбора
win = 0
color = ''
number = 0
all_nums = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23,
            10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3,
            26]
black_nums = [15, 4, 2, 17, 6, 13, 11, 8, 10, 24, 33,
              20, 31, 22, 29, 28, 35, 26]  # номера чёрных
red_nums = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
#  номера красных
green_nums = [0]  # зеро (зелёная)
if 0 < bet <= balance:  # проверка ставки
    number = choice(all_nums)  # выбор номера
    if number in black_nums:  # цвет по номеру
        color = '#808080'
    elif number in red_nums:
        color = '#FF0000'
    elif number in green_nums:
        color = '#008000'
    if picked_color == color and color == '#808080':  # проверка на выигрыш
        win = bet * 2
    elif picked_color == color and color == '#FF0000':
        win = bet * 3
    elif picked_color == color and color == '#008000':
        win = bet * 20
    else:
        win = -bet
else:
    print('неверная ставка или недостачно средств')
balance += win
print(balance, win, color, picked_color, number)
