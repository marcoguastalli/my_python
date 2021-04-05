# https://www.programiz.com/python-programming/list-comprehension
# https://pythones.net/listas-por-comprension-python/
def main():
    even_numbers_list = [0, 2, 4, 6, 8]
    print(even_numbers_list)

    #  <Expression> for <Element> in <Iterable> if <condition>
    even_numbers_list_comprehension = [x for x in range(9) if x % 2 == 0]
    print(even_numbers_list_comprehension)

    square_list_comprehension = [x ** 2 for x in range(10)]
    print(square_list_comprehension)

    decine_list_comprehension = [y for y in range(100) if y % 2 == 0 if y % 5 == 0]
    print(decine_list_comprehension)

    even_odd_list_comprehension = ["Even" if i % 2 == 0 else "Odd" for i in range(10)]
    print(even_odd_list_comprehension)

    vocales = ['A', 'E', 'I', 'O', 'U']
    Nombres = ['Tamara', 'Marcelo', 'Martin', 'Juan', 'Alberto', 'Exequiel', 'Alejandro', 'Leonel', 'Antonio', 'Omar',
               'Antonia', 'Amalia', 'Daniela', 'Sofia', 'Celeste', 'Ramon', 'Jorgelina', 'Anabela']
    nombres_vocales = [nombre for nombre in Nombres if nombre[0] in vocales]
    print(nombres_vocales)

    lista_femeninos = [nombre for nombre in Nombres if nombre[-1] == 'a' or nombre[-1] == 'e']
    lista_masculinos = [nombre for nombre in Nombres if nombre[-1] != 'a' and nombre[-1] != 'e']
    print(lista_femeninos)
    print(lista_masculinos)


if __name__ == "__main__":
    main()
