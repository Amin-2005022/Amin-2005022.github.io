"""
Lab 04 - Optional demo (slide 20): fixing the hotspot
Profiles the Fibonacci series twice: plain recursion, then with lru_cache.
Course: 0613-310 System Configuration and Performance Evaluation Lab
"""
import cProfile
import pstats
from functools import lru_cache


# Version 1: plain recursion (the hotspot from profiling_lab.py)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_series(count):
    return [fibonacci(i) for i in range(count)]


# Version 2: the same function with a cache that remembers each answer
@lru_cache(maxsize=None)
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def fibonacci_series_cached(count):
    return [fibonacci_cached(i) for i in range(count)]


def print_report(stats, names):
    """Print ncalls, total_time and cumulative_time for the named functions."""
    print(f"{stats.total_calls} function calls in {stats.total_tt:.3f} seconds\n")
    print(f"{'ncalls':>10} {'total_time':>11} {'cumulative_time':>16}  function")
    rows = []
    for (filename, line, name), data in stats.stats.items():
        primitive_calls, total_calls, total_time, cumulative_time, callers = data
        if name in names:
            rows.append((name, primitive_calls, total_calls, total_time, cumulative_time))
    rows.sort(key=lambda row: row[4], reverse=True)
    for name, primitive_calls, total_calls, total_time, cumulative_time in rows:
        if total_calls == primitive_calls:
            ncalls = str(total_calls)
        else:
            ncalls = f"{total_calls}/{primitive_calls}"
        print(f"{ncalls:>10} {total_time:>11.3f} {cumulative_time:>16.3f}  {name}")


def profile(title, func, count, names):
    profiler = cProfile.Profile()
    profiler.enable()
    series = func(count)
    profiler.disable()

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print("Last number in the series:", series[-1])
    print_report(pstats.Stats(profiler), names)


if __name__ == "__main__":
    profile("BEFORE: plain recursion", fibonacci_series, 25,
            ("fibonacci_series", "fibonacci"))
    profile("AFTER: with lru_cache", fibonacci_series_cached, 25,
            ("fibonacci_series_cached", "fibonacci_cached"))