"""Модуль с примерами работы"""

from op_package import cocktail_sort_increasing
from op_package import cocktail_sort_decreasing

print('Пример 1')
list_1 = [-5, 12, -8, -6, 1, 2]
print(list_1)
print(cocktail_sort_increasing(list_1))

print('Пример 2')
list_2 = [8, 1, 11, -4, -6, -11]
print(list_2)
print(cocktail_sort_increasing(list_2))

print('Пример 3')
list_3 = [-7, -10, 12, -11, 4, -12]
print(list_3)
print(cocktail_sort_increasing(list_3))

print('Пример 4')
list_4 = [6, 9, -2, 4, 5, 1]
print(list_4)
print(cocktail_sort_decreasing(list_4))

print('Пример 5')
list_5 = [-8, -3, 8, -1, 1, 7]
print(list_5)
print(cocktail_sort_decreasing(list_5))

print('Пример 6')
list_6 = [4, -1, 10, -12, 8, -6]
print(list_6)
print(cocktail_sort_decreasing(list_6))