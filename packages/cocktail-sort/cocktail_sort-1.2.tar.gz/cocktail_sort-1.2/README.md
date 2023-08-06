# Практическая работа №6 - Модульные программы

**Эрлан Назарбеков**,
**КИ22-16/1Б**,
**Вариант 24**

`$ python example.py -v` — примеры

`$ python generate_random.py` — функция для генерации случайного списка

`$ python sort_acdending.py` — функция для сортировки перемешиванием (по возрастанию)

`$ python sort_decsending.py` — функция для сортировки перемешиванием (по убыванию)

example:

```python
from op_package import cocktail_sort_increasing

print(cocktail_sort_increasing([5, 6, 8, 3, 2, 1]))

from op_package import cocktail_sort_decreasing

print(cocktail_sort_decreasing([5, 6, 8, 3, 2, 1]))
```

`[1, 2, 3, 5, 6, 8]`

`[8, 6, 5 ,3 ,2, 1]`
