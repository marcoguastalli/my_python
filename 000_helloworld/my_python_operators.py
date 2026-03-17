# https://www.programiz.com/python-programming/operators
def main():
    a = 1
    b = 2
    print(a, b, (a + b))

    c = 5 - a
    print(c)

    d = c * 2
    print(d)

    e = d / 2
    print(e)

    f = e % 2
    print(f)

    g = 3 ** 2
    print(g)

    h = 10 // 3
    print(h)

    print(10 > 5, 10 < 5, 10 == 5, 10 != 5, 10 >= 5, 10 <= 5)

    i = 10
    j = 5
    print(i is not j)
    print(i is j)

    k = +i
    print(k)

    l = -i
    print(l)

    m = 5
    m *= 2
    print(m)

    m /= 2
    print(m)

    n = 9
    n %= 2
    print(n)

    o = 3
    o **= 2
    print(o)


if __name__ == "__main__":
    main()
