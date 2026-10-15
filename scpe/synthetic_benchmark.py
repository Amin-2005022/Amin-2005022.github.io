"""
Lab 03 - System Performance Evaluation Using Synthetic Benchmarking
Benchmark 1: Ackermann function       (recursive benchmark)
Benchmark 2: Matrix multiplication    (numerical benchmark)
Course: 0613-310 System Configuration and Performance Evaluation Lab

Runs each benchmark several times, measures CPU Time and Wall (Execution)
Time, and prints the average, standard deviation and coefficient of variation.
Run it once with the system idle (Normal) and once under heavy load (Loaded).
"""
import sys
import time
import random
import platform
import threading
import statistics

ACK_M, ACK_N = 3, 9    # Ackermann(3, 9) = 4093, about 11 million calls
MATRIX_N = 250         # multiply two 250 x 250 matrices
RUNS = 5               # repeat each benchmark 5 times

# Ackermann(3, 9) recurses about 4,000 levels deep.
# Python's default limit is 1,000, so raise it.
sys.setrecursionlimit(10_000)


def ackermann(m, n):
    """Recursive Ackermann function."""
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))


def make_matrix(n):
    """Create an n x n matrix of random numbers between 0 and 1."""
    return [[random.random() for _ in range(n)] for _ in range(n)]


def matrix_multiply(a, b):
    """Multiply two n x n matrices with the classic triple loop."""
    n = len(a)
    c = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0.0
            for k in range(n):
                total += a[i][k] * b[k][j]
            c[i][j] = total
    return c


def measure(func, *args):
    """Run func(*args) once and return (result, cpu_time, wall_time)."""
    wall_start = time.perf_counter()     # real clock time
    cpu_start = time.process_time()      # CPU time used by this process
    result = func(*args)
    cpu_time = time.process_time() - cpu_start
    wall_time = time.perf_counter() - wall_start
    return result, cpu_time, wall_time


def summarize(name, values):
    avg = statistics.mean(values)
    sd = statistics.stdev(values)
    cv = sd / avg * 100
    print(f"{name:<10} Average = {avg:.4f} s   SD = {sd:.4f} s   CV = {cv:.2f} %")
    return avg


def run_benchmark(title, func, *args):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(f"{'Run':<6}{'CPU Time (s)':>18}{'Wall Time (s)':>18}")
    print("-" * 60)

    cpu_times, wall_times = [], []
    result = None
    for run in range(1, RUNS + 1):
        result, cpu_t, wall_t = measure(func, *args)
        cpu_times.append(cpu_t)
        wall_times.append(wall_t)
        print(f"{run:<6}{cpu_t:>18.4f}{wall_t:>18.4f}")

    print("-" * 60)
    cpu_avg = summarize("CPU Time", cpu_times)
    wall_avg = summarize("Wall Time", wall_times)
    print(f"Average waiting time (Wall - CPU) = {wall_avg - cpu_avg:.4f} s")
    return result


def main():
    print("=" * 60)
    print("SYNTHETIC BENCHMARKS: ACKERMANN AND MATRIX MULTIPLICATION")
    print("=" * 60)
    print(f"System    : {platform.system()} {platform.release()}")
    print(f"Processor : {platform.processor() or platform.machine()}")
    print(f"Python    : {platform.python_version()}")
    print(f"Runs      : {RUNS}")

    result = run_benchmark(f"TASK 1: ACKERMANN({ACK_M}, {ACK_N})  (recursive)",
                           ackermann, ACK_M, ACK_N)
    print(f"Check: Ackermann({ACK_M}, {ACK_N}) = {result}")

    random.seed(42)                       # same matrices every time
    a = make_matrix(MATRIX_N)
    b = make_matrix(MATRIX_N)
    run_benchmark(f"TASK 2: MATRIX MULTIPLICATION {MATRIX_N} x {MATRIX_N}  (numerical)",
                  matrix_multiply, a, b)
    print("=" * 60)


if __name__ == "__main__":
    # Deep recursion needs a bigger stack than some systems (e.g. Windows)
    # give by default, so run the benchmarks in a thread with a 64 MB stack.
    threading.stack_size(64 * 1024 * 1024)
    worker = threading.Thread(target=main)
    worker.start()
    worker.join()
