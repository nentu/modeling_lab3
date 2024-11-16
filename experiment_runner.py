import os
import re

from executer import execute


def run_experiment(params: dict, n_iter, filename='code.txt'):
    output_path = './data/' + str(params) + '.res'
    if os.path.exists(output_path):
        return open(output_path, 'r')
    code = open(filename, encoding='utf8').read()
    for key, value in params.items():
        code = code.replace(key, value)

    # print(code)
    result = execute(
        code, n_iter
    )

    with open(output_path, 'w') as f:
        f.write(result)
    return result


if __name__ == '__main__':
    run_experiment(
        {'E_buf': 1},
        100
    )
