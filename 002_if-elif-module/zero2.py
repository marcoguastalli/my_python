def main():
    return question()


def question():
    print("Do you know who is zero2? yes/no")
    answer = input()
    process__answer(answer)


def process__answer(answer):
    if answer is None:
        print("Invalid answer!")
    elif answer == "yes":
        return process__yes()
    elif answer == "no":
        print("She is the character of an anime.")
    return True


def process__yes():
    print("She is the character of which anime?")
    answer = input()
    if answer != "Darling in the Franxx":
        print("Wrong Answer")
    else:
        print("Congrats!")
    return True


if __name__ == "__main__":
    main()
