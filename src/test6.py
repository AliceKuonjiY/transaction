
import frelatage
import random

def test(a: int, b: int):
    return a + b;

input1 = frelatage.Input(value=1)
input2 = frelatage.Input(value=2)


fuzz = frelatage.Fuzzer(
    method=test,
    corpus=[[input1], [input2]],
    threads_count=4,
    output_directory="./fuzz_output",
    silent=False,
    infinite_fuzz=False,
)
fuzz.fuzz()
