if __name__ == "__main__":
    append_file_name = "/Users/marcoguastalli/temp/append.txt"
    with open(append_file_name, 'w+') as file:
        file.write("line one")
        file.write("\n")
        pass
    with open(append_file_name, 'a') as file:
        file.write("line two")
        pass
    with open(append_file_name, 'r') as file:
        # file.readlines() returns a list of str
        for line in file.readlines():
            print(line)
        pass
