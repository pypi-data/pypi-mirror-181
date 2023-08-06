"""Модуль, содержащий функцию cocktail_sort_increasing()
для сортировки перемешиванием по убыванию"""


def cocktail_sort_decreasing(sequence):
    """Алгоритм сортировки перемешиванием (по убыванию)"""
    left_border = 0
    right_border = len(sequence) - 1
    control = right_border

    while left_border < right_border:
        for i in range(left_border, right_border):
            if sequence[i] < sequence[i + 1]:
                sequence[i], sequence[i + 1] = \
                    sequence[i + 1], sequence[i]
                control = i
        right_border = control

        for i in range(right_border, left_border, -1):
            if sequence[i] > sequence[i - 1]:
                sequence[i], sequence[i - 1] = \
                    sequence[i - 1], sequence[i]
                control = i
        left_border = control

    return sequence


if __name__ == '__main__':
    import doctest
    doctest.testmod()
