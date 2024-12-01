import math
import re
import time

import scipy.stats as sps
from tabulate import tabulate

import json
from experiment_runner import run_experiment

filename = "code.txt"

EXP_NUM = 3


def extract_f(text, rx):
    data = re.findall(rx, text, re.MULTILINE)[0]
    data = data.strip().split()
    data = list(map(float, data))
    return data


def dov(cnt, std, a=0.99):
    za = float(sps.norm.ppf(1 - a / 2))
    return za * std  # / math.sqrt(cnt)


def parse(text):
    _, _, _, _, avg_length, _, avg_wait_nonzero, _ = extract_f(text, "^ BUF1(.*)\n")
    avg_resid, std_resid, _ = extract_f(text, "^ TU_UZEL(.*)\n")
    avg_wait, std_wait, _ = extract_f(text, "^ TU_BUF(.*)\n")
    std_wait = std_wait ** 0.5
    cnt_all, _, _ = extract_f(text, "GENERATE(.*)")
    cnt_refuse, _, _ = extract_f(text, "ZYX.*TERMINATE(.*)\n")
    _, _, _, _, _, _, _, util1, _, _ = extract_f(text, "STORAGE.*\n+ UZEL(.*)\n")
    cnt_passed = cnt_all - cnt_refuse
    prb_refuse = cnt_refuse / cnt_all
    dov_wait = dov(cnt_passed, std_wait)
    dovpct_wait = dov_wait / avg_wait * 100

    return dict(
        avg_resid=avg_resid,
        std_resid=std_resid,
        avg_wait=avg_wait,
        std_wait=std_wait,
        dov_wait=dov_wait,
        dovpct_wait=dovpct_wait,
        cnt_all=cnt_all,
        cnt_passed=cnt_passed,
        cnt_refuse=cnt_refuse,
        prb_refuse=prb_refuse,
        avg_length=avg_length,
        avg_wait_nonzero=avg_wait_nonzero,
        util=util1
    )


n_file = r"C:\Users\zam12\OneDrive\Документы\university\course3\modeling\lab3\executer\docs\numbers.txt"

GEN_param_decoder = {
    'E': '(Exponential(RN_a,0,t_a))',
    'T': f'(GetRandomNumberFromFile("{n_file}"))',
    'A': 'V$Erl_2'
}

SERV_param_decoder = {
    'E': '(Exponential(RN_b,0,t_b))'
}


def simulate(inputs):
    return parse(run_experiment(inputs, inputs['iter_n'], filename=filename, again=False))


def take_cols(x, cols):
    return {k: v for k, v in x.items() if cols is None or k in cols}


def run(src_inputs, out_cols=None):
    inputs = []
    for r in src_inputs:
        inputs.append(r.copy())
        if 'GEN_param' in inputs[-1]:
            inputs[-1]['GEN_param'] = GEN_param_decoder[inputs[-1]['GEN_param']]
        if 'SERV_param' in inputs[-1]:
            inputs[-1]['SERV_param'] = SERV_param_decoder[inputs[-1]['SERV_param']]

    outputs = [simulate(inp) for inp in inputs]
    table = [
        take_cols({**out, **inp}, out_cols)
        for inp, out in zip(src_inputs, outputs)
    ]
    with open(f"json/exp{EXP_NUM}.json", "w") as f:
        json.dump(table, f)
    text = tabulate(table, headers="keys", tablefmt="tsv", floatfmt=".3f")
    return text


inter_postup = 11.9955

"""
1.1.
in:    t.обслуж(t_b) as коэф.загруз (0.1-0.9)
const: l.поступления
out:   t.пер.режим   by c.заявок
"""


def exp1():
    inputs = [
        dict(
            TA_param=11.9955,
            TB_param=tb,
            iter_n=cnt,
            EB_param=1,
            PR_COUNT_param=1,
            GEN_param='E',
            SERV_param='E'
        )
        for tb in range(1, 25, 3)
        for cnt in [100, 500, 1000, 5000, 10000, 50000, 100000]
    ]
    return run(inputs, ["iter_n", "util", "TB_param", "avg_wait", "avg_resid"])


"""
1.2.
in:    T.поступления(t_a) as коэф.загруз (0.1-0.9)
const: t.обслуж
out:   t.пер.режим
"""


def exp2():
    inputs = [
        dict(
            TA_param=ta,
            TB_param=10,
            iter_n=cnt,
            EB_param=1,
            PR_COUNT_param=1,
            GEN_param='E',
            SERV_param='E'
        )
        for ta in range(1, 35, 5)
        for cnt in [100, 1000, 10000, 50000, 100000]
    ]
    return run(inputs, ["iter_n", "util", "TA_param", "avg_wait", "avg_resid"])


"""
2.
in:    закон(трасса,аппрокс,простейш,равном)
in:    t.обслуж as коэф.загруз (0.5,0.75,0.95,0.99)
out:   t.ожид t.преб p.потер
"""


def exp3():
    inputs = [
        dict(
            TA_param=inter_postup,  # TODO
            TB_param=tb,
            iter_n=100_000,
            EB_param=1,
            PR_COUNT_param=1,
            GEN_param=gtype,
            SERV_param='E'
        )
        for gtype, tlist in [('E', [7, 16, 47, 117]), ('T', [7, 16, 47, 117]), ('A', [7, 16, 47, 117])]
        for tb in tlist
    ]
    inputs.sort(key=lambda x: x['TB_param'])
    return run(inputs, ["GEN_param", "TB_param", "util", "avg_resid", "std_resid", "avg_wait", "std_wait", "dov_wait", "dovpct_wait",
                        "prb_refuse"])


"""
5.
in:     поток(простейш,трасса,аппрокс)
out:    c.заявок
target: устойчивый результат
"""


def exp4():
    inputs = [
        dict(
            iter_n=cnt,
            TA_param=0,
            TB_param=1,
            EB_param=0,
            PR_COUNT_param=2,
            GEN_param=gtype,
            SERV_param='E'
        )
        for gtype in ['E', 'T', 'R']
        for cnt in [10, 100, 1000, 10000, 100000]
    ]
    return run(inputs)


if __name__ == "__main__":
    # time.sleep(2)
    # for i in range(1, 5):
    #     exec(f"exp{i}()")
    f = open(f'res{EXP_NUM}.md', 'w')
    exec(f"f.write(exp{EXP_NUM}())")
    f.close()
    print()
