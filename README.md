# Pandas と Polars の比較・検証

## 概要
Python によるデータ処理・ETL 処理を想定し、**Pandas** と **Polars** のパフォーマンスおよび使い勝手を比較・検証します。

特に以下の観点で、実務利用を意識した検証を行っています。
- CSVファイルの読み込み性能
- データ検索・フィルタリング・集計処理
- Polars の Lazy API による効果

## 利用技術
- Python 3.12
- Pandas
- Polars
- Docker / Dev Containers

## 検証内容
### 1. CSV読み込み速度の比較
| 手法 | 実行時間 | 備考 |
| :--- | :--- | :--- |
| **Pandas (CSVファイル)**     | 0.467秒 | |
| **Polars (CSVファイル)**     | 0.026秒 | Pandas の約18倍高速 |
| **Polars (Parquetファイル)** | 0.073秒 | |

#### 考察
- **Polarsの優位性:** 単純なCSV読み込みにおいて、PolarsはPandasに対して圧倒的なパフォーマンスを発揮しました。
- **並列処理:** Polars の Rustベースの並列処理エンジンが、小中規模以上のデータセットに対して有効であることを確認しました。
- **Parquet:** 今回の検証では、Parquet 読み込みが CSV の約2.8倍の時間となりました。

#### データセット
静岡県の法人データ（12万7千行、30列）のCSVファイルを用いて、読み込み速度の計測を行いました。<br>
2025年12月26日時点のデータを使用しています。<br>
出典：国税庁法人番号公表サイト（国税庁）<a href="https://www.houjin-bangou.nta.go.jp" target="_blank" rel="noopener noreferrer">https://www.houjin-bangou.nta.go.jp</a>

### 2. データ操作（検索・集計）の比較
同一CSVデータに対して、Pandas と Polarsで、以下のデータ操作を実装・比較しました。

- 単一条件によるフィルタリング
- 複数条件（IN 検索）によるフィルタリング
- 日付条件による抽出
- グループ化＋件数集計

| 処理内容 | Pandas | Polars |
|---|---|---|
| CSV読み込み | read_csv | read_csv |
| 単一条件検索 | df[df[col] == value] | df.filter(pl.col == value) |
| IN検索 | isin | is_in |
| 日付条件 | Timestamp比較 | Date型比較 |
| 集計 | groupby + size | group_by + len |

#### 考察
- Polars の書き方は、SQLの処理フロー（WHERE → GROUP BY → ORDER BY）と対応関係が明確で、SQLに慣れている人には処理の流れが理解しやすい。

#### 使用したコード
- Pandas 実装: practice_pandas.py
- Polars 実装: practice_polars.py

### 3. Polars Lazy API による効果
Polars の特徴である Lazy API を用いて、検索・集計処理を「遅延評価」で実装しました。

- scan_csv() CSV読み込みの遅延
- filter / group_by / sort を組み合わせたクエリ構築
- collect() 呼び出しでクエリが実行される
- explain() で、クエリの実行計画を確認できる

```python
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
```


```plain text
vscode ➜ /workspaces/learning_polars (main) $ python practice_polars_lazy.py 
shape: (10, 2)
┌──────────────┬───────┐
│ cityName     ┆ count │
│ ---          ┆ ---   │
│ str          ┆ u32   │
╞══════════════╪═══════╡
│ 静岡市葵区    ┆ 5     │
│ 沼津市       ┆ 2     │
│ 浜松市中央区  ┆ 2     │
│ 富士市       ┆ 1     │
│ 島田市       ┆ 1     │
│ 三島市       ┆ 1     │
│ 掛川市       ┆ 1     │
│ 熱海市       ┆ 1     │
│ 静岡市清水区  ┆ 1     │
│ 下田市       ┆ 1     │
└─────────────┴───────┘
SORT BY [descending: [true]] [col("count")]
  AGGREGATE[maintain_order: false]
    [len().alias("count")] BY [col("cityName")]
    FROM
    Csv SCAN [data/22_shizuoka_all.csv]
    PROJECT 2/30 COLUMNS
    SELECTION: [(col("kind")) == ("101")]
    ESTIMATED ROWS: 95673
```

#### 考察
- Lazy API により、不要な列・行の読み込みが抑制される
- 大容量CSVを扱うETL処理では、I/O削減の効果が期待できる

#### 使用したコード
- Polars Lazy API 実装: practice_polars_lazy.py

## 検証環境
- **OS:** Windows 11 + WSL2 (Ubuntu 24.04)
- **CPU:** Intel Core i7-1260P @ 2.10GHz (12コア/16スレッド)
- **メモリ:** 16GB

## 実行方法（Docker / Dev Containers 対応）
1. **事前準備:** Docker Engine または Docker Desktop と VS Code (拡張機能: Dev Containers) を用意します。
2. **プロジェクト起動:** 本リポジトリを VS Code で開き、右下のポップアップまたはコマンドパレットから `コンテナで再度開く (Reopen in Container)` を選択します。
3. **1. CSV読み込み速度の比較:** コンテナ内のターミナルで以下のコマンドを実行します。
```bash
   python io_benchmark.py
```

## 実務での活用想定
- 大容量CSVを扱うETL・バッチ処理
- Pandas から Polars への移行検討時の技術検証
