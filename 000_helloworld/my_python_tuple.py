# https://www.programiz.com/python-programming/tuple

def main():
    my_tuple_a = 1, "two", 3.3
    print(type(my_tuple_a))
    print(my_tuple_a)
    print(len(my_tuple_a))

    my_tuple_b = ("four", 'V', 6)
    print(type(my_tuple_b))
    print(my_tuple_b)
    print(len(my_tuple_b))

    print(my_tuple_a[0])
    print(my_tuple_a[-2])
    print(my_tuple_a[-1])

    my_tuple_c = my_tuple_a, my_tuple_b
    del my_tuple_a
    del my_tuple_b
    print(my_tuple_c[0:1])
    print(my_tuple_c[:])
    print(my_tuple_c[:-1])


if __name__ == "__main__":
    main()
