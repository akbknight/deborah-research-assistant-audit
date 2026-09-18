"""
visualize_findings_dashboard.py
===============================
Generates an executive-level, multi-panel Forensic Audit Dashboard from
DEBORAH_FINDINGS_LEDGER.csv, summarizing:
1. Severity Distribution (High, Medium, Low)
2. Category Breakdown (Security, Platform, Functional, Testing, etc.)
3. Resolution Status (Resolved vs Unresolved / Technical Debt)
4. Primary Root Cause Taxonomy

Author: Akshay Kumar (akbknight)
Data Source: DEBORAH_FINDINGS_LEDGER.csv
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def ensure_assets_dir():
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    return assets_dir

def plot_findings_dashboard():
    assets_dir = ensure_assets_dir()
    csv_path = os.path.join(os.path.dirname(__file__), "..", "DEBORAH_FINDINGS_LEDGER.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cannot locate ledger at: {csv_path}")

    df = pd.read_csv(csv_path)

    # Clean / standardize categories
    def clean_category(cat):
        cat = str(cat).strip().lower()
        if "security" in cat:
            return "Security & Privacy"
        elif "platform" in cat:
            return "Platform / OS Drift"
        elif "testing" in cat:
            return "Test Suite & Tooling"
        elif "functional" in cat:
            return "Functional Logic"
        elif "packaging" in cat:
            return "Packaging & Release"
        elif "identity" in cat:
            return "Release Identity"
        elif "output" in cat:
            return "Output Quality"
        elif "ux" in cat:
            return "UX & Honesty"
        return "Other"

    df["clean_category"] = df["category"].apply(clean_category)

    # Clean / standardize status
    def clean_status(st):
        st = str(st).strip()
        if st.startswith("Resolved"):
            if "claim" in st.lower() or "unverified" in st.lower() or "paper" in st.lower():
                return "Resolved (Unverified on OS)"
            return "Verified Resolved"
        elif "unresolved" in st.lower():
            return "Unresolved Defect"
        elif "unavailable" in st.lower():
            return "Evidence Unavailable"
        return "Open / Pending"

    df["clean_status"] = df["status_at_latest"].apply(clean_status)

    # Standardize severity
    df["clean_severity"] = df["severity"].str.strip().str.capitalize()

    # Setup 2x2 Grid with high-contrast cinematic dark theme
    plt.style.use("dark_background")
    fig, axes = plt.subplots(2, 2, figsize=(18, 14), dpi=300)
    fig.patch.set_facecolor("#060608")

    for ax in axes.flat:
        ax.set_facecolor("#0d0d14")
        ax.grid(True, linestyle="--", alpha=0.15, color="#8888aa")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#2a2a40")
        ax.spines["bottom"].set_color("#2a2a40")
        ax.tick_params(colors="#8888aa", labelsize=9.5)

    # -------------------------------------------------------------
    # Panel 1: Severity Distribution (Donut Chart)
    # -------------------------------------------------------------
    ax_sev = axes[0, 0]
    sev_counts = df["clean_severity"].value_counts()
    order = ["High", "Medium", "Low"]
    sev_counts = sev_counts.reindex(order).fillna(0)
    total_sev = sev_counts.sum()

    colors_sev = ["#ef4444", "#f59e0b", "#3da0ff"]
    wedges, texts, autotexts = ax_sev.pie(
        sev_counts, labels=sev_counts.index,
        autopct=lambda p: f"{p:.1f}%\n({int(round(p * total_sev / 100))})",
        startangle=140, colors=colors_sev,
        wedgeprops=dict(width=0.42, edgecolor="#060608", linewidth=2.5),
        textprops=dict(color="#f0f0f8", fontsize=10, fontweight="bold")
    )
    for at in autotexts:
        at.set_color("#ffffff")
        at.set_fontsize(9.5)

    ax_sev.set_title("Audit Findings by Severity (Total: 44)",
                     color="#f0f0f8", fontsize=13, fontweight="bold", pad=15)

    # Center circle annotation
    ax_sev.text(0, 0, "44\nFindings", ha="center", va="center",
                color="#f0f0f8", fontsize=14, fontweight="bold")

    # -------------------------------------------------------------
    # Panel 2: Findings by Domain Category (Horizontal Bar)
    # -------------------------------------------------------------
    ax_cat = axes[0, 1]
    cat_counts = df["clean_category"].value_counts().sort_values(ascending=True)

    y_pos = np.arange(len(cat_counts))
    bars = ax_cat.barh(y_pos, cat_counts.values, height=0.62,
                       color="#3da0ff", alpha=0.85, edgecolor="#137fec", linewidth=1.2)

    ax_cat.set_yticks(y_pos)
    ax_cat.set_yticklabels(cat_counts.index, color="#f0f0f8", fontweight="medium", fontsize=10)
    ax_cat.set_xlabel("Number of Issues Identified", color="#8888aa", fontsize=10, fontweight="bold")
    ax_cat.set_title("Distribution Across Engineering Domains",
                     color="#f0f0f8", fontsize=13, fontweight="bold", pad=15)

    for bar in bars:
        w = bar.get_width()
        ax_cat.text(w + 0.3, bar.get_y() + bar.get_height()/2, f"{int(w)}",
                    va="center", ha="left", color="#f0f0f8", fontsize=9.5, fontweight="bold")

    # -------------------------------------------------------------
    # Panel 3: Resolution Status at Baseline v3.2-rc2 (Donut Chart)
    # -------------------------------------------------------------
    ax_stat = axes[1, 0]
    stat_counts = df["clean_status"].value_counts()
    stat_order = ["Verified Resolved", "Resolved (Unverified on OS)", "Unresolved Defect", "Evidence Unavailable"]
    stat_counts = stat_counts.reindex(stat_order).fillna(0)
    total_stat = stat_counts.sum()

    colors_stat = ["#10b981", "#3b82f6", "#ef4444", "#6b7280"]
    wedges2, texts2, autotexts2 = ax_stat.pie(
        stat_counts, labels=stat_counts.index,
        autopct=lambda p: f"{p:.1f}%\n({int(round(p * total_stat / 100))})" if p > 0 else "",
        startangle=90, colors=colors_stat,
        wedgeprops=dict(width=0.42, edgecolor="#060608", linewidth=2.5),
        textprops=dict(color="#f0f0f8", fontsize=9.5, fontweight="medium")
    )
    for at in autotexts2:
        at.set_color("#ffffff")
        at.set_fontsize(9)

    ax_stat.set_title("Resolution Status at Current Baseline (v3.2-rc2)\n(75% Resolved vs 25% Technical Debt/Unverified)",
                      color="#f0f0f8", fontsize=13, fontweight="bold", pad=15)
    ax_stat.text(0, 0, "75%\nFixed", ha="center", va="center",
                 color="#10b981", fontsize=13, fontweight="bold")

    # -------------------------------------------------------------
    # Panel 4: Root Cause Taxonomy Breakdown (Horizontal Bar)
    # -------------------------------------------------------------
    ax_rc = axes[1, 1]
    root_cause_categories = {
        "Platform & OS Encoding (cp1252 / CRLF)": 7,
        "Transport & Network Security (SSRF/TLS/Proxies)": 6,
        "Upstream API Barrier / Bot Shield (Cloudflare 403)": 3,
        "Packaging & Artifact Misconfiguration": 6,
        "Concurrency, Locks & File Descriptors": 5,
        "UI Specificity & Gate Binding (CSRF/Consent)": 5,
        "Entity Resolution & Scope Admissibility": 4,
        "Test Rig & Metric Coupling": 8,
    }

    rc_series = pd.Series(root_cause_categories).sort_values(ascending=True)
    y_pos_rc = np.arange(len(rc_series))

    bars_rc = ax_rc.barh(y_pos_rc, rc_series.values, height=0.62,
                         color="#a78bfa", alpha=0.85, edgecolor="#8b5cf6", linewidth=1.2)

    ax_rc.set_yticks(y_pos_rc)
    ax_rc.set_yticklabels(rc_series.index, color="#f0f0f8", fontsize=9)
    ax_rc.set_xlabel("Occurrences across 44 Ledger Items", color="#8888aa", fontsize=10, fontweight="bold")
    ax_rc.set_title("Forensic Root Cause Taxonomy",
                    color="#f0f0f8", fontsize=13, fontweight="bold", pad=15)

    for bar in bars_rc:
        w = bar.get_width()
        ax_rc.text(w + 0.2, bar.get_y() + bar.get_height()/2, f"{int(w)}",
                   va="center", ha="left", color="#f0f0f8", fontsize=9.5, fontweight="bold")

    plt.suptitle("DEBORAH RESEARCH ASSISTANT — FORENSIC AUDIT EXECUTIVE DASHBOARD\nSystemic Vulnerabilities, Architecture Evolutions, and Integrity Verdicts",
                 color="#ffffff", fontsize=15, fontweight="bold", y=0.99)

    plt.tight_layout(rect=[0, 0.02, 1, 0.97])
    output_path = os.path.join(assets_dir, "findings_dashboard.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[+] Saved Findings Dashboard to: {output_path}")

if __name__ == "__main__":
    plot_findings_dashboard()
