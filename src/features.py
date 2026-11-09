import numpy as np
import pandas as pd

# 15 original labels -> 8 groups
LABEL_GROUPS = {
    "BENIGN": "Benign",
    "DoS Hulk": "DoS",
    "DoS GoldenEye": "DoS",
    "DoS slowloris": "DoS",
    "DoS Slowhttptest": "DoS",
    "DDoS": "DDoS",
    "PortScan": "Port Scan",
    "FTP-Patator": "Brute Force",
    "SSH-Patator": "Brute Force",
    "Web Attack - Brute Force": "Web Attack",
    "Web Attack - XSS": "Web Attack",
    "Web Attack - Sql Injection": "Web Attack",
    "Bot": "Bot",
    "Infiltration": "Other",
    "Heartbleed": "Other",
}


def group_labels(df):
    """Keep the original label as Label_fine, and group it into Label."""
    df = df.copy()
    df["Label_fine"] = df["Label"]
    df["Label"] = df["Label"].map(LABEL_GROUPS)
    assert df["Label"].notna().all(), "unmapped label found"
    return df


def add_features(df):
    """Row-wise features. They learn nothing from the data, so they are safe before the split."""
    df = df.copy()
    fwd_p, bwd_p = df["Total Fwd Packets"], df["Total Backward Packets"]
    fwd_b, bwd_b = df["Total Length of Fwd Packets"], df["Total Length of Bwd Packets"]

    df["total_packets"] = fwd_p + bwd_p
    df["total_bytes"] = fwd_b + bwd_b
    df["fwd_bwd_packet_ratio"] = fwd_p / (bwd_p + 1)
    df["fwd_bwd_bytes_ratio"] = fwd_b / (bwd_b + 1)
    df["bytes_per_packet"] = df["total_bytes"] / (df["total_packets"] + 1)
    return df