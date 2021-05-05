import os
import sys

from app.create_table import CreateTable


def main():
    print("sqlite3")
    create_table = CreateTable()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
