def safe_pct(n,d): return 0 if d==0 else 100*n/d
def load_csv(path):
    import pandas as pd
    return pd.read_csv(path)
