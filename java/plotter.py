import glob
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

rows = []
# Adjust path to "../output/log/*.log" if running from inside scripts/
for filepath in glob.glob("./output/log/*.log"):
    filename = os.path.basename(filepath)
    m = re.match(r"linkedlists\.lockbased\.(.+)-i(\d+)-u(\d+)-t(\d+)-w\d+-d\d+\.log", filename)
    if not m:
        continue
    alg, size, u, t = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    with open(filepath) as f:
        content = f.read()

    thr_match = re.search(r"Throughput \(ops/s\):\s+([\d\.]+([eE][+-]?\d+)?)", content)
    if thr_match:
        rows.append({
            "Algorithm": alg,
            "ListSize": size,
            "UpdateRatio": u,
            "Threads": t,
            "Throughput": float(thr_match.group(1))
        })

df = pd.DataFrame(rows).sort_values("Threads")
df.to_csv("results.csv", index=False)

algs = [
    ("CoarseGrainedListBasedSet", "Coarse-Grained", "o"),
    ("HandOverHandListBasedSet", "Hand-Over-Hand", "s"),
    ("LazyLinkedListSortedSet", "Lazy Linked List", "^")
]
threads = [1, 4, 6, 8, 10, 12]

# 1. Comparison Plot (u=10%, i=1000)
plt.figure(figsize=(6.5, 4.2))
for col_name, label, marker in algs:
    sub = df[(df["Algorithm"] == col_name) & (df["UpdateRatio"] == 10) & (df["ListSize"] == 1000)]
    plt.plot(sub["Threads"], sub["Throughput"], marker=marker, linewidth=2, label=label)
plt.title("Algorithm Comparison (List Size = 1000, Update Ratio = 10%)")
plt.xlabel("Number of Threads")
plt.ylabel("Throughput (ops/s) [Log Scale]")
plt.xticks(threads)
plt.yscale("log")
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("plot_comparison_u10_i1000.pdf")
plt.close()

# 2. Varying List Size (100, 1k, 10k) at u=10%
for col_name, label, _ in algs:
    plt.figure(figsize=(6.5, 4.2))
    for size, marker in [(100, "o"), (1000, "s"), (10000, "^")]:
        sub = df[(df["Algorithm"] == col_name) & (df["UpdateRatio"] == 10) & (df["ListSize"] == size)]
        plt.plot(sub["Threads"], sub["Throughput"], marker=marker, linewidth=2, label=f"Size = {size}")
    plt.title(f"{label}: Varying List Size (Update Ratio = 10%)")
    plt.xlabel("Number of Threads")
    plt.ylabel("Throughput (ops/s)")
    plt.xticks(threads)
    plt.yscale("log")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"plot_{col_name}_varying_size.pdf")
    plt.close()

# 3. Varying Update Ratio (0, 10, 100) at i=1000 and i=100
for fixed_size in [1000, 100]:
    for col_name, label, _ in algs:
        plt.figure(figsize=(6.5, 4.2))
        for u, marker in [(0, "o"), (10, "s"), (100, "^")]:
            sub = df[(df["Algorithm"] == col_name) & (df["ListSize"] == fixed_size) & (df["UpdateRatio"] == u)]
            plt.plot(sub["Threads"], sub["Throughput"], marker=marker, linewidth=2, label=f"Update = {u}%")
        plt.title(f"{label}: Varying Update Ratio (List Size = {fixed_size})")
        plt.xlabel("Number of Threads")
        plt.ylabel("Throughput (ops/s)")
        plt.xticks(threads)
        plt.yscale("log")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"plot_{col_name}_varying_u_i{fixed_size}.pdf")
        plt.close()

print("Saved results.csv and generated all PDF plots!")