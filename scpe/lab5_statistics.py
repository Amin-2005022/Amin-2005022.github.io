"""
Lab 05 - Interpreting Measured Data
Course: 0613-310 System Configuration and Performance Evaluation Lab

Runs the Sieve of Eratosthenes benchmark 30 times and summarizes the results:
  - central tendency : mean, median
  - variability      : range, variance, standard deviation, CV, quartiles, IQR
  - errors           : outliers (1.5 x IQR rule) and the warm-up (first) run
  - confidence       : 95% confidence interval of the mean (t-distribution)
  - planning         : how many runs are needed for +/-1% and +/-5% precision
The 30 times are saved to a CSV file and drawn as a histogram, box plot and
run-by-run chart.

Before the first run:   pip install numpy scipy matplotlib
"""
import csv
import math
import time
import platform
import statistics

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

N = 5_000_000          # find all primes up to N
RUNS = 30              # number of measurements
CONFIDENCE = 0.95      # 95% confidence interval
CONDITION = "normal"   # change to "loaded" when you run under heavy load


# ---------------------------------------------------------------- benchmark
def sieve(n):
    """Return the number of primes from 2 to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for m in range(i * i, n + 1, i):
                is_prime[m] = False
    return sum(is_prime)


def measure_runs(runs):
    """Run the sieve `runs` times and return the wall times in seconds."""
    times = []
    for run in range(1, runs + 1):
        start = time.perf_counter()
        count = sieve(N)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"Run {run:>2}: {elapsed:.4f} s   ({count:,} primes)")
    return times


# ---------------------------------------------------------------- statistics
def confidence_interval(data, confidence=CONFIDENCE):
    """Return (mean, half_width, low, high) using the t-distribution."""
    n = len(data)
    mean = statistics.mean(data)
    sd = statistics.stdev(data)
    t_value = stats.t.ppf((1 + confidence) / 2, df=n - 1)
    half_width = t_value * sd / math.sqrt(n)
    return mean, half_width, mean - half_width, mean + half_width


def runs_needed(data, precision_percent, z=1.96):
    """Runs needed so the 95% CI is within +/- precision_percent of the mean."""
    mean = statistics.mean(data)
    sd = statistics.stdev(data)
    return math.ceil((100 * z * sd / (precision_percent * mean)) ** 2)


def summarize(times):
    data = np.array(times)
    n = len(data)
    mean = data.mean()
    median = np.median(data)
    variance = data.var(ddof=1)          # sample variance (divide by n - 1)
    sd = data.std(ddof=1)                # sample standard deviation
    cv = sd / mean * 100
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    low_fence, high_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = [(i + 1, t) for i, t in enumerate(times) if t < low_fence or t > high_fence]

    print("\n" + "=" * 60)
    print(f"SUMMARY OF {n} RUNS  (condition: {CONDITION})")
    print("=" * 60)
    print("Central tendency")
    print(f"  Mean                 = {mean:.4f} s")
    print(f"  Median               = {median:.4f} s")
    print("Variability")
    print(f"  Minimum / Maximum    = {data.min():.4f} s / {data.max():.4f} s")
    print(f"  Range                = {data.max() - data.min():.4f} s")
    print(f"  Variance             = {variance:.6f} s^2")
    print(f"  Standard deviation   = {sd:.4f} s")
    print(f"  Coeff. of variation  = {cv:.2f} %")
    print(f"  Q1 / Q3              = {q1:.4f} s / {q3:.4f} s")
    print(f"  IQR                  = {iqr:.4f} s")
    print("Errors")
    print(f"  Outlier fences       = {low_fence:.4f} s to {high_fence:.4f} s")
    if outliers:
        for run, t in outliers:
            print(f"  Outlier              : run {run} = {t:.4f} s")
    else:
        print("  Outliers             : none")
    rest = statistics.mean(times[1:])
    print(f"  First run (warm-up)  = {times[0]:.4f} s   vs mean of runs 2-{n}: {rest:.4f} s")

    print(f"\n{int(CONFIDENCE * 100)}% confidence interval of the mean")
    for label, sample in ((f"First 5 runs", times[:5]),
                          (f"All {n} runs", times),
                          (f"Runs 2-{n} (no warm-up)", times[1:])):
        m, h, lo, hi = confidence_interval(sample)
        print(f"  {label:<24}: {m:.4f} +/- {h:.4f} s  ->  [{lo:.4f}, {hi:.4f}]"
              f"  (+/- {h / m * 100:.1f} %)")

    print("\nRuns needed for a given precision (z = 1.96)")
    for r in (5, 1):
        print(f"  +/- {r}% of the mean   : {runs_needed(times, r)} runs")
    return outliers


# ---------------------------------------------------------------- output
def save_csv(times):
    filename = f"lab5_times_{CONDITION}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["run", "wall_time_s"])
        for run, t in enumerate(times, start=1):
            writer.writerow([run, f"{t:.6f}"])
    print(f"\nSaved the {len(times)} times to {filename}")


def plot(times):
    mean, half, lo, hi = confidence_interval(times)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

    ax1.hist(times, bins=10, color="#0B4F9C", edgecolor="white")
    ax1.axvline(mean, color="#B35400", linewidth=2, label=f"mean {mean:.3f} s")
    ax1.axvline(np.median(times), color="black", linestyle="--", linewidth=2,
                label=f"median {np.median(times):.3f} s")
    ax1.set_title("Histogram")
    ax1.set_xlabel("Wall time (s)")
    ax1.set_ylabel("Number of runs")
    ax1.legend()

    try:                                   # matplotlib 3.10 and newer
        ax2.boxplot(times, orientation="horizontal", widths=0.5)
    except TypeError:                      # older matplotlib
        ax2.boxplot(times, vert=False, widths=0.5)
    ax2.set_title("Box plot")
    ax2.set_xlabel("Wall time (s)")
    ax2.set_yticks([])

    runs = range(1, len(times) + 1)
    ax3.plot(runs, times, marker="o", color="#0B4F9C")
    ax3.axhspan(lo, hi, color="#B35400", alpha=0.2, label="95% CI of the mean")
    ax3.axhline(mean, color="#B35400", linewidth=2)
    ax3.set_title("Run by run")
    ax3.set_xlabel("Run number")
    ax3.set_ylabel("Wall time (s)")
    ax3.legend()

    fig.suptitle(f"Sieve benchmark, N = {N:,}, {len(times)} runs ({CONDITION})")
    fig.tight_layout()
    filename = f"lab5_plots_{CONDITION}.png"
    fig.savefig(filename, dpi=120)
    print(f"Saved the charts to {filename}")
    plt.show()


def main():
    print("=" * 60)
    print("LAB 05: INTERPRETING MEASURED DATA")
    print("=" * 60)
    print(f"System    : {platform.system()} {platform.release()}")
    print(f"Python    : {platform.python_version()}")
    print(f"Benchmark : Sieve of Eratosthenes, N = {N:,}, {RUNS} runs\n")

    times = measure_runs(RUNS)
    summarize(times)
    save_csv(times)
    plot(times)


if __name__ == "__main__":
    main()
