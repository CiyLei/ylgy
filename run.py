from main import *

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            sleep(2)