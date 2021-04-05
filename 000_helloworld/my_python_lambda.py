# https://www.programiz.com/python-programming/list-comprehension
def main():
    letters_list_comprehension = [letter for letter in 'human']
    print(letters_list_comprehension)

    letters_lambda = list(map(lambda x: x, 'human'))
    print(letters_lambda)


if __name__ == "__main__":
    main()
