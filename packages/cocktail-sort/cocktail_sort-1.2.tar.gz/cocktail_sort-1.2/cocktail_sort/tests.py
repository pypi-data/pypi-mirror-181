"""модуль для тестирования функций cocktail_sort_increasing
и cocktail_sort_decreasing()"""


from op_package import cocktail_sort_increasing
from op_package import cocktail_sort_decreasing


class TestClass:
    def test_1(self):
        assert cocktail_sort_decreasing([]) == []

    def test_2(self):
        assert cocktail_sort_decreasing([]) == []

    def test_3(self):
        assert cocktail_sort_increasing([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_4(self):
        assert cocktail_sort_increasing([4, 3, 5, 1, 2]) == [1, 2, 3, 4, 5]

    def test_5(self):
        assert cocktail_sort_decreasing([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]

    def test_6(self):
        assert cocktail_sort_decreasing([4, 3, 5, 1, 2]) == [5, 4, 3, 2, 1]

