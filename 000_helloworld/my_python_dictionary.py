# https://www.programiz.com/python-programming/dictionary
def main():
    my_dictionary = {'name': 'Marco', 'number': 27}
    print(type(my_dictionary))
    print(my_dictionary)
    print(type(my_dictionary['name']))
    print(len(my_dictionary))

    print("%s %s" % (my_dictionary['name'], my_dictionary['number']))

    my_dictionary['new_property'] = my_dictionary.pop('number')
    print(my_dictionary)

    # del() is a predefined funcion like print()
    del (my_dictionary['new_property'])
    print(my_dictionary)
    print(len(my_dictionary))


if __name__ == "__main__":
    main()
