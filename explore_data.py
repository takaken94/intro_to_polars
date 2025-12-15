import polars as pl
import sys

def main():
    # --- 設定 ---
    # データファイル
    data_file_path = "data/22_shizuoka_all.csv"

    # --- 処理 ---
    try:
        # データの読み込み
        df = pl.read_csv(data_file_path)
        print(df.shape)
        print(df.describe())
        print(df.head())
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {data_file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: ファイル処理中に予期せぬエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()