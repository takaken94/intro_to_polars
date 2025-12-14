import polars as pl
import sys

def load_csv_to_dataframe(file_path: str, encoding: str = "utf-8", has_header: bool = True, separator: str = ",") -> pl.DataFrame:
    """
    指定されたパスからCSVファイルを読み込み、Polarsデータフレームを返す。
    エラーが発生した場合は例外を送出する。
    """
    return pl.read_csv(
        file_path,
        encoding=encoding,
        has_header=has_header,
        separator=separator,
    )

def main():
    """データファイルを読み込み、基本的な探索的データ分析を行う。"""
    # --- 設定 ---
    # データファイル
    data_file_path = "data/22_shizuoka_all.csv"

    # --- 処理 ---
    try:
        # データの読み込み
        df = load_csv_to_dataframe(data_file_path)
        print(df.shape)
        print(df.describe())
        print(df.head())
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {data_file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: ファイル処理中に予期せぬ問題が発生しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()