import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# CONFIG

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "../data"
TARGET_DIR = BASE_DIR / "../target"

timestamp = datetime.now().strftime("%Y-%m-%d%H%M%S")

INPUT_FILE = DATA_DIR / "dirty_cafe_sales.csv"
REJECT_PATH = TARGET_DIR / f"reject/data_rejected_{timestamp}.csv"
ACCEPTED_PATH = TARGET_DIR / "accepted"

(REJECT_PATH.parent).mkdir(parents=True, exist_ok=True)
(ACCEPTED_PATH).mkdir(parents=True, exist_ok=True)


# UTILITY FUNCTION


def clean_column_name(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def replace_unknowns(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["item", "payment_method", "location"]:
        df[col] = df[col].replace(["ERROR", "UNKNOWN", np.nan], "Unknown")
    return df


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = ["quantity", "price_per_unit", "total_spent"]
    df[num_cols] = df[num_cols].replace(["ERROR", "UNKNOWN"], np.nan).astype(float)
    return df


def recalculate_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[
        df["quantity"].isna()
        & df["price_per_unit"].notna()
        & df["total_spent"].notna(),
        "quantity",
    ] = (
        df["total_spent"] / df["price_per_unit"]
    )
    df.loc[
        df["price_per_unit"].isna()
        & df["quantity"].notna()
        & df["total_spent"].notna(),
        "price_per_unit",
    ] = (
        df["total_spent"] / df["quantity"]
    )
    df.loc[
        df["total_spent"].isna()
        & df["quantity"].notna()
        & df["price_per_unit"].notna(),
        "total_spent",
    ] = (
        df["quantity"] * df["price_per_unit"]
    )
    return df


def create_price_map(df: pd.DataFrame) -> dict:
    prices = df[df["item"].ne("Unknown") & df["price_per_unit"].notna()]
    return prices.groupby("item")["price_per_unit"].first().to_dict()


def sort_unknowns_value(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.sort_values(
        by=[col], key=lambda c: c.str.lower().eq("unknown")
    ).reset_index(drop=True)


def create_dim_table(df: pd.DataFrame, col: str, id_name: str) -> pd.DataFrame:
    dim = df[[col]].drop_duplicates().pipe(sort_unknowns_value, col)
    dim[id_name] = range(1, len(dim) + 1)
    return dim[[id_name, col]]


# MAIN FUNCTION


def main():
    # Extract
    df = pd.read_csv(INPUT_FILE)
    df = clean_column_name(df)
    df.dropna(subset=["transaction_id"], inplace=True)

    # Transform
    df = replace_unknowns(df)
    df = clean_numeric_columns(df)
    df = recalculate_missing_values(df)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    price_map = create_price_map(df)
    df["price_per_unit"] = df["price_per_unit"].fillna(df["item"].map(price_map))
    df = recalculate_missing_values(df)

    reject_mask = (
        df["quantity"].isna()
        | df["price_per_unit"].isna()
        | df["total_spent"].isna()
        | df["transaction_date"].isna()
    )
    data_reject = df[reject_mask]
    data_clean = df.drop(data_reject.index)

    dim_items = (
        data_clean[["item", "price_per_unit"]]
        .drop_duplicates()
        .pipe(sort_unknowns_value, "item")
        .assign(item_id=lambda x: range(1, len(x) + 1))[
            ["item_id", "item", "price_per_unit"]
        ]
    )
    dim_payment_methods = create_dim_table(
        data_clean, "payment_method", "payment_method_id"
    )
    dim_locations = create_dim_table(data_clean, "location", "location_id")

    fact_transactions = (
        data_clean.merge(dim_items, on=["item", "price_per_unit"], how="left")
        .merge(dim_payment_methods, on="payment_method", how="left")
        .merge(dim_locations, on="location", how="left")[
            [
                "transaction_id",
                "transaction_date",
                "item_id",
                "payment_method_id",
                "location_id",
                "quantity",
                "total_spent",
            ]
        ]
    )

    # Load
    data_reject.to_csv(REJECT_PATH, index=False)
    dim_items.to_csv(ACCEPTED_PATH / f"dim_items_{timestamp}.csv", index=False)
    dim_payment_methods.to_csv(
        ACCEPTED_PATH / f"dim_payment_methods_{timestamp}.csv", index=False
    )
    dim_locations.to_csv(ACCEPTED_PATH / f"dim_locations_{timestamp}.csv", index=False)
    fact_transactions.to_csv(
        ACCEPTED_PATH / f"fact_transactions_{timestamp}.csv", index=False
    )

    print("ETL pipeline finished successfully.")
    print(f"- Clean data: {len(data_clean)} rows")
    print(f"- Rejected data: {len(data_reject)} rows")


if __name__ == "__main__":
    main()
