"""
Модуль для сортировки чисел методом подсчета

Используется для сортировки чисел на основании данных,
полученных в модуле data_input

Ф-я counting_sort - сортировка чисел методом подсчета
"""


def counting_sort(digits: list) -> list:
    """
    Функция для сортировки чисел методом подсчета
    :param digits: список чисел, которые нужно отсортировать
    :return: list, отсортированный список чисел
    """
    min_value = min(digits)
    max_value = max(digits)
    support = [0 for _ in range(max_value - min_value + 1)]
    for element in digits:
        support[element - min_value] += 1
    index = 0
    for i, sup in enumerate(support):
        for element in range(sup):
            digits[index] = i + min_value
            index += 1
    return digits
