"""
visualize_test_evidence.py
==========================
Generates high-resolution visualizations for the Deborah Research Assistant
forensic audit repository:
1. Test Suite Exponential Growth (Static definitions vs Executed tests)
2. Cross-Platform Stability Gap (Linux vs Windows Pass/Fail/Error trajectories)

Author: Akshay Kumar (akbknight)
Data Source: DEBORAH_TEST_EVIDENCE.csv & DEBORAH_COMPLETE_VERSION_HISTORY.md
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def ensure_assets_dir():
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    return assets_dir

def plot_test_evidence():
    assets_dir = ensure_assets_dir()

    # High-end Dark Theme Styling matching akbknight.github.io / NotebookLM
    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7), dpi=300)
    fig.patch.set_facecolor("#060608")
    for ax in (ax1, ax2):
        ax.set_facecolor("#0d0d14")
        ax.grid(True, linestyle="--", alpha=0.15, color="#8888aa")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#2a2a40")
        ax.spines["bottom"].set_color("#2a2a40")
        ax.tick_params(colors="#8888aa", labelsize=9)

    # -------------------------------------------------------------
    # 1. Test Growth Trajectory (Static vs Executed across Lineage)
    # -------------------------------------------------------------
    milestones = [
        "v1.0", "v1.1", "v1.2", "v2.0-rc1", "v2.0-rc2", "v2.0-rc3",
        "v2.1-rc1", "v2.2-rc1", "v3.0-rc1", "v3.0-rc2", "v3.1-rc1",
        "v3.2-rc1", "v3.2-rc2"
    ]
    static_tests = [67, 106, 158, 1771, 1771, 1775, 1850, 2020, 3191, 3210, 3270, 3350, 3373]
    executed_tests_linux = [0, 0, 211, 2417, 2427, 2502, 2571, 2687, 4191, 4308, 4371, 4413, 4426]

    x = np.arange(len(milestones))
    width = 0.35

    bar1 = ax1.bar(x - width/2, static_tests, width, label="Static Test Definitions",
                   color="#3da0ff", alpha=0.85, edgecolor="#137fec", linewidth=1.2)
    bar2 = ax1.bar(x + width/2, executed_tests_linux, width, label="Executed Tests (Linux Suite)",
                   color="#34d399", alpha=0.85, edgecolor="#10b981", linewidth=1.2)

    ax1.set_xticks(x)
    ax1.set_xticklabels(milestones, rotation=45, ha="right", fontweight="medium")
    ax1.set_ylabel("Number of Tests", color="#f0f0f8", fontsize=11, fontweight="bold")
    ax1.set_title("Test Suite Expansion: 67 to 4,426 Tests\n(Static Coverage vs Executed Suite)",
                  color="#f0f0f8", fontsize=13, fontweight="bold", pad=15)
    ax1.legend(facecolor="#13131f", edgecolor="#2a2a40", labelcolor="#f0f0f8", fontsize=10, loc="upper left")

    # Annotations for major inflection points
    ax1.annotate("v2.0 Architectural Pivot\n(+1,613 static tests)",
                 xy=(3, 1771), xytext=(2.2, 2800),
                 arrowprops=dict(arrowstyle="->", color="#3da0ff", lw=1.2),
                 color="#3da0ff", fontsize=9, fontweight="bold")

    ax1.annotate("v3.2-rc2 Packaged Baseline\n4,426 Passed (388.97s)",
                 xy=(12, 4426), xytext=(9.2, 4700),
                 arrowprops=dict(arrowstyle="->", color="#34d399", lw=1.2),
                 color="#34d399", fontsize=9, fontweight="bold")

    # -------------------------------------------------------------
    # 2. Cross-Platform Stability Gap (Linux vs Windows)
    # -------------------------------------------------------------
    platforms_runs = [
        "v2.0-rc1\n(Win 11)", "v2.0-rc1\n(Linux)",
        "v2.0-rc2\n(Win 11)*", "v2.0-rc2\n(Linux)",
        "v2.0-rc3\n(Win 11)", "v2.0-rc3\n(Linux)",
        "v2.1-rc1\n(Win 11)", "v2.1-rc1\n(Linux)",
        "v3.0-rc1\n(Win 11)", "v3.0-rc1\n(Linux)",
        "v3.2-rc2\n(Linux)", "v3.2-rc2\n(Win)*"
    ]

    passed =   [2415, 2417, 2427, 2427, 2443, 2502, 2570, 2571, 4178, 4191, 4426, 0]
    failures = [   1,    0,    0,    0,    1,    0,    1,    0,    5,    0,    0, 0]
    errors =   [   2,    0,    0,    0,    9,    0,    0,    0,    7,    0,    0, 0]
    unverified=[   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, 4426]

    x2 = np.arange(len(platforms_runs))

    p1 = ax2.bar(x2, passed, width=0.6, label="Passed Tests", color="#10b981", alpha=0.85)
    p2 = ax2.bar(x2, failures, width=0.6, bottom=passed, label="Failures", color="#ef4444", alpha=0.9)
    p3 = ax2.bar(x2, errors, width=0.6, bottom=np.array(passed)+np.array(failures), label="Errors (Crash/Env)", color="#f59e0b", alpha=0.9)
    p4 = ax2.bar(x2, unverified, width=0.6, bottom=np.array(passed)+np.array(failures)+np.array(errors),
                 label="Unverified / Never Run", color="#6b7280", alpha=0.4, hatch="//")

    ax2.set_xticks(x2)
    ax2.set_xticklabels(platforms_runs, rotation=45, ha="right", fontsize=8.5)
    ax2.set_ylabel("Test Outcomes", color="#f0f0f8", fontsize=11, fontweight="bold")
    ax2.set_title("Cross-Platform Stability Gap\n(Linux Production vs Windows Acceptance Drift)",
                  color="#f0f0f8", fontsize=13, fontweight="bold", pad=15)
    ax2.legend(facecolor="#13131f", edgecolor="#2a2a40", labelcolor="#f0f0f8", fontsize=10, loc="upper left")

    # Footnote about false positive and missing Windows tests
    ax2.text(0.02, -0.22,
             "* v2.0-rc2 Win was a verified false-positive (launcher ran legacy v1.2 UI). Post-v3.0-rc1 builds lack Windows execution evidence.",
             transform=ax2.transAxes, color="#8888aa", fontsize=8, style="italic")

    plt.tight_layout()
    output_path = os.path.join(assets_dir, "test_evidence_trend.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[+] Saved Test Evidence Trend to: {output_path}")

if __name__ == "__main__":
    plot_test_evidence()
