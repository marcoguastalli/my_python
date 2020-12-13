def question():
    print("Do you know who is zero2? yes/no")
    answer = input()
    process__answer(answer)


def process__answer(answer):
    if answer is None:
        print("Invalid answer!")
    elif answer == "yes":
        print("She is the character of which anime?")
    elif answer == "no":
        print("She is the character of an anime.")
    return True
