
import pandas as pd

DATE_COLS = {
    "orders": ["Order_Date"],
    "products": ["Product_Launch_Date"],
    "campaigns": ["Campaign_Date"],
    "returns": ["Return_Date"],
    "delivery": ["Dispatch_Date","Expected_Delivery_Date","Actual_Delivery_Date"],
}

def clean_data(dfs):
    out = {k: v.copy() for k,v in dfs.items()}
    for name, cols in DATE_COLS.items():
        for col in cols:
            if col in out[name]:
                out[name][col] = pd.to_datetime(out[name][col], errors="coerce")
    # Business-safe handling: optional Coupon/Campaign/Rating remain missing where genuinely absent.
    out["orders"]["Coupon_Code"] = out["orders"]["Coupon_Code"].fillna("NO_COUPON")
    out["orders"]["Campaign_ID"] = out["orders"]["Campaign_ID"].fillna("NO_CAMPAIGN")
    out["orders"]["Customer_Rating"] = out["orders"]["Customer_Rating"].fillna(
        out["orders"]["Customer_Rating"].median()
    )
    out["delivery"]["Actual_Days"] = out["delivery"]["Actual_Days"].fillna(
        out["delivery"]["Expected_Days"]
    )
    return out

def validate_data(dfs):
    checks=[]
    for name, df in dfs.items():
        checks.append({
            "table": name, "rows": len(df), "columns": len(df.columns),
            "duplicate_rows": int(df.duplicated().sum()),
            "missing_cells": int(df.isna().sum().sum())
        })
    return pd.DataFrame(checks)
