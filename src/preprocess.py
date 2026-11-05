from pathlib import Path
import numpy as np
import pandas as pd


def load_raw(raw_dir="data/raw"):
    """Load all CIC-IDS2017 CSVs into one DataFrame with compact dtypes."""
    files = sorted(Path(raw_dir).glob("*.csv"))
    dfs = []
    for f in files:
        df = pd.read_csv(f, encoding="latin1", low_memory=False)
        df.columns = df.columns.str.strip()
        for c in df.select_dtypes("float64").columns:
            df[c] = df[c].astype("float32")
        for c in df.select_dtypes("int64").columns:
            df[c] = df[c].astype("int32")
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def clean_labels(s):
    """Fix garbled characters, e.g. 'Web Attack ï¿½ XSS' -> 'Web Attack - XSS'."""
    return s.str.replace(r"[^\x20-\x7E]+", "-", regex=True).str.strip()


def clean(df):
    """Cleaning that learns nothing from the data, so it is safe before the split."""
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    df["Label"] = clean_labels(df["Label"])
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    df = df.drop_duplicates()
    return df.reset_index(drop=True)