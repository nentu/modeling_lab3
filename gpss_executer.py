import gpss



def execute(code, iter_n):
    gpss.parse(program=code)
    return gpss.createReport()


if __name__ == '__main__':
    f = open('code.txt', 'r', encoding='utf8').read()
    # time.sleep(2)
    print(
        execute(f, 1e6)
    )
