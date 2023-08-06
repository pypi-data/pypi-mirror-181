"""
Модуль для создания списка чисел

В этом пакете используется для исполнения функции counting_sort

Ф-я data_input - сортировка чисел методом подсчета
"""


def data_input():
    """
    Функция для ввода значений
    :return: list, список введенных чисел
    """
    flag = 1
    numbers_mas = []
    while flag != 0:
        try:
            numbers_mas = list(map(int, input('Введите числа для сортировки: ').split()))
            if numbers_mas:
                flag = 0
            else:
                print('Вы ничего не ввели!')
        except ValueError:
            print('Некорректный ввод!')
    return numbers_mas
