"""
Основной модуль для выполения следующих действий:
- запуск функции сортировки подсчетом;
- запуск тестов pytest;
- запуск тестов doctest.

Использует интерфейс командной строки соответственно:
>python __main__.py sort
>python __main__.py pytest
>python __main__.py doctest

doctest:
>>> counting_sort([345, -768, 0, 44])
[-768, 0, 44, 345]
>>> counting_sort([1689, 67, -56556, -9])
[-56556, -9, 67, 1689]
"""
import argparse
import doctest
import pytest
from .counting_sort import counting_sort
from .data_input import data_input


def main():
    """
    Реализация командного линейного интерфейса
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str)
    args = parser.parse_args()
    match args.mode:
        case 'sort':
            digits = data_input()
            print(counting_sort(digits))
        case 'pytest':
            pytest.main(['-v'])
        case 'doctest':
            doctest.testmod()
        case _:
            print('Такой опции нет!')


if __name__ == '__main__':
    main()
