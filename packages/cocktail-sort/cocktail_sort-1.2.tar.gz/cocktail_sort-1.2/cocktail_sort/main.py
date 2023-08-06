"""Простой интерфейс для демонстрации"""


import argparse
import pytest
from op_package.cocktail_sort import random_list
from op_package.cocktail_sort import cocktail_sort_increasing
from op_package.sort_descending import cocktail_sort_decreasing


def main():
    """Аргументы CLI, возможные варианты сортировки перемешиванием"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--increasing',
        type=bool,
        action=argparse.BooleanOptionalAction,
        help='Сортировка по возрастанию'
    )
    parser.add_argument(
        '-d',
        '--decreasing',
        type=bool,
        action=argparse.BooleanOptionalAction,
        help='Сортировка по убыванию')
    parser.add_argument(
        '-t',
        '--test',
        type=bool,
        action=argparse.BooleanOptionalAction,
        help='Введите для запуска теста'
    )
    args = parser.parse_args()
    increasing = args.list
    decreasing = args.list
    test = args.test

    if test:
        if increasing or decreasing:
            print('Тестовый режим включен.')
        pytest.main(['-q', 'sort_ascending.py',
                     'sort_descending.py'])
        return

    if not (increasing or decreasing):
        print('Введите один параметр: -i, -d, -t')

    if increasing and not decreasing:
        received_list = random_list()
        print('Список: ', received_list)
        print(' '.join(map(str, cocktail_sort_increasing(received_list))))

    if not increasing and decreasing:
        received_list = random_list()
        print('Список: ', received_list)
        print(' '.join(map(str, cocktail_sort_decreasing(received_list))))

    if increasing and decreasing:
        print('Введено два параметра, вы получите список, '
              'отсортированный по возрастанию ')
        received_list = random_list()
        print('Список: ', received_list)
        print(' '.join(map(str, cocktail_sort_increasing(received_list))))


if __name__ == '__main__':
    main()
