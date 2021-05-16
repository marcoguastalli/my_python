class A:
    def mro(self):
        print("A")


class B(A):
    def mro(self):
        print("B")


def main():
    instance = B()
    instance.mro()  # will render B


if __name__ == "__main__":
    main()
