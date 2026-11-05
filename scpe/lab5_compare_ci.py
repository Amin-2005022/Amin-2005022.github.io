"""
Lab 05 - Extension: compare two conditions with confidence intervals
Course: 0613-310 System Configuration and Performance Evaluation Lab

First run lab5_statistics.py twice:
  1. with CONDITION = "normal" on an idle system  -> lab5_times_normal.csv
  2. with CONDITION = "loaded" under heavy load    -> lab5_times_loaded.csv
Then run this file. It prints both 95% confidence intervals and says whether
they overlap. (Next week, Lab 06, the t-test answers this more precisely.)
"""
import csv
import math
import statistics

from scipy import stats
import matplotlib.pyplot as plt

CONFIDENCE = 0.95


def read_times(filename):
    with open(filename, newline="") as f:
        return [float(row["wall_time_s"]) for row in csv.DictReader(f)]


def confidence_interval(data, confidence=CONFIDENCE):
    n = len(data)
    mean = statistics.mean(data)
    sd = statistics.stdev(data)
    t_value = stats.t.ppf((1 + confidence) / 2, df=n - 1)
    half_width = t_value * sd / math.sqrt(n)
    return mean, half_width, mean - half_width, mean + half_width


def main():
    results = {}
    for condition in ("normal", "loaded"):
        times = read_times(f"lab5_times_{condition}.csv")
        results[condition] = confidence_interval(times)
        m, h, lo, hi = results[condition]
        print(f"{condition.capitalize():<7}: mean {m:.4f} s, "
              f"95% CI [{lo:.4f}, {hi:.4f}]  ({len(times)} runs)")

    _, _, n_lo, n_hi = results["normal"]
    _, _, l_lo, l_hi = results["loaded"]
    if n_hi < l_lo or l_hi < n_lo:
        print("\nThe intervals do NOT overlap: the difference is statistically significant.")
    else:
        print("\nThe intervals overlap: we cannot be sure from the intervals alone.")
        print("Use a t-test (Lab 06) to decide.")

    fig, ax = plt.subplots(figsize=(8, 4))
    for y, condition in enumerate(("normal", "loaded")):
        m, h, lo, hi = results[condition]
        ax.errorbar(m, y, xerr=h, fmt="o", capsize=8, markersize=8,
                    color="#0B4F9C" if condition == "normal" else "#B35400")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Normal", "Loaded"])
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("Mean wall time (s) with 95% confidence interval")
    ax.set_title("Comparing two conditions")
    fig.tight_layout()
    fig.savefig("lab5_compare_ci.png", dpi=120)
    print("Saved the chart to lab5_compare_ci.png")
    plt.show()


if __name__ == "__main__":
    main()
