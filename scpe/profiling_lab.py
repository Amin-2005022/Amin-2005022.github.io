"""
Lab 04 - Function-Level Performance Analysis Using cProfile and pstats
Course: 0613-310 System Configuration and Performance Evaluation Lab

The program has functions for summation, multiplication, recursion,
function-to-function calling and the Fibonacci series. cProfile measures
every function call, pstats collects the results, and print_report()
prints them with the columns total_time and cumulative_time.
"""
import cProfile
import pstats


# 1. Summation: add the numbers from 1 to n
def calculate_sum(n):
    total = 0
    for number in range(1, n + 1):
        total = total + number
    return total


# 2. Repeated multiplication: multiply the numbers from 1 to n
def calculate_multiplication(n):
    result = 1
    for number in range(1, n + 1):
        result = result * number
    return result


# 3. Recursive function: factorial of n
def recursive_factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * recursive_factorial(n - 1)


# 4. Function-to-function calling: calls two functions, then a short task
def generate_report():
    sum_result = calculate_sum(1_000_000)
    product = calculate_multiplication(10_000)
    size_bits = product.bit_length()      # short extra task: size of the product
    return sum_result, size_bits


# 5. Fibonacci: recursive, plus a function that builds the series
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_series(count):
    return [fibonacci(i) for i in range(count)]


# 6. main(): calls all the functions and shows the results
def main():
    sum_result, size_bits = generate_report()
    factorial_result = recursive_factorial(500)
    series = fibonacci_series(25)

    print("Sum from 1 to 1,000,000          :", sum_result)
    print("Size of 1 x 2 x ... x 10000 (bits):", size_bits)
    print("Digits in 500! (factorial)       :", len(str(factorial_result)))
    print("First 25 Fibonacci numbers       :", series)


OUR_FUNCTIONS = ("main", "generate_report", "calculate_sum", "calculate_multiplication",
                 "recursive_factorial", "fibonacci_series", "fibonacci")


# 7. Report: our own table with clear column names
#    total_time      = time in the function's own code only
#    cumulative_time = time including every function it calls
def print_report(stats):
    print("\nPROFILING REPORT (only our functions)")
    print(f"{stats.total_calls} function calls ({stats.prim_calls} primitive calls)"
          f" in {stats.total_tt:.3f} seconds")
    print("Ordered by: cumulative_time\n")
    print(f"{'ncalls':>10} {'total_time':>11} {'percall':>8} "
          f"{'cumulative_time':>16} {'percall':>8}  function")

    rows = []
    for (filename, line, name), data in stats.stats.items():
        primitive_calls, total_calls, total_time, cumulative_time, callers = data
        if name in OUR_FUNCTIONS:
            rows.append((name, primitive_calls, total_calls, total_time, cumulative_time))
    rows.sort(key=lambda row: row[4], reverse=True)    # biggest cumulative_time first

    for name, primitive_calls, total_calls, total_time, cumulative_time in rows:
        if total_calls == primitive_calls:
            ncalls = str(total_calls)
        else:
            ncalls = f"{total_calls}/{primitive_calls}"    # total/primitive
        print(f"{ncalls:>10} {total_time:>11.3f} {total_time / total_calls:>8.3f} "
              f"{cumulative_time:>16.3f} {cumulative_time / primitive_calls:>8.3f}  {name}")


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()          # start measuring
    main()
    profiler.disable()         # stop measuring

    stats = pstats.Stats(profiler)
    print_report(stats)