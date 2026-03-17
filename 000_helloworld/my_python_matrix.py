# https://www.programiz.com/python-programming/list-comprehension
def main():
    matrix = [[1, 2, 3, 4], [4, 5, 6, 8]]

    result_using_double_for = []
    for i in range(len(matrix[0])):
        internal_list = []
        for row in matrix:
            internal_list.append(row[i])
        result_using_double_for.append(internal_list)
    print(result_using_double_for)

    result_using_list_comprehension = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print(result_using_list_comprehension)


if __name__ == "__main__":
    main()
