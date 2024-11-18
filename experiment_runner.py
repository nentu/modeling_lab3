import os
import re

from my_executer import execute


def run_experiment(params: dict, n_iter, filename="code.txt", again=False):
    output_path = "./data/"
    for k, v in params.items():
        output_path += f"{k}_{v}__"
    output_path += ".res"

    print(output_path)
    if os.path.exists(output_path) and not again:
        return open(output_path, "r", encoding="utf8").read()
    code = open(filename, encoding="utf8").read()
    for key, value in params.items():
        code = code.replace(key, str(value))

    # print(code)
    result = execute(code, n_iter)

    with open(output_path, "w") as f:
        f.write(result)
    return result


if __name__ == "__main__":
    run_experiment({"E_buf": 1}, 100)
