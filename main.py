import re
import math
import scipy.stats as sps
from experiment_runner import run_experiment

def extract_f(text, rx):
    data = re.findall(rx, text, re.MULTILINE)[0]
    data = data.strip().split()
    data = list(map(float, data))
    return data


def dov(cnt, std, a=0.99):
    za = float(sps.norm.ppf(1 - a / 2))
    return za * std / math.sqrt(cnt)


def parse(text):
    _, _, _, _, avg_length, _, avg_wait_nonzero, _ = extract_f(text, "^ BUF1(.*)\n")
    avg_resid, std_resid, _ = extract_f(text, "^ TU_UZEL(.*)\n")
    avg_wait, std_wait, _ = extract_f(text, "^ TU_BUF(.*)\n")
    cnt_all, _, _ = extract_f(text, "GENERATE(.*)")
    cnt_refuse, _, _ = extract_f(text, "ZYX.*TERMINATE(.*)\n")
    cnt_passed = cnt_all - cnt_refuse
    prb_refuse = cnt_refuse / cnt_all
    dov_wait = dov(cnt_passed, std_wait)
    dovpct_wait = dov_wait / avg_wait

    return dict(
        avg_resid=avg_resid, std_resid=std_resid,
        avg_wait=avg_wait, std_wait=std_wait, dov_wait=dov_wait, dovpct_wait=dovpct_wait,
        cnt_all=cnt_all, cnt_passed=cnt_passed,
        cnt_refuse=cnt_refuse, prb_refuse=prb_refuse,
        avg_length=avg_length, avg_wait_nonzero=avg_wait_nonzero
    )

def get_results(params: dict, n_iter: int) -> dict:
    return parse(run_experiment(params, n_iter))

if __name__ == '__main__':
    get_results(
        {
            'EB_param': None,
            'TA_param': 
        },
        1000
    )