import polars as pl

def main():
    # --- 設定 ---
    # 入力ファイル
    in_file_path = "data/22_shizuoka_all.csv"

    # --- 処理 ---
    query = (
        pl.scan_csv(
            source=in_file_path,
            infer_schema_length=0, # 全ての列を str として読み込む pandas の dtype=str に相当
        )
        .filter(pl.col("kind") == "101")  # 法人種別 101: 国の機関
        .group_by("cityName")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )

    df = query.collect()
    pl.Config.set_tbl_rows(100)
    print(df)

    print(query.explain())

if __name__ == "__main__":
    main()