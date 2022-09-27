# https://www.programiz.com/python-programming/list
def main():
    my_list = [
        'First',
        '2nd'
    ]
    print(type(my_list))
    print(my_list)
    print(type(my_list[0]))
    print(len(my_list))

    print("%s %s" % (my_list[0], my_list[1]))

    my_list[0] = '1st'
    print(my_list)

    # https://www.programiz.com/python-programming/methods/list/remove
    my_list.remove('2nd')
    print(my_list)
    print(len(my_list))

    print(my_list.__contains__('1st'))
    print(my_list.__contains__('2nd'))


if __name__ == "__main__":
    main()
