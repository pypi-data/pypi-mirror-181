"""Модуль, содержащий функцию random_list()
для генерации списка со случайными значениями"""


from random import randint


def random_list():
    """Генерирует случайный список"""
    def correct_number():
        """
        Проверяет вводимое значение на корректность ввода
        Если параметр не задан, то функция не выполнится
        Параметры:
            value (int):
                вводимое значение
        """
        while True:
            try:
                value = int(input('Введите целое положительное число: '))
                if value > 0:
                    break
                else:
                    print('Введенное число не является положительным.')
            except ValueError:
                print('Введенное число не является целым.')

        return value

    roster = []
    list_length = correct_number()

    while len(roster) < list_length:
        element = randint(-list_length * 2, list_length * 2)

        if element not in roster:
            roster.append(element)

    return roster


if __name__ == '__main__':
    random_list()
