import pandas as pd

def fix_nan_in_frame(frame):
    return frame.applymap(lambda val: None if pd.isna(val) else val)