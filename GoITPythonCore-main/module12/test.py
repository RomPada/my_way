from time import process_time_ns

get_pow_lambda = lambda x: x*x

def get_pow(x: int) -> int:
    return x*x

for _ in range(20):
    start = process_time_ns()
    for _ in range(100):
        get_pow_lambda(3)
    print(f"{"get_pow_lambda, (ns):":<25} {process_time_ns() - start}")

    start = process_time_ns()
    for _ in range(100):
        get_pow(3)
    print(f"{"get_pow, (ns):":<25} {process_time_ns() - start}")
