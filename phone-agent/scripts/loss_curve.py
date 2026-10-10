import re
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

LOG = """epoch 1/4 step 100 loss 0.5300
epoch 1/4 step 200 loss 0.7112
epoch 1/4 step 300 loss 1.1736
epoch 1/4 step 400 loss 0.6503
epoch 1/4 step 500 loss 0.5927
epoch 1/4 step 600 loss -0.0200
epoch 1/4 step 700 loss 0.6887
epoch 1/4 step 800 loss 1.0034
epoch 1/4 step 900 loss 0.4855
epoch 1/4 step 1000 loss 0.3840
epoch 1/4 step 1100 loss 0.8197
epoch 1/4 step 1200 loss 1.1653
epoch 1/4 step 1300 loss 0.9518
epoch 1/4 step 1400 loss 1.5111
epoch 1/4 step 1500 loss 0.6812
epoch 1/4 step 1600 loss 0.0887
epoch 1/4 step 1700 loss 0.3093
epoch 1/4 step 1800 loss 0.4461
epoch 1/4 step 1900 loss 0.9898
epoch 1/4 step 2000 loss 0.5411
epoch 1/4 step 2100 loss 0.9499
epoch 1/4 step 2200 loss 0.2549
epoch 2/4 step 100 loss 0.5856
epoch 2/4 step 200 loss 0.8796
epoch 2/4 step 300 loss -0.0763
epoch 2/4 step 400 loss 0.4901
epoch 2/4 step 500 loss 0.2783
epoch 2/4 step 600 loss 0.7298
epoch 2/4 step 700 loss 0.6551
epoch 2/4 step 800 loss 0.1504
epoch 2/4 step 900 loss 0.7933
epoch 2/4 step 1000 loss 0.9261
epoch 2/4 step 1100 loss 0.7241
epoch 2/4 step 1200 loss 0.3124
epoch 2/4 step 1300 loss -0.3180
epoch 2/4 step 1400 loss 0.7565
epoch 2/4 step 1500 loss 0.8007
epoch 2/4 step 1600 loss 0.7657
epoch 2/4 step 1700 loss -0.3647
epoch 2/4 step 1800 loss 0.5083
epoch 2/4 step 1900 loss 0.2630
epoch 2/4 step 2000 loss -0.3859
epoch 2/4 step 2100 loss 0.8473
epoch 2/4 step 2200 loss -0.2211
epoch 3/4 step 100 loss 0.2998
epoch 3/4 step 200 loss 0.2396
epoch 3/4 step 300 loss 0.3418
epoch 3/4 step 400 loss 0.1475
epoch 3/4 step 500 loss 0.8322
epoch 3/4 step 600 loss 0.1561
epoch 3/4 step 700 loss 0.1858
epoch 3/4 step 800 loss -0.3287
epoch 3/4 step 900 loss -0.6176
epoch 3/4 step 1000 loss 0.7094
epoch 3/4 step 1100 loss 0.0208
epoch 3/4 step 1200 loss 0.9520
epoch 3/4 step 1300 loss 0.0192
epoch 3/4 step 1400 loss 0.2999
epoch 3/4 step 1500 loss 0.7066
epoch 3/4 step 1600 loss 0.9363
epoch 3/4 step 1700 loss 0.0497
epoch 3/4 step 1800 loss 0.1467
epoch 3/4 step 1900 loss -0.1602
epoch 3/4 step 2000 loss 0.0450
epoch 3/4 step 2100 loss -0.3786
epoch 3/4 step 2200 loss 0.3355
epoch 4/4 step 100 loss 0.5757
epoch 4/4 step 200 loss -0.1133
epoch 4/4 step 300 loss 0.3535
epoch 4/4 step 400 loss 0.5033
epoch 4/4 step 500 loss 1.0156
epoch 4/4 step 600 loss 0.8267
epoch 4/4 step 700 loss -0.3553
epoch 4/4 step 800 loss 0.6151
epoch 4/4 step 900 loss 0.3101
epoch 4/4 step 1000 loss 0.2606
epoch 4/4 step 1100 loss 0.0196
epoch 4/4 step 1200 loss 0.3287
epoch 4/4 step 1300 loss 0.0769
epoch 4/4 step 1400 loss 0.8070
epoch 4/4 step 1500 loss 1.3289
epoch 4/4 step 1600 loss -0.0321
epoch 4/4 step 1700 loss 0.2014
epoch 4/4 step 1800 loss -0.1342
epoch 4/4 step 1900 loss -0.6893
epoch 4/4 step 2000 loss -0.1153
epoch 4/4 step 2100 loss -0.3106
epoch 4/4 step 2200 loss -0.3949
"""

xs, ys, cols = [], [], []
for m in re.finditer(r"epoch (\d)/4 step (\d+) loss (-?[\d.]+)", LOG):
    e, s, v = int(m.group(1)), int(m.group(2)), float(m.group(3))
    xs.append((e - 1) * 2200 + s)
    ys.append(v)
    cols.append(e)

means = {1: 0.5030, 2: 0.4116, 3: 0.4022, 4: 0.3600}

fig, ax = plt.subplots(figsize=(10, 5))
import collections

by_ep = collections.defaultdict(list)
for x, y, e in zip(xs, ys, cols):
    by_ep[e].append((x, y))
for e in sorted(by_ep):
    ex, ey = zip(*sorted(by_ep[e]))
    ax.plot(ex, ey, marker="o", markersize=3, linewidth=1, label=f"epoch {e}")
for e, m in means.items():
    ax.hlines(m, (e - 1) * 2200, e * 2200, colors="red", linestyles="--", linewidth=1)
    ax.text(
        e * 2200 - 100, m + 0.05, f"ep{e} mean {m}", color="red", fontsize=8, ha="right"
    )
for e in (1, 2, 3):
    ax.axvline(e * 2200, color="gray", linestyle=":", linewidth=1)
ax.set_xlabel("micro-step (global)")
ax.set_ylabel("loss (RLCD)")
ax.set_title("laya-android-control full finetune: loss curve (Kaggle T4)")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("phone-agent/loss_curve.png", dpi=120)

# Smoothed twin: rolling mean (window 5) per epoch.
fig2, ax2 = plt.subplots(figsize=(10, 5))
for e in sorted(by_ep):
    ex, ey = zip(*sorted(by_ep[e]))
    w = 5
    sy = [
        sum(ey[max(0, i - w + 1) : i + 1]) / len(ey[max(0, i - w + 1) : i + 1])
        for i in range(len(ey))
    ]
    ax2.plot(
        ex, sy, marker="o", markersize=3, linewidth=1.5, label=f"epoch {e} (smooth {w})"
    )
for e, m in means.items():
    ax2.hlines(m, (e - 1) * 2200, e * 2200, colors="red", linestyles="--", linewidth=1)
for e in (1, 2, 3):
    ax2.axvline(e * 2200, color="gray", linestyle=":", linewidth=1)
ax2.set_xlabel("micro-step (global)")
ax2.set_ylabel("loss (RLCD, rolling mean)")
ax2.set_title("laya-android-control full finetune: smoothed loss (window 5)")
ax2.grid(alpha=0.3)
ax2.legend(fontsize=8)
fig2.tight_layout()
fig2.savefig("phone-agent/loss_curve_smooth.png", dpi=120)
print("saved")
